import pandas as pd
import extractor_parameter
import numpy as np
from datetime import datetime
import json


def calculate_age(current_timestamp_str, birthday_str):
    current_timestamp = datetime.strptime(current_timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
    birthday = datetime.strptime(birthday_str, "%d/%m/%Y")
    age_difference = current_timestamp - birthday
    return age_difference.days

def read_EHR_file(path, file_type): 
    file = file_type + '.csv'
    df = pd.read_csv(path+file)
    df = df[extractor_parameter.files_colomn[file]]
    df = df.drop_duplicates()
    return df


def write_dict_patient(encounter_dict,patient_df,patient_id):
    patient_info = patient_df[patient_df['PATIENT'] == patient_id]
    encounter_dict['patient'] = {'id': patient_id, 'birthday': patient_info.iloc[0]['BIRTHDATE'], 'race': patient_info.iloc[0]['RACE'], 
                                 'gender': patient_info.iloc[0]['GENDER']}
    return encounter_dict

def write_dict_encounter(encounter_dict,encounter_df,encounter_id):
    encounter_info = encounter_df[encounter_df['ENCOUNTER'] == encounter_id]
    encounter_dict['encounter'] = {'start': encounter_info.iloc[0]['START'],'id': encounter_id, 'code': encounter_info.iloc[0]['CODE'],
                                    'descriprion': encounter_info.iloc[0]['DESCRIPTION'],
                                    'reason code': encounter_info.iloc[0]['REASONCODE'], 
                                    'reason description': encounter_info.iloc[0]['REASONDESCRIPTION']}
    encounter_dict['encounter']['age(days)'] = calculate_age(encounter_dict['encounter']['start'], encounter_dict['patient']['birthday'])
    return encounter_dict

def write_dict_condition(encounter_dict,condition_df,encounter_id):
    if not condition_df[condition_df['ENCOUNTER'] == encounter_id].empty :
        condition_info = condition_df[condition_df['ENCOUNTER'] == encounter_id]
        encounter_dict['condition'] = {'code': condition_info.iloc[:]['CODE'].values.tolist(), 'descriprion': condition_info.iloc[:]['DESCRIPTION'].values.tolist()}
    return encounter_dict

def write_dict_careplan(encounter_dict,careplan_df,encounter_id):
    if not careplan_df[careplan_df['ENCOUNTER'] == encounter_id].empty : 
        careplan_info = careplan_df[careplan_df['ENCOUNTER'] == encounter_id]
        encounter_dict['careplan'] = {'code': careplan_info.iloc[:]['CODE'].values.tolist(), 'descriprion': careplan_info.iloc[:]['DESCRIPTION'].values.tolist(), 
        'reason code': careplan_info.iloc[:]['REASONCODE'].values.tolist(),'reason description': careplan_info.iloc[:]['REASONDESCRIPTION'].values.tolist()}
    return encounter_dict


def write_dict_observation(encounter_dict,observation_df,encounter_id):
    if not observation_df[observation_df['ENCOUNTER'] == encounter_id].empty : 
        observation_info = observation_df[observation_df['ENCOUNTER'] == encounter_id]
        encounter_dict['observation'] = {'descriprion': observation_info.iloc[:]['DESCRIPTION'].values.tolist(), 
        'value': observation_info.iloc[:]['VALUE'].values.tolist(),'unit': observation_info.iloc[:]['UNITS'].values.tolist()}
    return encounter_dict


def write_dict_allergy(encounter_dict,allergy_df,encounter_id):
    if not allergy_df[allergy_df['ENCOUNTER'] == encounter_id].empty : 
        allergy_info = allergy_df[allergy_df['ENCOUNTER'] == encounter_id]
        encounter_dict['allergy'] = {'code': allergy_info.iloc[:]['CODE'].values.tolist(),'system': allergy_info.iloc[:]['SYSTEM'].values.tolist(),
                                    'category': allergy_info.iloc[:]['CATEGORY'].values.tolist(), 
                                    'reaction code': allergy_info.iloc[:][['REACTION1','REACTION2']].values.tolist(),
                                    'reaction description': allergy_info.iloc[:][['DESCRIPTION1','DESCRIPTION2']].values.tolist(),
                                    'severity' : allergy_info.iloc[:][['SEVERITY1','SEVERITY2']].values.tolist()}            
    return encounter_dict     

def write_dict_img_study(encounter_dict,imaging_studies_df,encounter_id):      
    if not imaging_studies_df[imaging_studies_df['ENCOUNTER'] == encounter_id].empty : 
        img_info = imaging_studies_df[imaging_studies_df['ENCOUNTER'] == encounter_id]
        encounter_dict['img_study'] = {'body site code':img_info.iloc[:]['BODYSITE_CODE'].values.tolist(),'body site description': img_info.iloc[:]['BODYSITE_DESCRIPTION'].values.tolist(),
                                    'modality': img_info.iloc[:]['MODALITY_DESCRIPTION'].values.tolist(), 
                                    'procedure code': img_info.iloc[:]['PROCEDURE_CODE'].values.tolist()}
                                     
    return encounter_dict     
    

                                    
def write_dict_device(encounter_dict,device_df,encounter_id):
    if not device_df[device_df['ENCOUNTER'] == encounter_id].empty : 
        device_info = device_df[device_df['ENCOUNTER'] == encounter_id]
        encounter_dict['device'] = {'code':device_info.iloc[:]['CODE'].values.tolist(),
                                    'description': device_info.iloc[:]['DESCRIPTION'].values.tolist()}            
    return encounter_dict     


def write_dict_immu(encounter_dict,immunizations_df,encounter_id):
    if not immunizations_df[immunizations_df['ENCOUNTER'] == encounter_id].empty : 
        immu_info = immunizations_df[immunizations_df['ENCOUNTER'] == encounter_id]
        encounter_dict['immunization'] = {'code':immu_info.iloc[:]['CODE'].values.tolist(),
                                    'description': immu_info.iloc[:]['DESCRIPTION'].values.tolist()}    
    return encounter_dict     
    
def write_dict_medication(encounter_dict,medication_df,encounter_id):
    if not medication_df[medication_df['ENCOUNTER'] == encounter_id].empty : 
        med_info = medication_df[medication_df['ENCOUNTER'] == encounter_id]
        encounter_dict['medication'] = {'reason code':med_info.iloc[:]['REASONCODE'].values.tolist(),
                                    'description': med_info.iloc[:]['DESCRIPTION'].values.tolist(),
                                    'reason description': med_info.iloc[:]['REASONDESCRIPTION'].values.tolist()}    
    return encounter_dict     
    
def write_dict_claim(encounter_dict,claim_df,encounter_id):
    if not claim_df[claim_df['ENCOUNTER'] == encounter_id].empty : 
        claim_info = claim_df[claim_df['ENCOUNTER'] == encounter_id]
        encounter_dict['claim'] = {'diagnosis':claim_info.iloc[:][['DIAGNOSIS1','DIAGNOSIS2','DIAGNOSIS3','DIAGNOSIS4','DIAGNOSIS5','DIAGNOSIS6','DIAGNOSIS7','DIAGNOSIS8']].values.tolist()}    
    return encounter_dict     

if __name__ == '__main__':
    path = f"C:/Users/yy/Desktop/synthea/output/csv/"
    encounter_df =  read_EHR_file(path, 'encounters')
    claim_df =  read_EHR_file(path, 'claims')
    condition_df =  read_EHR_file(path, 'conditions')
    encounter_df =  read_EHR_file(path, 'encounters')
    careplan_df =  read_EHR_file(path, 'careplans')
    patient_df =  read_EHR_file(path, 'patients')
    observation_df =  read_EHR_file(path, 'observations')
    procedure_df =  read_EHR_file(path, 'procedures')
    allergy_df =  read_EHR_file(path, 'allergies')
    imaging_studies_df =  read_EHR_file(path, 'imaging_studies')
    supply_df =  read_EHR_file(path, 'supplies')
    immunizations_df =  read_EHR_file(path, 'immunizations')
    medication_df =  read_EHR_file(path, 'medications')
    device_df =  read_EHR_file(path, 'devices')


    list_patient = patient_df['PATIENT'].unique()
    count = 0
    for patient_id in list_patient:

        #patient_id = '136842c6-7272-867e-0777-c2fba764633a'
        list_encounter = list(encounter_df[encounter_df['PATIENT'] == patient_id]['ENCOUNTER'])
        #list_encounter =['10b3df77-7098-467f-5c7b-6654a53cf080']

        encounter_dict = {}

        for encounter_id in list_encounter:
            count+=1
            encounter_dict = write_dict_patient(encounter_dict,patient_df,patient_id)
            encounter_dict = write_dict_encounter(encounter_dict,encounter_df,encounter_id)
            encounter_dict = write_dict_condition(encounter_dict,condition_df,encounter_id)
            encounter_dict = write_dict_careplan(encounter_dict,careplan_df,encounter_id)
            encounter_dict = write_dict_observation(encounter_dict,observation_df,encounter_id)
            encounter_dict = write_dict_allergy(encounter_dict,allergy_df,encounter_id)
            encounter_dict = write_dict_img_study(encounter_dict,imaging_studies_df,encounter_id)
            encounter_dict = write_dict_device(encounter_dict,device_df,encounter_id)
            encounter_dict = write_dict_immu(encounter_dict,immunizations_df,encounter_id)
            encounter_dict = write_dict_medication(encounter_dict,medication_df,encounter_id)
            encounter_dict = write_dict_claim(encounter_dict,claim_df,encounter_id)
        
            with open("encounter/"+patient_id+"_"+encounter_id+".json", "a") as outfile:
                json.dump(encounter_dict, outfile)

            print(count)