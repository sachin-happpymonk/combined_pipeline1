import math
my_list =[[{'frame_id': 1, 'frame_anamoly_wgt': 0, 'detection_info': [], 'cid': None}, {'frame_id': 2, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmQcowh8Fy7uUPbcgnktX3ncp5qpQZmw7EqWhFajYm2mbA'}, {'frame_id': 3, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmQVYnHdF3z17htgbDgFUCjvNcv1x9cAYJ2AKa1SDTuQJc'}, {'frame_id': 4, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmaENXfzu1YDjHaRYPd9UvcBSFPXdN7gqeDfdFx5jdFW78'}, {'frame_id': 5, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmPm4yxWJSBeAn7YqeucVgQfF1cqvCQFZR3bHDz7wZvsjX'}, {'frame_id': 6, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmRgW7zBJoJjn7BiqYweCA7m37MWG231fLBNiivYdgsA99'}, {'frame_id': 7, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmPsJLcCvr4pyyyXoCWvXfotSN2fGrcQHbgb6YmtPCmFha'}, {'frame_id': 8, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmXK4M1YG2uGzZNvZ1jzsEuCZ8v24y4LKkha6hLexcCs3X'}, {'frame_id': 9, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmNjhpECoiRR2P2KenWodyM8AxniRCVWmgrLvTGaTdqrbK'}, {'frame_id': 10, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'Qmdo2G8JXwTXqzsZdzdzss7SNRqbYshVoEXfsEtiVCKuT1'}, {'frame_id': 11, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'Qmf3WYQEkYCe9nw547mHt8ZaSjrcwMfhTDAmJbt5TMbcHX'}, {'frame_id': 12, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmWR5ELvhDmhMxzkr4rEmpTgcFnx4RnF4iQpDW9gCacPoQ'}, {'frame_id': 13, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0, 'anamoly_score': None, 'activity_score': None}}, {6: {'type': 'Person', 'activity': 'Unknow', 'confidence': 0, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmSzmFP22ZFR2pUoAnHBBsSiCqXE7C9aKZwSWnF7HqibQu'}, {'frame_id': 14, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0, 'anamoly_score': None, 'activity_score': None}}, {6: {'type': 'Person', 'activity': 'Unknow', 'confidence': 0, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmQUjfTQ8dfFsKDh8th3zM2u7uTKQdL8B7SioVVdefYwGf'}, {'frame_id': 15, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmUgEBtcsVjsNyR1gqJDTHmJaehDY51RJVmFW8u2AC5cUY'}, {'frame_id': 16, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmYqeiP5nU4jwoa2A1btZJ1MoyQhRAJbuH75Lk3zKJKCzW'}, {'frame_id': 17, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmTomYsEibMvt1pFJK4es6LJNfCLCnmLsKydunsQDKp4bU'}, {'frame_id': 18, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmRy2uZB3cARomPJv1BqhXnWZrT28A55fedr12gVCzUAUL'}, {'frame_id': 19, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmXoiQGcPigpN2JbAWkxcgWucswb2FDJVXq3FmkMs5cwBu'}, {'frame_id': 20, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmZwNzhWT98MABsydYMu5bPA1r7aikjnEhJ3puYN8zHeNc'}, {'frame_id': 21, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmTUEmFWU6R2GQGRyCgJrHiG8K5RhhGKjHPE63hNbtfRRX'}, {'frame_id': 22, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmaSEFStdVRjYN7VK5QxbF8jMaCYce4ncCNRL2ZziYayMX'}, {'frame_id': 23, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmV6YJP9khXrn1ZksYaQmurWdPyEYgV1ff31Y1dafBYr63'}, {'frame_id': 24, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmXUhJzaRv91hppg2btV86DFVMmhZufNJRZQEFZMJEvr2d'}, {'frame_id': 25, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmWZfDwWHjuH8KnYJnzJfnkHFhS3kt72RjrzzWdY6wVN1p'}, {'frame_id': 26, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmbBjAfXmWodwNGLBttGvEzT41SjxW5XvLP7BCEWAFA1gA'}, {'frame_id': 27, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmcLCN3bpiZQpS6usFJ9AjUamvY4ckdiKQRahRSbuxTz5o'}, {'frame_id': 28, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmPR3ynMTWYAnU63Ua6adTPooCQUp5zy1qNofbeuNe1i1e'}, {'frame_id': 29, 'frame_anamoly_wgt': 0, 'detection_info': [{1: {'type': 'Vehicle', 'activity': '', 'confidence': 0.721361517906189, 'anamoly_score': None, 'activity_score': None}}, {2: {'type': 'Vehicle', 'activity': '', 'confidence': 0.6550610065460205, 'anamoly_score': None, 'activity_score': None}}, {3: {'type': 'Vehicle', 'activity': '', 'confidence': 0.5362839102745056, 'anamoly_score': None, 'activity_score': None}}], 'cid': 'QmW7z65iJGRCdfUDATod4BwzXxj6hd58y5eKaRQnjoUb1J'}]]


global id
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

    people_count_list =[]
    vehicle_count_list = []
    object_count_list = []
   
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
                    person += 1
                    person_counts[frame_id] = person
                    if cid not in person_ids:
                        person_ids.append(cid)
                    frame_cid[key]=person_ids
                    
                    
                    person_counts[frame_id] = person
                elif value['type'] == 'Vehicle':
                       vehicle +=1
                       vehicle_counts[frame_id] = vehicle
                       if cid not in vehicle_ids:
                           vehicle_ids.append(cid)
                           
                       
                       frame_cid[key]=vehicle_ids
                       
                elif value['type'] == 'Elephant':
                       object +=1
                       object_counts[frame_id] = object 
                       if cid not in object_ids:
                           object_ids.append(cid)
                           
                       
                       frame_cid[key]=object_ids  




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

    for x in my_list:
        for item in x:
            for detection in item['detection_info']:
                for key,values in detection.items():
                    detection_score = float(values.get('anamoly_score') or 0)
                    activity_score =  float(values.get('activity_score') or 0)
                    act_type = values.get('type')  
                    id = key  
                    if act_type == 'Person' and id not in people_count_list:
                        people_count_list.append(id)
                    if act_type == 'Vehicle' and id not in vehicle_count_list:
                        vehicle_count_list.append(id)
                    if act_type == 'Elephant' and id not in object_count_list:
                        object_count_list.append(id)
                    m = int(len(frame_cid[id]))
                    if m%2==0 and len(frame_cid[id])<2:
                        c_id = frame_cid[id][0]
                    if m%2==0 and len(frame_cid[id])>2:
                        i = int(m/2) + 1
                        c_id = frame_cid[id][i]
                    else:
                        i=int((m+1)/2)
                        c_id = frame_cid[id][i]                  
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
                                "cids": c_id
                            } 
                    temp_list.append(temp)            
    
    for obj in temp_list:          #this make sures that only unique entries are in metaObj
        if obj not in metaObj:
            metaObj.append(obj)
    for items in metaObj:
        items['detection_score']=sum(items['detection_score'])/len(items['detection_score'])
           
    
    
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

   
    metaBatch = {
        "detect": (count_all),
        "Frame_anomaly_score" : frame_anamoly_wgt,
        "count": {"people_count": (count_p),
                  "vehicle_count": (count_v),
                  "ObjectCount" : (count_o),
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

print(output_func(my_list))