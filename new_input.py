import math


def output_func(my_list):

    frames=[]        # this variable will hold the count of total number of frames in which a atleast one vehicle was detected"
    ids_to_be_monitored=[]
    frame_anamoly_wgt = []
    person_counts = {}
    vehicle_counts = {}
    object_counts = {}
    for item in my_list:
       for x in item:
        frame_id = x['frame_id']
        detection_info = x['detection_info']
        if detection_info ==[]:
            continue
        else:
            frames.append(frame_id)
        person = 0
        vehicle = 0
        object = 0
        for detection in x['detection_info']:
            for key, value in detection.items():
                if value['type'] == 'Person':
                    person += 1
                    person_counts[frame_id] = person
                elif value['type'] == 'Vehicle':
                       vehicle +=1
                       vehicle_counts[frame_id] = vehicle
                elif value['type'] == 'Elephant':
                       object +=1
                       object_counts[frame_id] = object    


    temp = [key for elem in my_list for x in elem for detection in x['detection_info'] for key, values in detection.items() if values.get('type') == 'Person' and values.get('anamoly_score') is not None and values['anamoly_score'] > 50]
    for id in temp:
        if id not in ids_to_be_monitored:
            ids_to_be_monitored.append(id)





    vehicle_count = sum(vehicle_counts.values())  # this variable will hold the count of total vehicles detected overall
    person_count = sum(person_counts.values())  # this variable will hold the count of total person detected overall
    animal_count = sum(object_counts.values())  # this variable will hold the count of total elephants detected overall
    total_count = vehicle_count + person_count + animal_count
    

    frame_count_vehicle = len(vehicle_counts)  # this variable will hold the count of total frames in which vehicle was detected
    frame_count_person = len(person_counts)
    frame_count_animal = len(object_counts)
    frame_count = len(frames)

    if frame_count != 0 and total_count > frame_count:
        detection_count = math.ceil(total_count / frame_count)
    else :
        detection_count = 0
    if frame_count_vehicle != 0 and vehicle_count > frame_count_vehicle:
        avg_Batchcount_vehicle = math.ceil(vehicle_count / frame_count_vehicle)
    else :
        avg_Batchcount_vehicle = 0
    if frame_count_animal != 0 and animal_count > frame_count_animal:
        avg_Batchcount_elephant = math.ceil(animal_count / frame_count_animal)
    else :
        avg_Batchcount_elephant = 0
    if frame_count_person !=0 and person_count > frame_count_person:
        avg_Batchcount_person = math.ceil(person_count / frame_count_person)
    else :
        avg_Batchcount_person = 0

    metaObj = [{
        "type": values.get('type'),
        "detection_score": int(values.get('anamoly_score') or 0),
        "activity_score": int(values.get('activity_score') or 0),
        "track": '',
        "id": '',
        "activity": values.get('activity'),
        "detect_time": '',
        "cids": None
    } for x in my_list for item in x for detection in item['detection_info'] for key, values in detection.items()]

    metaBatch = {
        "detect": (detection_count),
        "Frame_anomaly_score" : frame_anamoly_wgt,
        "count": {"people_count": (avg_Batchcount_person),
                  "vehicle_count": (avg_Batchcount_vehicle),
                  "ObjectCount" : (avg_Batchcount_elephant),
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

#print(output_func(my_list))