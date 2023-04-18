import math
import cv2
#.env vars loaded
import os
from os.path import join, dirname
from dotenv import load_dotenv
import ast
import gc
import os, shutil
import subprocess as sp

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ipfs_url = os.getenv("ipfs")



global id
def most_frequent_func(lst):
    if len(list(set(lst))) == 1:
        res = lst[0]
    else:
        counts = {}
        for item in lst:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        most_frequent = sorted_counts[0][0]
        second_most_frequent = sorted_counts[1][0]
        if most_frequent == '':
            res =  second_most_frequent
        else:
            res =  most_frequent
    return res

def conv_path2cid(pathh):
    command = 'ipfs --api={ipfs_url} add {file_path} -Q'.format(file_path=pathh,ipfs_url=ipfs_url)
    output = sp.getoutput(command)
    return output

def padding_img(path, frame):
    # Set target size
    width, height = 640, 360

    # Load image
    img = frame
    # Get current size
    h, w, _ = img.shape

    # Calculate padding
    top = bottom = (height - h) // 2
    left = right = (width - w) // 2
    top, left,right,bottom = abs(top), abs(left),abs(right),abs(bottom)

    # Add black padding
    color = [0, 0, 0] # Black
    img_padded = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,value=color)

    # Resize image
    img_resized = cv2.resize(img_padded, (width, height))

    # Save image
    cv2.imwrite(path, img_resized)
    

def output_func(my_list):
    
    frames=[]               # this variable will hold the frame_id of all the frames in which a atleast one detection was made"
    ids_to_be_monitored=[]  #re-id of all the person type detection with anamoly score>50
    frame_anamoly_wgt = []
    person_counts = {}
    vehicle_counts = {}
    object_counts = {}
    activity_dict = {}
    det_score_dict = {}
    temp_list=[]
    metaObj = []
    frame_cid = {}
    did = []
    did_dict = {}
    did_info = []
   
    people_count_list =[]
    vehicle_count_list = []
    object_count_list = []
    crops = {}
   
    person_ids = []
    vehicle_ids = []
    object_ids = []

    count_non_empty = sum(1 for item in my_list if item != '')
    sub_my_list = my_list[0]
    h=len(my_list[0])

    # print(sub_my_list)
    last_frame_data = []
    for i in range(1, len(sub_my_list)):
        if len(sub_my_list[h-i]["detection_info"]) > 0:
            last_frame_data = sub_my_list[h-i]["detection_info"]
            break 
        else:
            continue
    lastframe_re_ids = [str(list(each.keys())[0]) for each in last_frame_data]
    cidss_dic =  {}
    #create dic with list of cid for each reid
    #{1: {'type': 'Person', 'activity': 'Unknow', 'confidence': 0, 'did': '', 'track_type': '100', 'crops': 'QmfMcu2MMU7YXqsXEKXV6nYwhWvWWZAxsKp8BAPduwwrED', 'anamoly_score': None, 'activity_score': None}}
    for each in sub_my_list:
        if len(each['detection_info'])>0:
            for every in each['detection_info']:
                if list(every.keys())[0] not in cidss_dic:
                    cidss_dic[list(every.keys())[0]] = []
                    cidss_dic[list(every.keys())[0]].append(every[list(every.keys())[0]]['crops'])
                else:
                    cidss_dic[list(every.keys())[0]].append(every[list(every.keys())[0]]['crops'])
        if each["cid"]:
            if "frame_cids" not in cidss_dic:
                cidss_dic["frame_cids"] = []
                cidss_dic["frame_cids"].append(each["cid"])
            else:
                cidss_dic["frame_cids"].append(each["cid"])

    # print("******************")
    # print(cidss_dic)            
    # print("*****************")
    final_cid = {}
    for each in cidss_dic:
        if len(cidss_dic[each]) <= 2:
            final_cid[each] = cidss_dic[each][0]
        elif len(cidss_dic[each]) == 0:
            final_cid[each] = None
        elif len(cidss_dic[each]) > 2:
            idxx = round(len(cidss_dic[each])/2)
            final_cid[each] = cidss_dic[each][idxx]
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    # #{1: 'QmagJYuUsQBZyjSQknH2czvQYKNXuX2UKzRDAm31cBkzoY', 2: 'QmNnfodd895WbSd4aaYgruSLrUn1m4ohHRLJ2go6aJBnpL', 3: 'QmTd3HariQNF6z3SnZaKgVgogs1pgFHW6UieDT3aGYqvoD', 'frame_cids': 'QmUL8Lp8gEQxrwbt5EFUX1QgJnYDhxGic48bZrXhsV4b7F'}
    # # finding middle cid 
    # print(final_cid)
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


    for item in my_list:
       for x in item:
        frame_anamoly_wgt.append(x['frame_anamoly_wgt'])
        frame_id = x['frame_id']
        detection_info = x['detection_info']
        if detection_info ==[]:
            continue
        else:
            frames.append(frame_id)
        person = 0
        vehicle = 0
        object = 0
        cid = x['cid']
        for detection in x['detection_info']:
            for key, value in detection.items():
                did = value.get('did')
                if key in did_dict :
                   did_dict[key].append(did)                             
                else:
                   did_dict[key] = [did]
                # did  = []
                # did.append(value.get('did'))
                # did_dict[key] = did
                if value['type'] == 'Person':
                    person += 1
                    person_counts[frame_id] = person
                    # if cid not in person_ids:
                    #     person_ids.append(cid)
                    # frame_cid[key]=person_ids
                    
                    
                    person_counts[frame_id] = person
                elif value['type'] == 'Vehicle':
                       vehicle +=1
                       vehicle_counts[frame_id] = vehicle
                    #    if cid not in vehicle_ids:
                    #        vehicle_ids.append(cid)
                    #frame_cid[key]=vehicle_ids
                       
                elif value['type'] == 'Elephant':
                       object +=1
                       object_counts[frame_id] = object 
                    #    if cid not in object_ids:
                    #        object_ids.append(cid)
                    #    frame_cid[key]=object_ids  




    temp = [key for elem in my_list for x in elem for detection in x['detection_info'] for key, values in detection.items() if values.get('type') == 'Person' and values.get('anamoly_score') is not None and values['anamoly_score'] > 50]
    for id in temp:
        if id not in ids_to_be_monitored:
            ids_to_be_monitored.append(id)





    vehicle_count = sum(vehicle_counts.values())  # this variable will hold the count of total vehicles detected overall
    person_count = sum(person_counts.values())  # this variable will hold the count of total person detected overall
    animal_count = sum(object_counts.values())  # this variable will hold the count of total elephants detected overall
    total_count = vehicle_count + person_count + animal_count
    
    

    frame_count_vehicle = len(vehicle_counts)  # this variable will hold the count of total frames in which vehicle was detected
    frame_count_person = len(person_counts)    # this variable will hold the count of total frames in which people were detected
    frame_count_animal = len(object_counts)    # this variable will hold the count of total frames in which elephant was detected
    frame_count = len(frames)
    


    # if frame_count != 0 and total_count > frame_count:
    #     detection_count = math.ceil(total_count / frame_count)
    # else :
    #     detection_count = 0
    if frame_count_vehicle != 0 and vehicle_count > frame_count_vehicle:
        avg_Batchcount_vehicle = math.ceil(vehicle_count / frame_count_vehicle)
    else :
        avg_Batchcount_vehicle = 0
    if frame_count_animal != 0 and animal_count > frame_count_animal:
        avg_Batchcount_animal = math.ceil(animal_count / frame_count_animal)
    else :
        avg_Batchcount_animal = 0
    if frame_count_person !=0 and person_count > frame_count_person:
        avg_Batchcount_person = math.ceil(person_count / frame_count_person)
    else :
        avg_Batchcount_person = 0

    total_add = avg_Batchcount_person + avg_Batchcount_animal +  avg_Batchcount_vehicle

    for k,v in did_dict.items():
                new= {}
                if all(val == '' or val == None for val in v):
                    new['id'] = k
                    new['track'] = '100'
                    new['old_id'] = k
                    did_info.append(new)
                else:
                    id  = most_frequent_func(v)
                    new['id'] = id
                    
                    track_ = str(id[0:2])
                    new['track'] = track_
                    new['old_id'] = k
                    did_info.append(new)

    for x in my_list:
        for item in x:
            for detection in item['detection_info']:
                for key,values in detection.items():
              
                    detection_score = float(values.get('anamoly_score') or 0)
                    activity_score =  float(values.get('activity_score') or 0)
                    did  =  values.get('did')
                    act_type = values.get('type')  
                    re_id = key 
                     
                    crop = values.get('crops') 
                    if act_type == 'Person' and re_id not in people_count_list:
                        people_count_list.append(re_id)
                    if act_type == 'Vehicle' and re_id not in vehicle_count_list:
                        vehicle_count_list.append(re_id)
                    if act_type == 'Elephant' and re_id not in object_count_list:
                        object_count_list.append(re_id)
                    # if re_id in crops:
                    #     if crop not in crops[re_id]:
                    #             crops[re_id].append(crop)
                    # else:
                    #      crops[re_id] = [crop]
                    for m in final_cid:
                        if m==re_id:
                            c_id = final_cid[m]
                    # m = int(len(crops[re_id]))
                    
                    # if m%2==0 and m<2:
                      
                    #     c_id = crops[re_id][0]
                    # elif  m%2==0 and m>2:
                    #     i = int(m/2) + 1
                    #     c_id = crops[re_id][i]
                    # elif m%2!=0 and m>2:
                    #     i=int((m+1)/2)
                    #     c_id = crops[re_id][i]      
                    # elif m==1:
                    #     c_id = crops[re_id][0]

                    activity = values.get('activity')


                    if re_id in det_score_dict :
                        if detection_score not in det_score_dict[re_id]:
                            det_score_dict[re_id].append(detection_score)
                    else:
                        det_score_dict[re_id] = [detection_score]

                    if re_id in did_dict :
                        did_dict[re_id].append(did)
                        # if did not in  did_dict[re_id]:
                             
                    else:
                         did_dict[re_id] = [did]

                    
                    if re_id in activity_dict:
                        if activity not in activity_dict[re_id]:
                                activity_dict[re_id].append(activity)
                    else:
                        activity_dict[re_id] = [activity]

                   
                    
                    act =   activity_dict[re_id]
                
                    det_score = det_score_dict[re_id]
                  
                    if act == [""]:
                        act = []
                    for y in did_info:
                        if re_id == y['old_id']:
                            id = y['id']
                            track  = y['track']


                    temp = {
                                "type": act_type,
                                "detectionScore": det_score,
                                "activityScore": activity_score,
                                "track": track,
                                "id": str(id),
                                "activity": act,
                                "detectTime": '',
                                "cids": c_id
                            } 
                    temp_list.append(temp)            
    
    for obj in temp_list:          #this make sures that only unique entries are in metaObj
        if obj not in metaObj:
            metaObj.append(obj)
    for items in metaObj:
        items['detectionScore']=sum(items['detectionScore'])/len(items['detectionScore'])
           
    
    
    if len(people_count_list) ==1:
        count_p = len(people_count_list)
    else :
        count_p = avg_Batchcount_person
    
    if len(vehicle_count_list) == 1:
        count_v = len(vehicle_count_list)
    else :
        count_v = avg_Batchcount_vehicle
        
    if len(object_count_list) == 1:
        count_o = len(object_count_list)
    else:
         count_o = avg_Batchcount_animal
    
    count_all = count_o +count_v +count_p

    if 'frame_cids' in final_cid:
        finn = final_cid['frame_cids']
    else:
        finn = None

    metaBatch = {
        "detect": (count_all),
        "frameAnomalyScore" : frame_anamoly_wgt,
        "count": {"peopleCount": (count_p),
                  "vehicleCount": (count_v),
                  "ObjectCount" : (count_o),
                  },
        "anamolyIds": ids_to_be_monitored,
         'cid' : finn,
        "object": metaObj
       
    }
    # print("$$$$$$$$$$$$$")
    # print(metaObj)
    # print("$$$$$$$$$$$$$")
    # h=len(metaObj)
    # # print(h)
    # print(metaObj[h-1]['detection_info']) 
    #     # metaObj=metaObj[h-1]
    primary = {
        "type": "activity",
        "deviceid": "",
        "batchid": "",
        "timestamp": "",
        "geo": {
            "latitude": "",
            "longitude": ""
        },
        "metaData": metaBatch
    }
    #primary["metaData"]["object"].append(test_data)
    #primary["metaData"]["object"].append(test_data1)
    # print(primary)

    object_updated = [each for each in primary["metaData"]["object"] if each["id"] in lastframe_re_ids or "did" in each["id"]]


    # find counts of vehicle person and elephant
    vehicle_cnt = 0
    ppl_cnt = 0
    ele_cnt = 0
    for each in object_updated:
        if each["type"] == "Vehicle":
            vehicle_cnt = vehicle_cnt + 1
        if each["type"] == "Person":
            ppl_cnt = ppl_cnt + 1
        if each["type"] == "Elephant":
            ele_cnt = ele_cnt + 1 
    primary["metaData"]["count"]["peopleCount"] = ppl_cnt
    primary["metaData"]["count"]["vehicleCount"] = vehicle_cnt
    primary["metaData"]["count"]["ObjectCount"] = ele_cnt
    primary["metaData"]["object"] = object_updated
    total_count_1  =len(primary["metaData"]["object"])
    primary["metaData"]["detect"] = total_count_1

    if primary["metaData"]['cid']:
        # convert full frame numpy to cid
        pathh = "./"+primary['deviceid']+"/cid_ref_full.jpg"
        padding_img(pathh,primary["metaData"]['cid'][0])
        primary["metaData"]['cid'] = conv_path2cid(pathh)

        for each in primary["metaData"]["object"]:
            pathh = "./"+primary['deviceid']+"/cid_ref.jpg"
            padding_img(pathh,each["cids"][0])
            each["cids"] = conv_path2cid(pathh)

        

    #primary[]


# h=len(metaObj)

    return primary




# print(output_func(my_list))