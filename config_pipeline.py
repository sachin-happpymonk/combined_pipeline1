from anamoly_track import trackmain
from multiprocessing import Process, Queue
from project_1_update_ import output_func


# gstreamer
import sys
from io import BytesIO
import os
from dotenv import load_dotenv
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

#multi treading 
import asyncio
import nats
import os
import json
import numpy as np 
from PIL import Image
import cv2
import glob
from nanoid import generate
from multiprocessing import Process, Queue
import torch
import torchvision.transforms as T
from general import (check_requirements_pipeline)
import logging 
import threading
import gc
import datetime #datetime module to fetch current time when frame is detected
import shutil
import ast
from nats.aio.client import Client as NATS
import nats

#PytorchVideo
from functools import partial


import pytorchvideo
from pytorchvideo.transforms.functional import (
    uniform_temporal_subsample,
    short_side_scale_with_boxes,
    clip_boxes_to_image,
)
from torchvision.transforms._functional_video import normalize
from pytorchvideo.data.ava import AvaLabeledVideoFramePaths
from pytorchvideo.models.hub import slow_r50_detection # Another option is slowfast_r50_detection

from visualization import VideoVisualizer

from pytz import timezone
from datetime import datetime 
import imageio
import subprocess as sp

import fnmatch


track_type = []


async def json_publish_activity(primary):    
    nc = await nats.connect(servers=["nats://216.48.181.154:5222"] , reconnect_time_wait= 50 ,allow_reconnect=True, connect_timeout=20, max_reconnect_attempts=60)
    js = nc.jetstream()
    JSONEncoder = json.dumps(primary)
    json_encoded = JSONEncoder.encode()
    Subject = "service.activities"
    Stream_name = "services"
    # await js.add_stream(name= Stream_name, subjects=[Subject])
    ack = await js.publish(Subject, json_encoded)
    print(f'Ack: stream={ack.stream}, sequence={ack.seq}')
    print("Activity is getting published")


def activity_trackCall(source, device_data):
    device_id = device_data[0]
    device_urn = device_data[1]
    timestampp = device_data[2]
    queue1 = Queue()
    print(source)
    det = Process(target= trackmain(source, device_id, queue1))
    det.start()
    video_data = queue1.get()
    video_data = [item for sublist in video_data for item in sublist]
    print(video_data)
    # video_anamoly_score = [frame_data['frame_anamoly_wgt'] for sml_vdo in video_data for frame_data in sml_vdo]

    #entire video info
    # print(video_data)
    outt_ = output_func(video_data)
    print(outt_)    
    torch.cuda.empty_cache()    
    asyncio.run(json_publish_activity(primary=outt_))
    torch.cuda.empty_cache()



def config_func(source, device_data):
    print("success")
    device_id = device_data[0]
    urn = device_data[1]
    timestampp = device_data[2]
    subsciptions = device_data[3]
    print(subsciptions)
    # if "activity" in subsciptions:
    Process(target = activity_trackCall, args = (source, device_data,)).start()
    # activity_trackCall(source, device_data)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
