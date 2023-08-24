import organizer
import pandas as pd
import neo4j_driver as nd

if __name__ == '__main__':


    dict_id_patient = organizer.patient_id_init()
    patient_data = organizer.csv_reader('patients',dict_id_patient)
    careplan_data = organizer.csv_reader('careplans',dict_id_patient)
    
    conn = nd.Neo4jConnection("bolt://localhost:7687", "neo4j", "Tianjin951101")
    # conn.query('CREATE  (p:Patient)')

    patient_careplan = organizer.patient_careplan_matching(patient_data,careplan_data,dict_id_patient)
    

   
    conn.add_graph(patient_careplan)
    conn.close()