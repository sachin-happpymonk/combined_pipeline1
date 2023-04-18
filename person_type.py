from io import BytesIO
import face_recognition 
import subprocess as sp
import cv2
from datetime import datetime  #datetime module to fetch current time when frame is detected
import numpy as np
from pytz import timezone 
from nanoid import generate

face_did_encoding_store = dict()
TOLERANCE = 0.70
batch_person_id = []
FRAME_THICKNESS = 3
FONT_THICKNESS = 2


def find_person_type(im0, datainfo):
    known_whitelist_faces = datainfo[0]
    known_blacklist_faces = datainfo[1]
    known_whitelist_id = datainfo[2]
    known_blacklist_id = datainfo[3]
    np_arg_src_list = known_whitelist_faces + known_blacklist_faces
    np_bytes2 = BytesIO()
    np.save(np_bytes2, im0, allow_pickle=True)
    np_bytes2 = np_bytes2.getvalue()
    
    

    image = im0 # if im0 does not work, try with im1
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    locations = face_recognition.face_locations(image)
    # print("locations",locations)
    #encodings = face_recognition.face_encodings(image, locations, model = "large")
    encodings = face_recognition.face_encodings(image,locations)
    #print(f', found {len(encodings)} face(s)\n')
    # print("encodings",encodings)
    did = "" 
    track_type = "100"
    if len(locations) != 0:
        if len(known_whitelist_faces) and len(known_blacklist_faces):
            for face_encoding ,face_location in zip(encodings, locations):
                faceids = face_recognition.face_distance(np_arg_src_list,face_encoding)
                print(np.argmin(faceids))
                if np.argmin(faceids) <=0.40:
                    # print(face_encoding ,face_location )
                    #print(np.shape(known_whitelist_faces), "known_whitelist_faces", np.shape(face_encoding),"face_encoding")
                    # print(known_whitelist_faces, face_encoding, TOLERANCE)
                    results_whitelist = face_recognition.compare_faces(known_whitelist_faces, face_encoding, TOLERANCE)
                    # print(results_whitelist)
                    faceids = face_recognition.face_distance(known_whitelist_faces,face_encoding)
                    # print(faceids)
                    
                    matchindex = np.argmin(faceids)

                    #print(results_whitelist, "611")
                    
                    if results_whitelist[matchindex]:
                    
                        did = '00'+ str(known_whitelist_id[matchindex])
                        #print(did, "did 613")
                        batch_person_id.append(did)
                            
                        track_type = "00"
                        ct = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f') # ct stores current time
                    
                        if did in face_did_encoding_store.keys():
                            face_did_encoding_store[did].append(face_encoding)
                            top_left = (face_location[3], face_location[0])
                            bottom_right = (face_location[1], face_location[2])
                            color = [0,255,0]
                            #cv2.rectangle(im0, top_left, bottom_right, color, FRAME_THICKNESS)
                            top_left = (face_location[3], face_location[2])
                            bottom_right = (face_location[1]+50, face_location[2] + 22)
                            #cv2.rectangle(im0, top_left, bottom_right, color, cv2.FILLED)
                            #cv2.putText(im0, did , (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), FONT_THICKNESS)
                            #Attendance(name)
                        else:
                            face_did_encoding_store[did] = list(face_encoding)
                            top_left = (face_location[3], face_location[0])
                            bottom_right = (face_location[1], face_location[2])
                            color = [0,255,0]
                            #cv2.rectangle(im0, top_left, bottom_right, color, FRAME_THICKNESS)
                            top_left = (face_location[3], face_location[2])
                            bottom_right = (face_location[1]+50, face_location[2] + 22)
                            #cv2.rectangle(im0, top_left, bottom_right, color, cv2.FILLED)
                            #cv2.putText(im0, did , (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), FONT_THICKNESS)
                            #Attendance(name)
                    else:
                        # if face_encoding not in known_blacklist_faces:
                            # # Serialization
                            # numpyData = {"array": image}
                            # encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
                            # #push to blacklist lmdb
                            # person_name = bytearray(name[0]+ str(count), "utf-8")
                            # person_img = bytearray(encodedNumpyData, "utf-8")
                            # with env.begin(write=True) as txn:
                            #     txn.put(person_name, person_img, db=known_db)
                            # known_blacklist_faces.append(face_encoding)
                            # known_blacklist_id.append("Blacklisted person")
                        # else:
                            results_blacklist = face_recognition.compare_faces(known_blacklist_faces, face_encoding, TOLERANCE)
                            faceids = face_recognition.face_distance(known_blacklist_faces,face_encoding)
                            matchindex = np.argmin(faceids)

                            
                            if results_blacklist[matchindex]:

                                did = '01'+ str(known_blacklist_id[matchindex])
                                #print("did 623", did)
                                batch_person_id.append(did)
                                track_type = "01"
                                ct = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f') # ct stores current time
                    
                                if did in face_did_encoding_store.keys():
                                    face_did_encoding_store[did].append(face_encoding)
                                    top_left = (face_location[3], face_location[0])
                                    bottom_right = (face_location[1], face_location[2])
                                    color = [0,255,0]
                                    #cv2.rectangle(im0, top_left, bottom_right, color, FRAME_THICKNESS)
                                    top_left = (face_location[3], face_location[2])
                                    bottom_right = (face_location[1]+50, face_location[2] + 22)
                                    #cv2.rectangle(im0, top_left, bottom_right, color, cv2.FILLED)
                                    #cv2.putText(im0, did , (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), FONT_THICKNESS)

                                else:
                                    face_did_encoding_store[did] = list(face_encoding)
                                    top_left = (face_location[3], face_location[0])
                                    bottom_right = (face_location[1], face_location[2])
                                    color = [0,255,0]
                                    #cv2.rectangle(im0, top_left, bottom_right, color, FRAME_THICKNESS)
                                    top_left = (face_location[3], face_location[2])
                                    bottom_right = (face_location[1]+50, face_location[2] + 22)
                                    #cv2.rectangle(im0, top_left, bottom_right, color, cv2.FILLED)
                                    #cv2.putText(im0, did , (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), FONT_THICKNESS)
                                    #Attendance(name)
                            else:
                                if len(face_did_encoding_store) == 0:
                                    did = '10'+ str(generate(size = 8 ))
                                    track_type = "10"
                                    batch_person_id.append(did)
                                    face_did_encoding_store[did] = list(face_encoding)
                                    top_left = (face_location[3], face_location[0])
                                    bottom_right = (face_location[1], face_location[2])
                                    color = [0,255,0]
                                    #cv2.rectangle(im0, top_left, bottom_right, color, FRAME_THICKNESS)
                                    top_left = (face_location[3], face_location[2])
                                    bottom_right = (face_location[1]+50, face_location[2] + 22)
                                    #cv2.rectangle(im0, top_left, bottom_right, color, cv2.FILLED)
                                    #cv2.putText(im0, did , (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), FONT_THICKNESS)
                                    #Attendance(name)
                                else:
                                    for key, value in face_did_encoding_store.items():
                                        if key.startswith('10'):
                                            try :
                                                results_unknown = face_recognition.compare_faces(np.transpose(np.array(value)), face_encoding, TOLERANCE)
                                                faceids = face_recognition.face_distance(np.transpose(np.array(value)),face_encoding)
                                                matchindex = np.argmin(faceids)

                                                if results_unknown[matchindex]:
                                                    key_list = list(key)
                                                    key_list[1] = '1'
                                                    key = str(key_list)
                                                    batch_person_id.append(key)
                                                    track_type = "11"
                                                    face_did_encoding_store[key].append(face_encoding)
                                                    top_left = (face_location[3], face_location[0])
                                                    bottom_right = (face_location[1], face_location[2])
                                                    color = [0,255,0]
                                                    #cv2.rectangle(im0, top_left, bottom_right, color, FRAME_THICKNESS)
                                                    top_left = (face_location[3], face_location[2])
                                                    bottom_right = (face_location[1]+50, face_location[2] + 22)
                                                    #cv2.rectangle(im0, top_left, bottom_right, color, cv2.FILLED)
                                                    #cv2.putText(im0, key , (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), FONT_THICKNESS)
                                                    #Attendance(name)
                                                else:
                                                    did = '10'+ str(generate(size=4))
                                                    batch_person_id.append(did)
                                                    face_did_encoding_store[did] = list(face_encoding)
                                                    top_left = (face_location[3], face_location[0])
                                                    bottom_right = (face_location[1], face_location[2])
                                                    color = [0,255,0]
                                                    #cv2.rectangle(im0, top_left, bottom_right, color, FRAME_THICKNESS)
                                                    top_left = (face_location[3], face_location[2])
                                                    bottom_right = (face_location[1]+50, face_location[2] + 22)
                                                    #cv2.rectangle(im0, top_left, bottom_right, color, cv2.FILLED)
                                                    #cv2.putText(im0, did , (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), FONT_THICKNESS)

                                            except np.AxisError as e:
                                                continue
    if track_type != "100":
        print("*****************************************")
        print("*****************************************")
        print("*****************************************")
        print(did,track_type)
        print("*****************************************")
        print("*****************************************")
        print("*****************************************")
        #open text file
        text_file = open("data.txt", "w")
        
        #write string to file
        text_file.write(did+' '+track_type)
        
        #close file
        text_file.close()
    #     cv2.imwrite(track_type+".jpg",im0)
    # cv2.imwrite("type.jpg",im0)

    return did,track_type
                    