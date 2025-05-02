import sqlite3
from datetime import datetime
import pandas as pd

def add_patient(patient_id, name, age, gender, severity_history):
    """
    Adds a new patient to the patients table.
    
    Parameters:
    - patient_id (int): Unique identifier for the patient.
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
    conn = sqlite3.connect('patients.db') 
    query = "SELECT * FROM patients WHERE patient_id = ?"
    patient_data = pd.read_sql(query, conn, params=(patient_id,))
    conn.close()
    return patient_data

def fetch_patient_by_id(patient_id):
    """
    Fetches patient details by patient_id.
    
    Parameters:
    - patient_id (int): Unique identifier for the patient.
    
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

def save_data(patient_id, severity, name=None, age=None, gender=None):
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    entry = f"{date} {time} {severity}"

    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    if cursor.fetchone():
        cursor.execute("UPDATE patients SET severity_history = COALESCE(severity_history, '') || ',' || ? WHERE patient_id = ?", (entry, patient_id))
    else:
        cursor.execute("INSERT INTO patients (patient_id, name, age, gender, severity_history) VALUES (?, ?, ?, ?, ?)",
                       (patient_id, name, age, gender, entry))

    conn.commit()
    conn.close()
    

def get_next_patient_id():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(CAST(patient_id AS INTEGER)) FROM patients")
    max_id = cursor.fetchone()[0]
    conn.close()

    return str(int(max_id) + 1) if max_id else "1"

