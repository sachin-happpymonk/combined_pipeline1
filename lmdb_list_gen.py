import numpy as np
import cv2 as cv
import lmdb
from io import BytesIO
import io
from PIL import Image
import face_recognition 


known_blacklist_faces = []
known_blacklist_id = []
known_whitelist_faces = []
known_whitelist_id = []




#load lmdb
env = lmdb.open('./lmdb/face-detection.lmdb',
                max_dbs=10, map_size=int(100e9))


# Now create subdbs for known and unknown people.
known_db = env.open_db(b'white_list')
unknown_db = env.open_db(b'black_list')



def attendance_lmdb_known():
    # begin = time.time()
    known_whitelist_faces = []
    with env.begin() as txn:
        list1 = list(txn.cursor(db=known_db))
        
    db_count_whitelist = 0
    for key, value in list1:
        #fetch from lmdb
        with env.begin() as txn:
            re_image = txn.get(key, db=known_db)
            
            finalNumpyArray = np.array(Image.open(io.BytesIO(re_image))) 
            image = finalNumpyArray
            try :
                encoding = face_recognition.face_encodings(image)[0]
            except IndexError as e  :
                continue
            known_whitelist_faces.append(encoding)
            known_whitelist_id.append(key.decode())
            db_count_whitelist += 1
            
    # end = time.time()

    # print(f"Total runtime of the program is {end - begin}")
    # print(known_whitelist_faces)
    print(db_count_whitelist, "total whitelist person")
    return known_whitelist_faces, known_whitelist_id



def attendance_lmdb_unknown():
    # begin = time.time()
    known_blacklist_faces = []
    with env.begin() as txn:
        list1 = list(txn.cursor(db=unknown_db))
        
    db_count_blacklist = 0
    for key, value in list1:
        #fetch from lmdb
        with env.begin() as txn:
            re_image = txn.get(key, db=unknown_db)
            
            finalNumpyArray = np.array(Image.open(io.BytesIO(re_image))) 
            image = finalNumpyArray
            try :
                encoding = face_recognition.face_encodings(image)[0]
            except IndexError as e  :
                continue
            known_blacklist_faces.append(encoding)
            known_blacklist_id.append(key.decode())
            db_count_blacklist += 1
            
    # end = time.time()
    # print(known_blacklist_faces)
    # print(f"Total runtime of the program is {end - begin}")
    print(db_count_blacklist, "total blacklist person")
    return known_blacklist_faces,known_blacklist_id
