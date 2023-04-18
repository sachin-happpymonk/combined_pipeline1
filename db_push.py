import psycopg2
from pytz import timezone 
from datetime import datetime
#.env vars loaded
import os
from os.path import join, dirname
from dotenv import load_dotenv
import ast

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

ack = False

def push_db(uri, device_id):
    try:
        
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(host=pg_url, database=pgdb, port=pgport, user=pguser, password=pgpassword)
        # connection = psycopg2.connect(host='216.48.182.5', database='postgres',port='5432',user='postgres',password='Happy@123')
        
        # Create a cursor object
        cursor=connection.cursor()
        
        # Define the update statement
        query='''UPDATE "DeviceMetaData" SET uri=%s WHERE "deviceId"=%s;'''
        
        print(uri)
        print(device_id)
        
        # Execute the update statement with the specified values
        cursor.execute(query, (uri, device_id))
        
        connection.commit()
        
        return ("Updated the uri column in device table")
            
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# uri = 'https://hls.ckdr.co.in/live/stream7/7.m3u8'
# device_id = '8f83cf90-ce4c-11ed-9bae-1d91dc06bb6b'
# push_db(uri, device_id)
# device_data = fetch_db()
# print(device_data)