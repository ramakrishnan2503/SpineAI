# db_helper.py

import sqlite3

def add_patient(patient_id, name, age, gender, disease, medical_history, allergies, medications, recent_procedures):
    """
    Adds a new patient to the patients table.
    
    Parameters:
    - patient_id (str): Unique identifier for the patient.
    - name (str): Full name of the patient.
    - age (int): Age of the patient.
    - gender (str): Gender of the patient.
    - disease (str): Diagnosed lumbar spine disease.
    - medical_history (str): Relevant medical history.
    - allergies (str): Known allergies.
    - medications (str): Current medications.
    - recent_procedures (str): Recent medical procedures.
    
    Returns:
    - bool: True if insertion is successful, False otherwise.
    """
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO patients (
                patient_id, name, age, gender, disease, medical_history, 
                allergies, medications, recent_procedures
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient_id, name, age, gender, disease, medical_history, allergies, medications, recent_procedures))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # This exception is raised if the patient_id already exists
        success = False
    finally:
        conn.close()
    return success

def fetch_patient_by_id(patient_id):
    """
    Fetches patient details by patient_id.
    
    Parameters:
    - patient_id (str): Unique identifier for the patient.
    
    Returns:
    - tuple or None: Patient details if found, else None.
    """
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
    patient = c.fetchone()
    conn.close()
    return patient

def fetch_all_patients():
    """
    Fetches all patient records.
    
    Returns:
    - list of tuples: All patient records.
    """
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients')
    patients = c.fetchall()
    conn.close()
    return patients

