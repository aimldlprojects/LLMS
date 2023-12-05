import json
import xmltodict
import pandas as pd
import boto3
from xml.etree import ElementTree as ET
import multiprocessing
from io import StringIO
from datetime import datetime
from config import *
bucket_name= 'wwsdf-raw-data-dev'

def s3_connector():
    s3_client = boto3.client('s3')
    return s3_client



def compare(file_path):
    s3_client=s3_connector()
    file_code=int(file_path.split('/')[-1].split('_')[0])
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='submitted_files/output_csv/submitted_report')
    sorted_objects = sorted(response.get('Contents', []), key=lambda x: x['LastModified'], reverse=True)
    fileobj = s3_client.get_object(
                    Bucket=bucket_name,
                    Key=sorted_objects[0]['Key']
                    ) 
                    # open the file object and read it into the variable filedata. 
    body = fileobj['Body']
    submitted_codes_file=pd.read_csv(body)
    fileobj = s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                ) 
            # open the file object and read it into the variable filedata. 
    body = fileobj['Body']
    processed_codes_file=pd.read_csv(body)
    processed_codes=processed_codes_file[processed_codes_file['Meddra_code']!='No Meddra Mapping Found/desc Found']['Meddra_code']
    submitted_codes_json=submitted_codes_file[submitted_codes_file['file_code']==file_code].reset_index(drop=True).head(1).to_dict(orient='index')[0]
    submitted_codes=submitted_codes_json['Meddra_codes'].replace('[','').replace(']','').split(',')
    submitted_file=submitted_codes_json['file_name']
    submitted_codes=[int(i) for i in submitted_codes]
    print(submitted_codes)
    print(processed_codes)
    if len(submitted_codes)>0 and len(processed_codes)>0:
        count_processed=len(set(processed_codes))
        count_submitted=len(set(submitted_codes))
        print(processed_codes[processed_codes.isin(submitted_codes)])
        matched_codes=len(set(processed_codes[processed_codes.isin(submitted_codes)]))
        return submitted_file,count_processed,count_submitted,matched_codes
    return None

# s3_client=s3_connector()
# print(compare(s3_client,'processed_files/output_csv/202201241784_MMM_E2B_20221018_8UWI3CEV_0000367547 (1).csv'))