def output_func(my_list):

    frame_count = 0  # this variable will hold the count of total number of frames in which a atleast one vehicle was detected"
    frame_anamoly_wgt = []
    ids_to_be_monitored = []
    frame_info_vehicle = {}  # this dictionary will hold the info about frames in which a atleast one vehicle was detected
    frame_info_person = {}
    frame_info_animal = {}

    for frame in my_list:
        frame_anamoly_wgt.append(frame['frame_anamoly_wgt'])
        frame_id = frame['frame_id']
        detection_info = frame['detection_info']
        if detection_info == []:
            frame_count = frame_count
        else:
            frame_count += 1
        for detection in detection_info:
            a_count = 0
            v_count = 0
            p_count = 0
            for obj_id, obj_info in detection.items():
                if obj_info.get('type') == 'Vehicle':
                    v_count += 1
                    frame_info_vehicle[frame_id] = v_count
                elif obj_info.get('type') == 'Person':
                    p_count += 1
                    frame_info_person[frame_id] = p_count
                elif obj_info.get('type') == 'Animal':
                    a_count+=1
                    frame_info_animal[frame_id] = a_count

    # Loop through the dictionaries in the list
    for detection in my_list:
        detection_info = detection.get('detection_info')
        if detection_info:
            # Loop through the keys in the detection_info dictionary
            for key in detection_info[0]:
                # Check if the anamoly_score for this key is greater than 50
                anamoly_score = detection_info[0][key]['anamoly_score']
                type_ = detection_info[0][key]['type']
                if anamoly_score == None:
                    pass
                elif anamoly_score > 50 and type_ == 'Person':
                    ids_to_be_monitored.append(key)

    vehicle_count = sum(frame_info_vehicle.values())  # this variable will hold the count of total vehicles detected overall
    person_count = sum(frame_info_person.values())  # this variable will hold the count of total person detected overall
    animal_count = sum(frame_info_animal.values())  # this variable will hold the count of total elephants detected overall
    total_count = vehicle_count + person_count + animal_count

    frame_count_vehicle = len(frame_info_vehicle)  # this variable will hold the count of total frames in which vehicle was detected
    frame_count_person = len(frame_info_person)
    frame_count_animal = len(frame_info_animal)

    if frame_count != 0 and total_count > frame_count:
        detection_count = round(total_count / frame_count)
    else :
        detection_count = None
    if frame_count_vehicle != 0:
        avg_Batchcount_vehicle = round(vehicle_count / frame_count_vehicle)
    else :
        avg_Batchcount_vehicle = None
    if frame_count_animal != 0:
        avg_Batchcount_elephant = round(animal_count / frame_count_animal)
    else :
        avg_Batchcount_elephant = None
    if frame_count_person !=0:
        avg_Batchcount_person = round(person_count / frame_count_person)
    else :
        avg_Batchcount_person = None

    metaBatch = {
        "detect": (detection_count),
        "Frame_anomaly_score" : frame_anamoly_wgt,
        "count": {"people_count": (avg_Batchcount_person),
                  "vehicle_count": (avg_Batchcount_vehicle),
                  "ObjectCount" : (avg_Batchcount_elephant),
                  },
        "ids_to_be_monitored": ids_to_be_monitored,
        "cid": "str(detected_img_cid)",
        "object": "metaObj"

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
