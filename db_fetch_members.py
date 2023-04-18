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

def check_null(member_data):
    
    member_final_list = []
    for each in member_data:
        member = each['member']
        for item in member:
            if((item['memberId'] != None) and (item['faceCID'] != None) and (item['role'] != None)):
                member_final_list.append(each)
    
    return (member_final_list)

def fetch_db_mem():
    try:
        member_info = {}
        outt = []
        # connection = psycopg2.connect(host='216.48.182.5', database='postgres',port='5432',user='postgres',password='Happy@123')
        # connection = psycopg2.connect(host="216.48.182.5", database="postgres", port="8081", user="postgres", password="Happy@123")
        connection = psycopg2.connect(host=pg_url, database=pgdb, port=pgport, user=pguser, password=pgpassword)
        cursor=connection.cursor()
        
        query='''SELECT * FROM "Member";'''
        cursor.execute(query)
        
        # print("Selecting rows from device table using cursor.fetchall")
        device_records = cursor.fetchall()
        
        connection.commit()
        
        for row in device_records:
            # print(row[10])
            # print(row[11])
            # print(row[12])
            # print(row[13])
            # print(row[14])


            inn_dict = {}
            member_info={}
            
            member_info['id'] = row[0]
            member_info["member"] = []
            inn_dict['memberId'] = row[2]
            inn_dict['type'] = row[4]
            inn_dict['faceCID'] = row[28]
            inn_dict['role'] = row[3]
            member_info["member"].append(inn_dict)
            outt.append(member_info)

        output = check_null(outt)
        
        return output
    
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    
# device_data = fetch_db_mem()
# print(device_data)

# fetch_db_mem()