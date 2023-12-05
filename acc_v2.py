import json
import xmltodict
import pandas as pd
import boto3
from xml.etree import ElementTree as ET
import multiprocessing
from io import StringIO
from datetime import datetime
from multiprocessing import Manager
from concurrent.futures import ThreadPoolExecutor
from config import *

manager = Manager()

concated_dataframe = manager.list()

# s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# json_file_path='Untitled Folder/data.json'
package_file_path ='Untitled Folder/der2_sRefset_SNOMEDtoMedDRASimpleMapSnapshot_INT_20230131.txt'
csv_file_path ='mdhier.xlsx'

# Define a Pydantic model for the request body
bucket_name= 'wwsdf-raw-data-dev'
def s3_connector():
    s3_client = boto3.client('s3')
    return s3_client
class submitted_files:
    def __init__(self):
        self.s3_client = s3_connector()
        self.extracted_codes=[]
    def load_xml(self,file_path):
        try:
            self.file_path=file_path
            s3_client=s3_connector()
            #Create a file object using the bucket and object key. 
            fileobj = s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                ) 
            # open the file object and read it into the variable filedata. 
            body = fileobj['Body']
            data_dict = xmltodict.parse(body.read(),encoding='utf-8')
            self.file_code=self.file_path.split('/')[-1].split('_')[0]
            return data_dict
        except Exception as e:
            print(f"Error loading XML file: {e}")

    def check_keys_in_nested_dict(self,keys, dictionary):
        if isinstance(dictionary, dict):
            if all(key in dictionary.keys() for key in keys):
                self.extracted_codes.append(int(dictionary['value']['@code']))
                return dictionary
            for value in dictionary.values():
                if type(value) == dict:
                    self.check_keys_in_nested_dict(keys, value)
                if type(value)==list:
                    for i in value:
                        self.check_keys_in_nested_dict(keys, i)
        if type(dictionary)==list:
            for i in dictionary:
                self.check_keys_in_nested_dict(keys, i)
        return self.extracted_codes
    
    def report(self):
        return {'file_name':self.file_path,'file_code':self.file_code,'Meddra_codes':self.extracted_codes}

def final(file_path):
    codes=submitted_files()
    data_dict=codes.load_xml(file_path)
    mylist=['id','code','value','location']
    med_codes=codes.check_keys_in_nested_dict(mylist,data_dict)
    report=codes.report()
    return report

def submitted_batch(s3_location):
    s3_client=s3_connector()
    start=datetime.now()
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_location)
    files = response.get("Contents")
    xml_files=[file['Key'] for file in files if file['Key'].upper().endswith('XML')]
    # print(xml_files)
    # Create a pool of processes
    num_processes = 3
    # pool = multiprocessing.Pool(processes=num_processes)
    # Map the processing function to the list of files for parallel execution
    # output=pool.map(final,xml_files)
    with ThreadPoolExecutor(max_workers=num_processes) as executor:
        output=list(executor.map(final, xml_files))
    # pool.close()
    # pool.join()
    end=datetime.now()
    report=pd.DataFrame(output)
    csv_buffer = StringIO()
    report.to_csv(csv_buffer, index=False)
    key=f"{s3_location}output_csv/submitted_report_{datetime.now()}.csv"
    # print(key)
    # print(meddra_ouput.columns)
    s3_client.put_object(Bucket=bucket_name, Key= key, Body=csv_buffer.getvalue())
    return end-start,output
# ti,output=submitted_batch('submitted_files/')
# print(output)