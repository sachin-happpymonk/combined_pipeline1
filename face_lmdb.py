import lmdb
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
from json import JSONEncoder
from pathlib import Path
import glob
import os
path = os.getcwd()

env = lmdb.open(os.path.join(path,'lmdb/face-detection.lmdb'),
                max_dbs=10, map_size=int(100e9))


known_db = env.open_db(b'white_list')
unknown_db = env.open_db(b'black_list')



directory = os.path.join(path,"white_list")

for filename in os.listdir(directory):
    print(filename)
    name = filename.split('.')
    image_path = os.path.join(directory,filename)
    print(image_path)

    image  = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

    encodedNumpyData = cv2.imencode('.jpg', image)[1].tobytes()

    person_name = bytearray(name[0], "utf-8")
    person_img = encodedNumpyData
    with env.begin(write=True) as txn:
        txn.put(person_name, person_img, db=known_db)
     

directory = os.path.join(path,"black_list")
for filename in os.listdir(directory):
 
    print(filename)
    name = filename.split('.')
    image_path = os.path.join(directory,filename)
    print(image_path)

    image  = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

    encodedNumpyData = cv2.imencode('.jpg', image)[1].tobytes()

    person_name = bytearray(name[0], "utf-8")
    person_img = encodedNumpyData
    with env.begin(write=True) as txn:
        txn.put(person_name, person_img, db=unknown_db)
  