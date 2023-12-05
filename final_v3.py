from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from xml.etree import ElementTree as ET
import pandas as pd
from fastapi.responses import FileResponse
import multiprocessing
from multiprocessing import Manager
from nltk.tokenize import sent_tokenize
from io import StringIO
import boto3
from datetime import datetime 
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import time
import xmltodict
import json
from botocore.exceptions import ClientError
import nltk
from config import *
nltk.download('punkt')


bucket_name= 'wwsdf-raw-data-dev'
# Define a Pydantic model for the request body

manager = Manager()
concated_dataframe = manager.list()
def s3_connector():
    s3_client = boto3.client('s3')
    return s3_client

 

class xml_functions:
    def __init__(self):
        self.s3_client=s3_connector()

 

    def load_xml_tree(self,file_path):
        try:
            #Create a file object using the bucket and object key.
            fileobj = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                )
            # open the file object and read it into the variable filedata.
            body = fileobj['Body'].read()
            self.tree = ET.ElementTree(ET.fromstring(body))
        except Exception as e:
            print(f"Error loading XML file: {e}")

    # def load_xml_dict(self,s3_client,file_path):
    #     try:
    #         #Create a file object using the bucket and object key.
    #         fileobj = s3_client.get_object(
    #             Bucket=bucket_name,
    #             IfMatch=file_path
    #             )
    #         # open the file object and read it into the variable filedata.
    #         body = fileobj['Body']
    #         data_dict = xmltodict.parse(body.read(),encoding='utf-8')
    #         return data_dict
    #     except Exception as e:
    #         print(f"Error loading XML file: {e}")
    #         raise e

 

    def get_xml_data(self,file_path):
        try:
            #Create a file object using the bucket and object key.
            fileobj = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                )
            # open the file object and read it into the variable filedata.
            body = fileobj['Body'].read()
            return body
        except Exception as e:
            print(f"Error loading XML file: {e}")

 

class submitted_coddes:
    def __init__(self):
        self.a=[]
    def load_xml(self,s3_client,file_path):
        try:
            #Create a file object using the bucket and object key.
            fileobj = s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                )
            # open the file object and read it into the variable filedata.
            body = fileobj['Body']
            data_dict = xmltodict.parse(body.read(),encoding='utf-8')
            return data_dict
        except Exception as e:
            print(f"Error loading XML file: {e}")

 

    def check_keys_in_nested_dict(self,keys, dictionary):
        if isinstance(dictionary, dict):
            if all(key in dictionary.keys() for key in keys):
                self.a.append(int(dictionary['value']['@code']))
                return dictionary
            for value in dictionary.values():
                if type(value) == dict:
                    self.check_keys_in_nested_dict(keys, value)
                if type(value)==list:
                    for i in value:
                        self.check_keys_in_nested_dict(keys, i)
        if type(dictionary)==list:
            for i in value:
                self.check_keys_in_nested_dict(keys, i)
        return self.a
    def run(self,s3_client,file_path):
        data_dict=self.load_xml(s3_client,file_path)
        mylist=['id','code','value','location']
        med_codes=self.check_keys_in_nested_dict(mylist,data_dict)
        return set(med_codes)

 

# s3_client = s3_connector()
# s=submitted_coddes()
# m=s.run(s3_client,'submitted_files/202201241784')
# print(m)
class extract_narrative:

 

    def __init__(self):
        self.s3_client = s3_connector()
        self.tree = None
    def load_xml(self,file_path):
        try:
            #Create a file object using the bucket and object key.
            fileobj = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                )
            # open the file object and read it into the variable filedata.
            body = fileobj['Body'].read()
            self.tree = ET.ElementTree(ET.fromstring(body))
        except Exception as e:
            print(f"Error loading XML file: {e}")

 

    def extract_case_narrative(self):
        if self.tree is not None:
            root = self.tree.getroot()
            for child in root.iter('narrativeincludeclinical'):  # Replace 'case_narrative' with your specific XML tag
                case_narrative=(child.text)
            return case_narrative
        else:
            print("XML not loaded. Call load_xml() first.")
            return "XML not loaded. Call load_xml() first."        

 

class xml_snomed_to_csv_meddra:

 

    def __init__(self,concated_dataframe):
        self.s3_client = s3_connector()
        self.tree = None
        self.package_file_path = 'der2_sRefset_SNOMEDtoMedDRASimpleMapSnapshot_INT_20230131.txt'
        self.csv_file_path = 'mdhier.xlsx'
        self.values=[]
        self.concated_dataframe = concated_dataframe

 

    def get_xml_data(self,file_path):
        try:
            #Create a file object using the bucket and object key.
            fileobj = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                )
            # open the file object and read it into the variable filedata.
            body = fileobj['Body'].read()
            return body
        except Exception as e:
            print(f"Error loading XML file: {e}")

 

    def load_xml(self,file_path):
        try:
            #Create a file object using the bucket and object key.
            fileobj = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                )
            # open the file object and read it into the variable filedata.
            body = fileobj['Body'].read()
            self.tree = ET.ElementTree(ET.fromstring(body))
        except Exception as e:
            print(f"Error loading XML file: {e}")

 

    def extract_case_narrative(self):
        if self.tree is not None:
            root = self.tree.getroot()
            for child in root.iter('narrativeincludeclinical'):  # Replace 'case_narrative' with your specific XML tag
                case_narrative=(child.text)
            return case_narrative
        else:
            print("XML not loaded. Call load_xml() first.")
            return None        

    def infer_snomedct(self):
        current_retry=1
        while current_retry<4:
            try:
                comprehend_medical = boto3.client('comprehendmedical',region_name='us-east-2')
                if len(self.case_narrative)<5000:
                    snomedct_concepts = comprehend_medical.infer_snomedct(Text=(self.case_narrative))
                else:
                    narratives=self.divide_into_chunks(self.case_narrative)
                    snomedct_concepts=[]
                    for case_narrative in narratives:
                        while current_retry<4:
                            try:
                                snomedct_concepts.append(comprehend_medical.infer_snomedct(Text=(case_narrative)))
                                break
                            except ClientError as e:
                                print(current_retry)
                                if e.response['Error']['Code'] == 'TooManyRequestsException':
                                    current_retry += 1
                                    wait_time = current_retry  
                                    time.sleep(wait_time)
                                else:
                                    raise e
                return snomedct_concepts
            except ClientError as e:
                print(current_retry)
                if e.response['Error']['Code'] == 'TooManyRequestsException':
                    current_retry += 1
                    wait_time =current_retry  # Exponential backoff
                    time.sleep(wait_time)
                else:
                    raise e
    def load_packages(self):
        try:
            self.data = pd.read_table(self.package_file_path)
            self.meddra_data = pd.read_excel(self.csv_file_path)
        except Exception as e:
            print(f"Error loading data: {e}")

 

    def get_meddra_codes(self, reference_ids):
        if self.data is not None:
            common_ids = set(reference_ids) & set(self.data['referencedComponentId'])
            if not common_ids:
                print(f"No common reference meddra codes found for {self.file_path}.")
                return None
            filtered_df = self.data[self.data['referencedComponentId'].isin(common_ids)][['referencedComponentId','mapTarget']].reset_index(drop=True)
            return filtered_df
        else:
            print("Data not loaded. Call load_packages() first.")
            return None

 

    def run(self,file_path,destination_path):
        self.destination_path=destination_path
        self.file_path=file_path
        global concated_dataframe
        # load xml file
        self.load_xml(file_path)
        # extract narrative from xml file
        self.case_narrative=self.extract_case_narrative()
        # load packages
        self.load_packages()
        # get snomed codes from aws infer_snomed service, output will be json
        json_data=self.infer_snomedct()
        # get all snomedctcconcepts codes and related data as list from json
        loc_snomed_codes = self.find_key_locations(json_data, 'SNOMEDCTConcepts')
        # make the list as dataframe
        snomed_codes = pd.DataFrame(loc_snomed_codes, columns=['Text','Type','Category','Description', 'referencedComponentId'])
        meddra_codes=self.get_meddra_codes(snomed_codes['referencedComponentId'])
        if meddra_codes is not None:
            meddra_codes = pd.merge(snomed_codes, meddra_codes, on='referencedComponentId', how='left')
            # meddra_codes['Location'] = meddra_codes['referencedComponentId'].map({v: k for k, v in loc_snomed_codes.items()})
            meddra_codes.to_csv('mapped_codes.csv')
            self.meddra_codes= meddra_codes
            meddra_desc=self.get_descriptions_by_meddra_ids()
            meddra_desc = meddra_desc.rename(columns={'pt_code': 'mapTarget'})
            if meddra_desc is not None:
                meddra_ouput = pd.merge(meddra_codes, meddra_desc, on='mapTarget', how='left')
                meddra_ouput=meddra_ouput.fillna('No Meddra Mapping Found/desc Found')
                meddra_ouput=meddra_ouput.rename(columns={'mapTarget':'Meddra_code','referencedComponentId':'Snomed_code'})
                # meddra_codes['mapTarget']=meddra_codes['mapTarget'].fillna('No Meddra Mapping Found')
                # meddra_ouput.to_csv(f"{str(self.destination_path).replace('.xml','')}.csv")
                csv_buffer = StringIO()
                meddra_ouput.to_csv(csv_buffer, index=False)
                meddra_ouput.to_csv('new.csv')
                key=f"output_csv/{str(file_path).replace('.xml','').replace('.XML','')}.csv"
                # print(meddra_ouput.columns)
                self.s3_client.put_object(Bucket=bucket_name, Key= destination_path, Body=csv_buffer.getvalue())
                self.concated_dataframe.extend(meddra_ouput.to_dict(orient='records'))
                # print(meddra_ouput[meddra_ouput['mapTarget']=='No Meddra Mapping Found/desc Found'])
                report=self.report(meddra_ouput)
                return report
            meddra_codes['mapTarget']=meddra_codes['mapTarget'].fillna('No Meddra Mapping Found')
            meddra_codes=meddra_codes.rename(columns={'mapTarget':'Meddra_code','referencedComponentId':'Snomed_code'})
            report=self.report(meddra_codes)
            return report
        snomed_codes=snomed_codes.rename(columns={'referencedComponentId':'Snomed_code'})
        report=self.report(snomed_codes)
        return report

 

    def find_key_locations(self,data, target_key, parent_key=None):
        locations = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    if parent_key is not None:
                       for i in value:
                            location = f"{parent_key}.{key}"
                            self.values.append([data['Text'],data['Type'],data['Category'],i['Description'],int(i['Code'])])
                            locations.append(location)
                if isinstance(value, (dict, list)):
                    locations.extend(self.find_key_locations(value, target_key, parent_key=f"{parent_key}.{key}" if parent_key else key))
        elif isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    locations.extend(self.find_key_locations(item, target_key, parent_key=f"{parent_key}.{index}" if parent_key else f"[{index}]"))
        return self.values

 

    def get_descriptions_by_meddra_ids(self):
        reference_ids= self.meddra_codes['mapTarget']
        if self.meddra_data is not None:
            common_ids = set(reference_ids) & set(self.meddra_data['pt_code'])
            if not common_ids:
                print(f"No common reference meddra description found for {self.file_path}.")
                return None
            filtered_df = self.meddra_data[self.meddra_data['pt_code'].isin(common_ids)][['pt_code','pt_name','hlt_name','hlgt_name','soc_name','soc_abbrev']].reset_index(drop=True)
            return filtered_df
        else:
            print("Data not loaded. Call load_packages() first.")
            return None

    def divide_into_chunks(self,text):
    # Use NLTK's sentence tokenizer to split the text into sentences
        sentences = sent_tokenize(text)
        paragrapghs=[]
        para=''
        for i in sentences:
            if len(para+i)<5000:
                para=para+i
            else:
                paragrapghs.append(para)
                para=''
        return paragrapghs

    def report(self,final_codes):
        if len(final_codes)>0:
            no_of_processed_snomed_codes=[]
            no_of_processed_snomed_codes=final_codes[final_codes['Snomed_code']!='No Meddra Mapping Found/desc Found']
            no_of_processed_meddra_codes=[]
            if 'Meddra_code' in final_codes:
                no_of_processed_meddra_codes=final_codes[final_codes['Meddra_code']!='No Meddra Mapping Found/desc Found']
            return {'file_name':self.file_path,'snomed_codes':len(no_of_processed_snomed_codes),'meddra_codes':len(no_of_processed_meddra_codes),'percentage':len(no_of_processed_meddra_codes)/len(no_of_processed_snomed_codes)*100,'output_file':self.destination_path}
        return {'file_name':self.file_path,'snomed_codes':0,'meddra_codes':0,'percentage':100,'output_file':''}

 

def snomed_to_meddra(file_path,concated_dataframe,destination_path):
    try:
        s_m=xml_snomed_to_csv_meddra(concated_dataframe)
        destination_path=file_path.replace(destination_path,destination_path+'output_csv/').replace('.xml','').replace('.XML','')+'.csv'
        data = s_m.run(file_path,destination_path)
        return data
    except Exception as e:
        return {file_path:str(e)}

 

def snomed_meddra(s3_location, no_of_files=10, destination_path='output/',bucket_name=bucket_name):
    strt=datetime.now()
    s3_client = s3_connector()
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_location)
    files = response.get("Contents")
    xml_files=[file['Key'] for file in files if file['Key'].upper().endswith('.XML')][:no_of_files]
    print(xml_files)
    num_processes = 5
    # concated_dataframe = Manager().list()
    # pool = multiprocessing.Pool(processes=num_processes)
    # Map the processing function to the list of files for parallel execution
    # output=pool.map(snomed_to_meddra, xml_files)
    # output = pool.starmap(snomed_to_meddra, zip(xml_files, repeat(concated_dataframe),repeat(s3_location)))

 

    with ThreadPoolExecutor(max_workers = num_processes) as executor:
        output = list(executor.map(snomed_to_meddra, xml_files, repeat(concated_dataframe), repeat(s3_location)))
    # pool.close()
    # pool.join()
    final_dataframe = pd.DataFrame(list(concated_dataframe))
    csv_buffer = StringIO()
    final_dataframe.to_csv(csv_buffer, index=False)
    final_dataframe.to_csv('new.csv')
    key=f"{s3_location}output_csv/final_dataframe_{datetime.now()}.csv"
    # print(key)
    # print(meddra_ouput.columns)
    s3_client.put_object(Bucket=bucket_name, Key= key, Body=csv_buffer.getvalue())
    # print(final_dataframe)
    end=datetime.now()
    print(end-strt)
    print(output)
    key=f"{s3_location}output_csv/report_{datetime.now()}.json"
    print(key)
    total_snomed_codes = 0
    total_meddra_codes = 0
    converted_percentage=0
    batch_report= {}
    for entry in output:
        if type(entry)==dict and len(entry)>2:
            # print(entry)
            total_snomed_codes += entry["snomed_codes"]
            total_meddra_codes += entry["meddra_codes"]
    if total_snomed_codes !=0:
        converted_percentage=total_meddra_codes/total_snomed_codes*100
    batch_report={"snomed_codes":total_snomed_codes,
                        "meddra_codes":total_meddra_codes,
                        "overall_percentage":converted_percentage,
                        "processed_files":len(output),
                        "data":output}

    s3_client.put_object(Bucket=bucket_name, Key= key, Body=json.dumps(batch_report))
    print("done")
    return "done"
# snomed_meddra('processed_files/')

 

def get_for_batch_percetage(bucket_name=bucket_name):
    s3_client = s3_connector()
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='output_csv/final_dataframe')
    sorted_objects = sorted(response.get('Contents', []), key=lambda x: x['LastModified'], reverse=True)
    report=[]
    for file in sorted_objects:
        fileobj = s3_client.get_object(
                    Bucket=bucket_name,
                    Key=file['Key']
                    )
                    # open the file object and read it into the variable filedata.
        validating = pd.read_csv(fileobj['Body'])
        no_of_processed_snomed_codes=validating[validating['Snomed_code']!='No Meddra Mapping Found/desc Found']
        no_of_processed_meddra_codes=validating[validating['Meddra_code']!='No Meddra Mapping Found/desc Found']
        report.append({'file_name':file['Key'],'snomed_codes':len(no_of_processed_snomed_codes),'meddra_codes':len(no_of_processed_meddra_codes)})
    return report
# print(get_for_batch_percetage())

 

# funnction to get converted codes csv from s3
def get_csv(file_path,bucket_name=bucket_name):
    s3_client = s3_connector()
    fileobj = s3_client.get_object(
                Bucket=bucket_name,
                Key=file_path
                )
    # open the file object and read it into the variable filedata.
    data = pd.read_csv(fileobj['Body'])
    return data
# print(get_csv('processed_files/output_csv/202201243077_MMM_E2B_20221019_5GQ42XM3_0000367625.csv'))

 

# get the latest report of analysis
def get_batch_report(folder_path,bucket_name=bucket_name):
    s3_client = s3_connector()
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path+'output_csv/report')
    print(response.get('Contents'))
    sorted_objects = sorted(response.get('Contents', []), key=lambda x: x['LastModified'], reverse=True)
    latest_report=sorted_objects[0]['Key']
    fileobj = s3_client.get_object(
                Bucket=bucket_name,
                Key=latest_report
                )
                # open the file object and read it into the variable filedata.
    json_data=fileobj['Body'].read().decode('utf-8')
    report = json.loads(json_data)
    return report
# get_batch_report()