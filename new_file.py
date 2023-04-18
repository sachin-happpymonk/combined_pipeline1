import math

my
global id
def output_func(my_list):
    
    frames=[]        
    ids_to_be_monitored=[]
    frame_anamoly_wgt = []
    activity_dict = {}
    det_score_dict = {}
    temp_list=[]
    metaObj = []
    frame_cid = {}

    people_count =[]
    vehicle_count = []
    object_count = []
   
    person_ids = []
    vehicle_ids = []
    object_ids = []

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
                if value['type'] == 'Person':
                    #person += 1
                    #person_counts[frame_id] = person
                    if cid not in person_ids:
                        person_ids.append(cid)
                    frame_cid[key]=person_ids
                    
                    
                    #person_counts[frame_id] = person
                elif value['type'] == 'Vehicle':
                       #v#ehicle +=1
                       #vehicle_counts[frame_id] = vehicle
                       if cid not in vehicle_ids:
                           vehicle_ids.append(cid)
                           
                       
                       frame_cid[key]=vehicle_ids
                       
                elif value['type'] == 'Elephant':
                       #object +=1
                       #object_counts[frame_id] = object 
                       if cid not in object_ids:
                           object_ids.append(cid)
                           
                       
                       frame_cid[key]=object_ids  

    temp = [key for elem in my_list for x in elem for detection in x['detection_info'] for key, values in detection.items() if values.get('type') == 'Person' and values.get('anamoly_score') is not None and values['anamoly_score'] > 50]
    for id in temp:
        if id not in ids_to_be_monitored:
            ids_to_be_monitored.append(id) 
    for x in my_list:
        for item in x:
            for detection in item['detection_info']:
                for key,values in detection.items():
                    detection_score = float(values.get('anamoly_score') or 0)
                    activity_score =  float(values.get('activity_score') or 0)
                    act_type = values.get('type')  
                    id = key  
                    if act_type == 'Person' and id not in people_count:
                        people_count.append(id)
                    if act_type == 'Vehicle' and id not in vehicle_count:
                        vehicle_count.append(id)
                    if act_type == 'Elephant' and id not in object_count:
                        object_count.append(id)
                    
                                  
                       
                    m = int(len(frame_cid[id]))
                    if m%2==0:
                        i = int(m/2)
                        con_id = frame_cid[id][i]
                    else:
                        i=int((m+1)/2)
                        con_id = frame_cid[id][i]                  
                    activity = values.get('activity')
                    if id in det_score_dict :
                        if detection_score not in det_score_dict[id]:
                            det_score_dict[id].append(detection_score)
                    else:
                        det_score_dict[id] = [detection_score]
                    if id in activity_dict:
                        if activity not in activity_dict[id]:
                                activity_dict[id].append(activity)
                    else:
                        activity_dict[id] = [activity]
                    act =   activity_dict[id]
                
                    det_score = det_score_dict[id]
                    temp = {
                                "type": act_type,
                                "detection_score": det_score,
                                "activity_score": activity_score,
                                "track": '',
                                "id": id,
                                "activity": act,
                                "detect_time": '',
                                "cids": con_id
                            } 
                    temp_list.append(temp)            
    
    for obj in temp_list:
        if obj not in metaObj:
            metaObj.append(obj)
    for items in metaObj:
        items['detection_score']=sum(items['detection_score'])/len(items['detection_score'])
           
    total_count = len(object_count) + len(people_count) + len(vehicle_count)

    metaBatch = {
        "detect": (total_count),
        "Frame_anomaly_score" : frame_anamoly_wgt,
        "count": {"people_count": (len(people_count)),
                  "vehicle_count": (len(vehicle_count)),
                  "ObjectCount" : (len(object_count)),
                  },
        "ids_to_be_monitored": ids_to_be_monitored,
        "cid": "str(detected_img_cid)",
        "object": metaObj

    }

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


    return primary

# print(output_func(my_list))