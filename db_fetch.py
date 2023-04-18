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



def fetch_db():
    try:
        device_info = {}
        
        connection = psycopg2.connect(host=pg_url, database=pgdb, port=pgport, user=pguser, password=pgpassword)
        # connection = psycopg2.connect(host='216.48.182.5', database='postgres',port='5432',user='postgres',password='Happy@123')

        cursor=connection.cursor()
        
        query='''select dev.id,metadev.urn,metadev.ddns,metadev.ip,metadev.port,metadev."videoEncodingInformation",dev."remoteUsername",metadev.rtsp,dev."remoteDeviceSalt",feature."name",ge.latitude,ge.longitude
            from "Device" dev
            inner join "DeviceMetaData" metadev on dev."deviceId"= metadev."deviceId"
            inner join "Feature" feature on dev."deviceId"= feature."deviceId"
            inner join "Geo" ge on  ge."deviceMetaDataId" = metadev.id
            ;'''
        cursor.execute(query)
        
        print("Selecting rows from device table using cursor.fetchall")
        device_records = cursor.fetchall()
        # return(device_records)
        for row in device_records:
            # print(row)
            device_info[str(row[0])] = {}
            device_info[str(row[0])]["urn"] = row[1]
            device_info[str(row[0])]["ip"] = row[3]
            device_info[str(row[0])]["rtsp"] = row[7]
            device_info[str(row[0])]["username"] = row[6]
            device_info[str(row[0])]["password"] = row[8]
            device_info[str(row[0])]["ddns"] = row[2]
            device_info[str(row[0])]["videoEncodingInformation"] = row[5]
            device_info[str(row[0])]["port"] = int(row[4])
            device_info[str(row[0])]["subscriptions"] = row[9]
            device_info[str(row[0])]["lat"] = row[10]
            device_info[str(row[0])]["long"] = row[11]
    
        return(device_info)
            
        connection.commit()
    
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# device_data = fetch_db()
# print(device_data)