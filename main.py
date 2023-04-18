# gstreamer python bindings
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

# os
import sys
import os

# concurrency and multi-processing 
import asyncio
from multiprocessing import Process, Queue

# Nats
from nats.aio.client import Client as NATS
import nats
# json
import json
# datetime
from pytz import timezone
import time
from datetime import datetime 
import imageio
import subprocess as sp
import torch
import shutil
# cv
import numpy as np
import cv2
import io

#.env vars loaded
from os.path import join, dirname
from dotenv import load_dotenv
import ast
import gc
import psutil
from nanoid import generate

from pytorchvideo.models.hub import slowfast_r50_detection
from yolo_slowfast.deep_sort.deep_sort import DeepSort
# from memory_profiler import profile

#to fetch data from postgres
from db_fetch import fetch_db
from db_fetch_members import fetch_db_mem
from db_push import push_db

from lmdb_list_gen import attendance_lmdb_known, attendance_lmdb_unknown
from facedatainsert_lmdb import add_member_to_lmdb
from anamoly_track import trackmain
from project_1_update_ import output_func
# obj_model = torch.hub.load('ultralytics/yolov5', 'custom', path='./three_class_05_dec.pt')

obj_model = torch.hub.load('Detection', 'custom', path='./three_class_05_dec.pt', source='local',force_reload=True)
deepsort_tracker = DeepSort("./yolo_slowfast/deep_sort/deep_sort/deep/checkpoint/ckpt.t7")
device = 'cuda'
video_model = slowfast_r50_detection(True).eval().to(device)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ipfs_url = os.getenv("ipfs")
nats_urls = os.getenv("nats")
nats_urls = ast.literal_eval(nats_urls)

pg_url = os.getenv("pghost")
pgdb = os.getenv("pgdb")
pgport = os.getenv("pgport")
pguser = os.getenv("pguser")
pgpassword = os.getenv("pgpassword")

nc_client = NATS() # global Nats declaration
Gst.init(sys.argv) # Initializes Gstreamer, it's variables, paths

# creation of directories for file storage
hls_path = "./Hls_output"
gif_path = "./Gif_output"
    
if os.path.exists(hls_path) is False:
    os.mkdir(hls_path)
    
if os.path.exists(gif_path) is False:
    os.mkdir(gif_path)

# list variables
frames = []
numpy_frames = []
gif_frames = []
known_whitelist_faces = []
known_whitelist_id = []
known_blacklist_faces = []
known_blacklist_id = []
cid_unpin_cnt = 0
gif_cid_list = []
# flag variable
start_flag = False
image_count = 0
gif_batch = 0
batch_count = 0
frame_count = 0
track_type = []
veh_pub = True
only_vehicle_batch_cnt = 0
unique_device = []

def remove_cnts(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def load_lmdb_list():
    known_whitelist_faces1, known_whitelist_id1 = attendance_lmdb_known()
    known_blacklist_faces1, known_blacklist_id1 = attendance_lmdb_unknown()
    
    global known_whitelist_faces
    known_whitelist_faces = known_whitelist_faces1

    global known_whitelist_id
    known_whitelist_id = known_whitelist_id1
    
    global known_blacklist_faces
    known_blacklist_faces = known_blacklist_faces1

    global known_blacklist_id
    known_blacklist_id = known_blacklist_id1
    print("-------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------")
    print(len(known_whitelist_faces), len(known_blacklist_faces))
    print("-------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------")

async def json_publish_activity(primary):    
    nc = await nats.connect(servers=nats_urls , reconnect_time_wait= 50 ,allow_reconnect=True, connect_timeout=20, max_reconnect_attempts=60)
    js = nc.jetstream()
    JSONEncoder = json.dumps(primary)
    json_encoded = JSONEncoder.encode()
    Subject = "service.activities"
    Stream_name = "services"
    ack = await js.publish(Subject, json_encoded)
    print(" ")
    print(f'Ack: stream={ack.stream}, sequence={ack.seq}')
    print("Activity is getting published")

def activity_trackCall(source, device_data, datainfo):
    global only_vehicle_batch_cnt,veh_pub
    device_id = device_data[0]
    device_urn = device_data[1]
    timestampp = device_data[2]
    lat = device_data[4]
    long = device_data[5]
    queue1 = Queue()
    batchId = generate(size=32)

    trackmain(
        source, 
        device_id, 
        batchId,
        queue1, 
        datainfo,
        obj_model,
        deepsort_tracker,
        video_model,
        device
        )

    video_data = queue1.get()

    # print(video_data)

    outt_ = output_func(video_data)
    outt_['deviceid'] = device_id
    outt_['timestamp'] = timestampp
    outt_['geo'] = {"latitude":lat, "longitude":long}
    pid = psutil.Process()
    memory_bytes = pid.memory_info().rss
    memory_mb = memory_bytes / 1024 / 1024
    mbb = f"{memory_mb:.2f}"
    outt_['memory'] = str(float(mbb) / 1024) + " GB"
    outt_["version"] = "v0.0.2"   
    outt_["batchid"] = batchId

    if outt_['metaData']['count']['peopleCount'] == 0 and outt_['metaData']['count']['vehicleCount'] > 0:
        outt_['type']='tracking'
    if len(outt_['metaData']['anamolyIds'])>0:
        outt_['type']='anamoly'
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    # print(" ")
    # print(outt_['metaData']['count']['peopleCount'],outt_['metaData']['count']['vehicleCount'])
    # print(" ")
    if outt_['metaData']['count']['peopleCount'] == 0 or outt_['metaData']['count']['vehicleCount'] != 0:
        veh_pub =True


    if outt_['metaData']['count']['peopleCount'] != 0 or outt_['metaData']['count']['vehicleCount'] != 0:

        print(veh_pub)
        if veh_pub:
            # print(outt_)
            asyncio.run(json_publish_activity(primary=outt_)) 
            print(outt_)
            veh_pub = False

    torch.cuda.empty_cache()

    pid = os.getpid()
    print("killing ",str(pid))
    sp.getoutput("kill -9 "+str(pid))

def config_func(source, device_data,datainfo ):
    
    # print("success")
    device_id = device_data[0]
    urn = device_data[1]
    timestampp = device_data[2]
    subsciptions = device_data[3]
    lat = device_data[4]
    long = device_data[5]
    print(subsciptions)
    
    activity_trackCall(source, device_data,datainfo)
    # # activity_trackCall(source, device_data)
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

def device_hls_push(device_id, device_info):
    
    device_data = device_info[device_id]
    
    ddns_name = device_data['ddns']
    
    if(ddns_name == None):
        hostname = 'localhost'
    else:
        hostname = ddns_name
    
    hls_url = 'https://{hostname}/live/{device_id}/{device_id}.m3u8'.format(device_id=device_id, hostname=hostname)
    status = push_db(hls_url, device_id)
    return status
        
    # device_data = device_info[device_id]
    
    # rtsp = device_data['rtsp']
    
    # if rtsp not in unique_device:
    #     unique_device.append(rtsp)

    # print(unique_device)
    # device_cnt = (unique_device.index(rtsp)) + 1
    # print(device_cnt)
    
    # hls_url = 'https://hls.ckdr.co.in/live/stream{device_cnt}/{device_cnt}.m3u8'.format(device_cnt = device_cnt)
    # status = push_db(hls_url, device_id)
    # return status

async def device_snap_pub(device_id, urn, gif_cid, time_stamp):
    nc = await nats.connect(servers=nats_urls , reconnect_time_wait= 50 ,allow_reconnect=True, connect_timeout=20, max_reconnect_attempts=60)
    js = nc.jetstream()
    device_data = {
        "deviceId": device_id,
        "urn": urn,
        "timestamp": time_stamp,
        "thumbnail": gif_cid
    }
    JSONEncoder = json.dumps(device_data)
    json_encoded = JSONEncoder.encode()
    print(json_encoded)
    print("Json encoded")
    Subject = "service.device_thumbnail"
    Stream_name = "service"
    ack = await js.publish(Subject, json_encoded)
    print(f'Ack: stream={ack.stream}, sequence={ack.seq}')
    print("Thumbnail is getting published")


def numpy_creation(device_id, urn, img_arr, timestamp,device_data):

    # filename for mp4
    video_name_gif = gif_path + '/' + str(device_id)
    if not os.path.exists(video_name_gif):
        os.makedirs(video_name_gif, exist_ok=True)
    
    path = video_name_gif + '/' + str(timestamp).replace(' ','') + '.gif'
    
    global image_count, cid_unpin_cnt, gif_batch, gif_frames
    
    image_count += 1
    
    if (image_count < 31):
        numpy_frames.append(img_arr)
        gif_frames.append(img_arr)
    elif (image_count >= 31):
        print(timestamp)

        datainfo = [known_whitelist_faces, known_blacklist_faces,known_whitelist_id,known_blacklist_id]
        Process(target = config_func,args = (numpy_frames, device_data,datainfo,)).start()
        # config_func(numpy_frames, device_data,datainfo)
        gif_batch += 1 

        
        if gif_batch == 5:
            gif_frames = gif_frames[-100:]
            print(timestamp)
            print("Images added: ", len(gif_frames))
            print("Saving GIF file")
            with imageio.get_writer(path, mode="I") as writer:
                for idx, frame in enumerate(gif_frames):
                    print("Adding frame to GIF file: ", idx + 1)
                    writer.append_data(frame)
                    
            # print("PATH:", path)
            command = 'ipfs --api={ipfs_url} add {file_path} -Q'.format(ipfs_url=ipfs_url, file_path=path)
            gif_cid = sp.getoutput(command)
            # print(gif_cid)
            
            os.remove(path)
            print("The path has been removed")
            # await device_snap_pub(device_id = device_id, urn=urn, gif_cid = gif_cid, time_stamp = timestamp)
            asyncio.run(device_snap_pub(device_id = device_id, urn=urn, gif_cid = gif_cid, time_stamp = timestamp))
            
            frames.clear()
            image_count = 0  
        image_count = 0
        numpy_frames.clear()

# def gif_creation(device_id, urn, img_arr, timestamp, batch_count):

#     global image_count, gif_path, cid_unpin_cnt
    
#     # filename for mp4
#     video_name_gif = gif_path + '/' + str(device_id)
#     if not os.path.exists(video_name_gif):
#         os.makedirs(video_name_gif, exist_ok=True)
    
#     path = video_name_gif + '/' + str(timestamp).replace(' ','') + '.gif'
    
#     image_count += 1
#     if (batch_count == 0 and image_count <= 30):
#         frames.append(img_arr)
#     elif (batch_count == 1 and image_count > 30):
#         print(timestamp)
#         print("Images added: ", len(frames))
#         print("Saving GIF file")
#         with imageio.get_writer(path, mode="I") as writer:
#             for idx, frame in enumerate(frames):
#                 print("Adding frame to GIF file: ", idx + 1)
#                 writer.append_data(frame)
                
#         print("PATH:", path)
#         command = 'ipfs --api={ipfs_url} add {file_path} -Q'.format(ipfs_url=ipfs_url, file_path=path)
#         gif_cid = sp.getoutput(command)
#         print(gif_cid)
        
#         os.remove(path)
#         print("The path has been removed")
#         # await device_snap_pub(device_id = device_id, urn=urn, gif_cid = gif_cid, time_stamp = timestamp)
#         asyncio.run(device_snap_pub(device_id = device_id, urn=urn, gif_cid = gif_cid, time_stamp = timestamp))
        
#         frames.clear()
#         image_count = 0    

def gst_hls(device_id, device_info):
        
    location = device_info['rtsp'] # Fetching device info
    username = device_info['username']
    password = device_info['password']
    ddns_name = device_info['ddns']
    encode_type = device_info['videoEncodingInformation']
    
    print("Entering HLS Stream")
    
    # filename for hls
    video_name_hls = hls_path + '/' + str(device_id)
    if not os.path.exists(video_name_hls):
        os.makedirs(video_name_hls, exist_ok=True)
    print(video_name_hls)
    
    if(ddns_name == None):
        hostname = 'localhost'
    else:
        hostname = ddns_name
        
    try:
        if((encode_type.lower()) == "h264"):
            pipeline = Gst.parse_launch('rtspsrc name=h_rtspsrc_{device_id} location={location} latency=10 protocols="tcp" drop-on-latency=true user-id={username} user-pw={password} ! rtph264depay name=h_depay_{device_id} ! mpegtsmux name=h_mux_{device_id} ! hlssink name=h_sink_{device_id}'.format(location=location, device_id=device_id, username=username, password=password))
        elif((encode_type.lower()) == "h265"):
            pipeline = Gst.parse_launch('rtspsrc name=h_rtspsrc_{device_id} location={location} latency=10 protocols="tcp" drop-on-latency=true user-id={username} user-pw={password} ! rtph265depay name=h_depay_{device_id} ! mpegtsmux name=h_mux_{device_id} ! hlssink name=h_sink_{device_id}'.format(location=location, device_id=device_id, username=username, password=password))
        elif((encode_type.lower()) == "mp4"):
            pipeline = Gst.parse_launch('rtspsrc name=h_rtspsrc_{device_id} location={location} protocols="tcp" ! decodebin name=h_decode_{device_id} ! x264enc name=h_enc_{device_id} ! mpegtsmux name=h_mux_{device_id} ! hlssink name=h_sink_{device_id}'.format(device_id = device_id, location=location))
            
        # sink params
        sink = pipeline.get_by_name('h_sink_{device_id}'.format(device_id = device_id))

        # Location of the playlist to write
        sink.set_property('playlist-root', 'https://{hostname}/live/{device_id}'.format(device_id=device_id, hostname=hostname))
        # Location of the playlist to write
        sink.set_property('playlist-location', '{file_path}/{file_name}.m3u8'.format(file_path=video_name_hls, file_name=device_id))
        # Location of the file to write
        sink.set_property('location', '{file_path}/segment.%01d.ts'.format(file_path=video_name_hls))
        # The target duration in seconds of a segment/file. (0 - disabled, useful for management of segment duration by the streaming server)
        sink.set_property('target-duration', 10)
        # Length of HLS playlist. To allow players to conform to section 6.3.3 of the HLS specification, this should be at least 3. If set to 0, the playlist will be infinite.
        sink.set_property('playlist-length', 3)
        # Maximum number of files to keep on disk. Once the maximum is reached,old files start to be deleted to make room for new ones.
        sink.set_property('max-files', 6)
        
        if not sink or not pipeline:
            print("Not all elements could be created.")
        else:
            print("All elements are created and launched sucessfully!")

        # Start playing
        ret = pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.SUCCESS:
            print("Successfully set the pipeline to the playing state.")
            
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Unable to set the pipeline to the playing state.")
            
    except TypeError as e:
        print(TypeError," gstreamer hls streaming error >> ", e)

def gst_mp4(device_id, device_info):
    
    location = device_info['rtsp'] # Fetching device info
    username = device_info['username']
    password = device_info['password']
    subscriptions = device_info['subscriptions']
    encode_type = device_info['videoEncodingInformation']
    urn = device_info['urn']
    lat = device_info['lat']
    long = device_info['long']
    
    print("Entering Framewise Stream")
    
    def gst_to_opencv(sample):
        buf = sample.get_buffer()
        caps = sample.get_caps()
                    
        arr = np.ndarray(
            (caps.get_structure(0).get_value('height'),
            caps.get_structure(0).get_value('width')),
            buffer=buf.extract_dup(0, buf.get_size()),
            dtype=np.uint8)

        return arr

    def new_buffer(sink, data):
                     
        global image_arr
        device_data = []
        device_data.append(device_id)
        device_data.append(urn)
        device_data.append(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f'))
        device_data.append(subscriptions)
        device_data.append(lat)
        device_data.append(long)
        sample = sink.emit("pull-sample")
        buffer = sample.get_buffer()
        arr = gst_to_opencv(sample)
        rgb_frame = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
        # print(rgb_frame.shape)
        datetime_ist = str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f'))
        numpy_creation(device_id=device_id, urn=urn, img_arr=rgb_frame, timestamp=datetime_ist,device_data=device_data)    
        return Gst.FlowReturn.OK
    
    try:
        if((encode_type.lower()) == "h264"):
            pipeline = Gst.parse_launch('rtspsrc name=g_rtspsrc_{device_id} location={location} latency=30 protocols="tcp" drop-on-latency=true user-id={username} user-pw={password} !  rtph264depay name=g_depay_{device_id} ! h264parse config_interval=-1 name=g_parse_{device_id} ! decodebin name=h_decode_{device_id} ! videoconvert name=h_videoconvert_{device_id} ! videoscale name=h_videoscale_{device_id} ! video/x-raw,width=1920, height=1080 ! appsink name=g_sink_{device_id}'.format(location=location, device_id=device_id, username=username, password=password))
        elif((encode_type.lower()) == "h265"):
            pipeline = Gst.parse_launch('rtspsrc name=g_rtspsrc_{device_id} location={location} latency=30 protocols="tcp" drop-on-latency=true user-id={username} user-pw={password} !  rtph265depay name=g_depay_{device_id} ! h265parse config_interval=-1 name=g_parse_{device_id} ! decodebin name=h_decode_{device_id} ! videoconvert name=h_videoconvert_{device_id} ! videoscale name=h_videoscale_{device_id} ! video/x-raw,width=1920, height=1080 ! appsink name=g_sink_{device_id}'.format(location=location, device_id=device_id, username=username, password=password))
        elif((encode_type.lower()) == "mp4"):
            pipeline = Gst.parse_launch('rtspsrc name=g_rtspsrc_{device_id} location={location} protocols="tcp" ! decodebin name=g_decode_{device_id} ! videoconvert name=g_videoconvert_{device_id} ! videoscale name=g_videoscale_{device_id} ! video/x-raw,width=640, height=320 ! appsink name=g_sink_{device_id}'.format(location=location, device_id=device_id))
        if not pipeline:
            print("Not all elements could be created.")
        else:
            print("All elements are created and launched sucessfully!")
        
        # sink params
        sink = pipeline.get_by_name('g_sink_{device_id}'.format(device_id=device_id))
        
        sink.set_property("emit-signals", True)
        sink.connect("new-sample", new_buffer, device_id)
        
        # Start playing
        ret = pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.SUCCESS:
            print("Able to set the pipeline to the playing state.")
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Unable to set the pipeline to the playing state.")
            
    except TypeError as e:
        print(TypeError," gstreamer Framewise error >> ", e)  
             
#@profile
def call_gstreamer(device_data):
    # i = 0
    print("Got device info from DB")
    for i,key in enumerate(device_data):
        # print(i, key)
        # i += 1
        # if(i <= 1):
        Process(target = gst_mp4(key, device_data[key])).start()
        Process(target = gst_hls(key, device_data[key])).start()
        push_status = device_hls_push(key, device_data)
        print(push_status)

async def device_info(msg):
    if msg.subject == "service.device_discovery":
        device_info = {}
        print("Received a Device data\n")  
        deviceInfo_raw = msg.data  # fetch data from msg
        print(deviceInfo_raw)
        deviceInfo_decode = deviceInfo_raw.decode("utf-8") # decode the data which is in bytes
        deviceInfo_json = json.loads(deviceInfo_decode) # load it as dict
        print(deviceInfo_json)
        deviceInfo_username = deviceInfo_json['username'] # fetch all the individual fields from the dict
        deviceInfo_password = deviceInfo_json['password']
        deviceInfo_ip = deviceInfo_json['ddns']
        deviceInfo_port = deviceInfo_json['port']
        deviceInfo_rtsp = deviceInfo_json['rtsp']
        deviceInfo_encode = deviceInfo_json['videoEncodingInformation']
        deviceInfo_id = deviceInfo_json['deviceId']
        deviceInfo_urn = deviceInfo_json['urn']
        deviceInfo_sub = deviceInfo_json['subscriptions']
        lat = deviceInfo_json['lat']
        long = deviceInfo_json['long']
        device_info[deviceInfo_id] = {}
        device_info[deviceInfo_id]['urn'] = deviceInfo_urn
        device_info[deviceInfo_id]['videoEncodingInformation'] = deviceInfo_encode
        device_info[deviceInfo_id]['rtsp'] = deviceInfo_rtsp
        device_info[deviceInfo_id]['port'] = deviceInfo_port
        device_info[deviceInfo_id]['ddns'] = deviceInfo_ip
        device_info[deviceInfo_id]['password'] = deviceInfo_password
        device_info[deviceInfo_id]['username'] = deviceInfo_username
        device_info[deviceInfo_id]['subscriptions'] = deviceInfo_sub
        device_info[deviceInfo_id]['lat'] = lat
        device_info[deviceInfo_id]['long'] = long
        
        gst_mp4(deviceInfo_id, device_info[deviceInfo_id])
        
        gst_hls(deviceInfo_id, device_info[deviceInfo_id])
        push_status = device_hls_push(deviceInfo_id, device_info)
        print(push_status)

    if msg.subject == "service.member_update":
        
        print(msg.data)   
        data = (msg.data)
        #print(data)
        data  = data.decode()
        data = json.loads(data)
        print(data)
        status = add_member_to_lmdb(data)
        if status:
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            await nc_client.publish(msg.reply,b'ok')
            print("Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data))
            load_lmdb_list()

def load_lmdb_fst(mem_data):
    i = 0
    for each in mem_data:
        i = i+1
        # if i < 5:
        add_member_to_lmdb(each)
        print("inserting ",each)

#@profile
async def main():
    try:

        remove_cnts("./lmdb")
        load_lmdb_list()
        print("removed lmdb contents")
        mem_data = fetch_db_mem()
        # print(mem_data)
        
        load_lmdb_fst(mem_data)
        load_lmdb_list()

        device_data = fetch_db()
        print(device_data)
        call_gstreamer(device_data)

        await nc_client.connect(servers=nats_urls) # Connect to NATS cluster!
        print("Nats Connected successfully!\n")
        await nc_client.subscribe("service.*", cb=device_info) # Subscribe to the device topic and fetch data through callback
        print("Subscribed to the topic, now you'll start receiving the Device details!\n")

    except Exception as e:
        await nc_client.close() # Close NATS connection
        print("Nats encountered an error: \n", e)


if __name__ == '__main__':
    torch.multiprocessing.set_start_method('spawn', force=True)
    loop = asyncio.get_event_loop()
    try :
        loop.run_until_complete(main())
        loop.run_forever()
    except RuntimeError as e:
        print("error ", e)
        print(torch.cuda.memory_summary(device=None, abbreviated=False), "cuda")

