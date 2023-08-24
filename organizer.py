import pandas as pd
import numpy as np

path = f"C:/Users/yy/Desktop/synthea/output/csv/"


def csv_reader(file_type,dict_id_patient):
    data = pd.read_csv(path+file_type+".csv")
    if file_type == 'patients':
        col_name = 'Id'
    else:
        col_name = 'PATIENT'
    data = data.replace({col_name: dict_id_patient})
    return data

def patient_id_init():
    patient_data = pd.read_csv(path+"patients.csv")
    num_patient = patient_data['Id'].nunique()
    list_patient = np.linspace(1,num_patient,num_patient)
    dict_id_patient = dict(zip(patient_data['Id'].unique(),list_patient))
    return dict_id_patient

def patient_careplan_matching(patient_data,careplan_data,dict_id_patient):
    total_merged = pd.DataFrame()
    for id in dict_id_patient.values(): 
        patient_line = patient_data.loc[patient_data.Id == id,["Id","BIRTHDATE","GENDER"]]
        careplan_line = careplan_data.loc[careplan_data.PATIENT == id,["PATIENT","START","STOP","CODE","DESCRIPTION"]]
        
        if len(careplan_data[careplan_data.PATIENT == id].values) != 0:
            merged = pd.merge(patient_line, careplan_line, left_on='Id',right_on="PATIENT", how='outer')
        else: 
            continue  

        merged = merged.fillna(0)
        total_merged = total_merged.append(merged)
    return total_merged
