from fastapi import FastAPI
from final_v3 import *
from matching import *
from acc_v2 import *
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from xml.etree import ElementTree as ET
import pandas as pd
from fastapi.responses import FileResponse
import openpyxl
# import os
import json
import boto3
from config import *

class input(BaseModel) :
    file_path : str
    num : int

class xml_csv(BaseModel) :
    file_path : str

app=FastAPI()

app.add_middleware(
    CORSMiddleware,    allow_origins= ["*"],    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/analysed_docs')
def doc_analysis(details:input):
    exec=snomed_meddra(details.file_path)
    report=get_batch_report(details.file_path)
    return report

@app.post('/view_narrative')
def get_narrative(details:xml_csv):
    nar=extract_narrative()
    nar.load_xml(details.file_path)
    narrative=nar.extract_case_narrative()
    return narrative

@app.post('/xml')
def get_xml(details:xml_csv):
    nar=xml_functions()
    xml=nar.get_xml_data(details.file_path)
    return xml

@app.post('/output')
def get_output(details:xml_csv):
    data=get_csv(details.file_path)
    df_json = data.to_json(orient='records')
    return df_json

@app.post('/submitted_comparision')
def submitted_file(details:xml_csv):
    matching=submitted_batch('e2b/processed_xml_files/ArgusSubmittedFiles/')
    report=compare(details.file_path)
    return report

package_file_path ='./der2_sRefset_SNOMEDtoMedDRASimpleMapSnapshot_INT_20230131.txt'
csv_file_path ='./mdhier.xlsx'

# Define a Pydantic model for the request body
class XMLRequest(BaseModel):
    xml_data: str

class XMLDataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = None

    def load_xml(self):
        try:
            self.tree = ET.parse(self.file_path)
        except Exception as e:
            print(f"Error loading XML file: {e}")

    def extract_case_narrative(self):
        if self.tree is not None:
            root = self.tree.getroot()
            case_narratives = []
            for child in root.iter('narrativeincludeclinical'):  # Replace 'case_narrative' with your specific XML tag
                case_narratives.append(child.text)  
            return case_narratives
        else:
            print("XML not loaded. Call load_xml() first.")
            return None


class DataFilter:
    
    def __init__(self,case_narrative):
        self.package_file_path = './der2_sRefset_SNOMEDtoMedDRASimpleMapSnapshot_INT_20230131.txt'
        self.case_narrative = case_narrative
        self.csv_file_path = './mdhier.xlsx'
        self.data = None
        self.values=[]
        self.load_data()

    def infer_snomedct(self):
        comprehend_medical = boto3.client('comprehendmedical',region_name='us-east-2')
        print(comprehend_medical)
        snomedct_concepts = comprehend_medical.infer_snomedct(Text=(self.case_narrative))
        return snomedct_concepts

    def load_data(self):
        try:
            self.data = pd.read_table(self.package_file_path)
            self.meddra_data = pd.read_excel(self.csv_file_path)
        except Exception as e:
            print(f"Error loading data: {e}")

    def filter_by_reference_ids(self, reference_ids):
        if self.data is not None:
            common_ids = set(reference_ids) & set(self.data['referencedComponentId'])
            if not common_ids:
                print("No common reference IDs found.")
                return None
            filtered_df = self.data[self.data['referencedComponentId'].isin(common_ids)][['referencedComponentId','mapTarget']].reset_index(drop=True)
            return filtered_df
        else:
            print("Data not loaded. Call load_data() first.")
            return None

    def map_snomed_to_medra(self):
        self.load_data()
        json_data=self.infer_snomedct()
        loc_snomed_codes = self.find_key_locations(json_data, 'SNOMEDCTConcepts')
        snomed_codes = pd.DataFrame(loc_snomed_codes, columns=['Text','Type','Category','Description', 'referencedComponentId'])
        meddra_codes=self.filter_by_reference_ids(snomed_codes['referencedComponentId'])
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
                meddra_codes['mapTarget']=meddra_codes['mapTarget'].fillna('No Meddra Mapping Found')
                meddra_ouput = meddra_ouput.rename(columns={'referencedComponentId': 'Snomed_Code','mapTarget':'MedDRA_Code'})
                return meddra_ouput
            meddra_codes['mapTarget']=meddra_codes['mapTarget'].fillna('No Meddra Mapping Found')
        return snomed_codes

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
                print("No common reference IDs found.")
                return None
            filtered_df = self.meddra_data[self.meddra_data['pt_code'].isin(common_ids)][['pt_code','pt_name','hlt_name','hlgt_name','soc_name','soc_abbrev']].reset_index(drop=True)
            # filtered_df.to_csv('map_codes.csv')
            # df = pd.concat( map(pd.read_csv, ['mapped_codes.csv', 'map_codes.csv']), ignore_index=True) 
            # df.to_csv('output.csv') 
            return filtered_df
        else:
            print("Data not loaded. Call load_data() first.")
            return None

@app.post("/upload-xml")
async def upload_xml(file: UploadFile):
    # Save a copy of the uploaded XML as "xml_data.xml"
    with open("xml_data.xml", "wb") as config_file:
        data = config_file.write(file.file.read())
    xml_extractor = XMLDataExtractor('xml_data.xml')
    xml_extractor.load_xml()
    case_narratives = xml_extractor.extract_case_narrative()
    narratives = []
    if case_narratives is not None:
        for narrative in case_narratives:
            narratives.append(narrative)
    return narratives

@app.get("/snomed-to-meddra")
async def snomed_to_meddra(case_narative:str):
    # Replace with your JSON file path
    # json_file_path = 'C:/Users/Lenovo/Desktop/nithin_ibm_workspace/serverend/data.json'
    # json_data = json.load(open(json_file_path, 'r'))
    s_m = DataFilter(case_narative)
    data = s_m.map_snomed_to_medra()
    json_data = data.to_json(orient='records')
    return json_data

