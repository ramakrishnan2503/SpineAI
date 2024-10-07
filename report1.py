import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from PIL import Image
import io
from fpdf import FPDF

# Connect to SQLite database
def get_patient_data(patient_id):
    conn = sqlite3.connect('patients.db')  # Adjust the database name as necessary
    query = "SELECT * FROM patients WHERE patient_id = ?"
    patient_data = pd.read_sql(query, conn, params=(patient_id,))
    conn.close()
    return patient_data

# Function to generate the report
def generate_report(patient_id, ct_scan_image):
    patient_data = get_patient_data(patient_id)
    if not patient_data.empty:
        report_data = patient_data.iloc[0]

        # Generate PDF report
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, 'Patient Report', ln=True, align='C')

        # Patient Info
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f'Patient ID: {report_data["patient_id"]}', ln=True)
        pdf.cell(0, 10, f'Full Patient Name: {report_data["name"]}', ln=True)
        pdf.cell(0, 10, f'Age: {report_data["age"]}', ln=True)
        pdf.cell(0, 10, f'Gender: {report_data["gender"]}', ln=True)

        # Disease Information
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Disease:', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, 'Lumbar Spine Disease', ln=True)

        # Medical History
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Relevant Medical History and Clinical Information:', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f'Allergies: {report_data["allergies"]}', ln=True)
        pdf.cell(0, 10, f'Current Medications: {report_data["medications"]}', ln=True)
        pdf.cell(0, 10, f'Recent Procedures: {report_data["recent_procedures"]}', ln=True)

        # Scan Details
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Scan Details:', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f'Date of the Scan: {datetime.now().strftime("%Y-%m-%d")}', ln=True)
        pdf.cell(0, 10, f'Time of the Scan: {datetime.now().strftime("%H:%M:%S")}', ln=True)

        # CT Scan Image
        pdf.cell(0, 10, 'CT Scan Image:', ln=True)
        # Save the image temporarily to display in PDF
        image_path = 'ct_scan_image.png'
        ct_scan_image.save(image_path)

        # Add image to PDF
        pdf.image(image_path, x=5, w=50)  # Adjust size as needed

        # Recommendations
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Assessment and Recommendations:', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, 'Interpretation of Findings: Normal', ln=True)
        pdf.cell(0, 10, 'Clinical Significance of Abnormalities: [Insert Clinical Significance]', ln=True)
        pdf.cell(0, 10, 'Recommendations for Further Imaging or Diagnostic Tests: [Insert Recommendations]', ln=True)
        pdf.cell(0, 10, 'Possible Treatment Options or Interventions: [Insert Treatment Options]', ln=True)

        # Signature
        pdf.cell(0, 10, '[Doctor\'s Name]', ln=True, align='R')
        pdf.cell(0, 10, '[Doctor\'s Title]', ln=True, align='R')
        pdf.cell(0, 10, datetime.now().date().strftime("%Y-%m-%d"), ln=True, align='R')

        # Save PDF to a temporary file
        pdf_file_path = 'patient_report.pdf'
        pdf.output(pdf_file_path)

        # Read the PDF file into BytesIO
        with open(pdf_file_path, 'rb') as f:
            pdf_output = io.BytesIO(f.read())

        # Provide download link
        st.download_button("Download Report as PDF", pdf_output, "patient_report.pdf", "application/pdf")
    else:
        st.error("No patient found with the provided ID.")

# Streamlit app layout
st.title("Lumbar Spine Disease Report Generator")

# Input field for Patient ID
patient_id = st.text_input("Enter Patient ID:")

# File uploader for CT scan image
ct_scan_image = st.file_uploader("Upload Spine CT Scan Image", type=["png", "jpg", "jpeg"])

# Button to generate report
if st.button("Generate Report"):
    if ct_scan_image is not None:
        image = Image.open(ct_scan_image)  # Load the uploaded image
        generate_report(patient_id, image)  # Call the report generation function
    else:
        st.error("Please upload a CT scan image.")
