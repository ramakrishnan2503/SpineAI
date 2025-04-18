import sqlite3
import pandas as pd

def add_patient(patient_id, name, age, gender, severity_history):
    """
    Adds a new patient to the patients table.
    
    Parameters:
    - patient_id (str): Unique identifier for the patient.
    - name (str): Full name of the patient.
    - age (int): Age of the patient.
    - gender (str): Gender of the patient.
    - severeity_history (str): List of previous medical history
    
    Returns:
    - bool: True if insertion is successful, False otherwise.
    """
    
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO patients (
                patient_id, name, age, gender, severity_history
            )
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, name, age, gender, severity_history))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
        
    return success

def get_patient_data(patient_id):
    conn = sqlite3.connect('patients.db')  # Adjust the database name as necessary
    query = "SELECT * FROM patients WHERE patient_id = ?"
    patient_data = pd.read_sql(query, conn, params=(patient_id,))
    conn.close()
    return patient_data

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

