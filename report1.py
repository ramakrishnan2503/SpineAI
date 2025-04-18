import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import io
from fpdf import FPDF
from db_helper import get_patient_data

def generate_report(patient_id, ct_scan_image):
    patient_data = get_patient_data(patient_id)
    if not patient_data.empty:
        report_data = patient_data.iloc[0]

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, 'Lumbar Spine Disease Report', ln=True, align='C')

        pdf.set_font("Arial", 'B', 14)
        pdf.ln(10) 
        pdf.cell(200, 10, 'Patient Information', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f'Patient ID: {report_data["patient_id"]}', ln=True)
        pdf.cell(0, 10, f'Full Name: {report_data["name"]}', ln=True)
        pdf.cell(0, 10, f'Age: {report_data["age"]}', ln=True)
        pdf.cell(0, 10, f'Gender: {report_data["gender"]}', ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, 'Disease Information', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, 'Condition: Lumbar Spine Disease', ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, 'Medical History', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f'Previous Severity levels: {report_data["severity_history"]}', ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, 'CT Scan Details', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f'Scan Date: {datetime.now().strftime("%Y-%m-%d")}', ln=True)
        pdf.cell(0, 10, f'Scan Time: {datetime.now().strftime("%H:%M:%S")}', ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, 'CT Scan Image', ln=True)
        image_path = 'ct_scan_image.png'
        ct_scan_image.save(image_path)
        pdf.image(image_path, x=10, w=150) 

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, 'Assessment and Recommendations', ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, 'Interpretation of Findings: Normal', ln=True)
        pdf.cell(0, 10, 'Clinical Significance: [Insert Clinical Significance]', ln=True)
        pdf.cell(0, 10, 'Further Imaging Recommendations: [Insert Recommendations]', ln=True)
        pdf.cell(0, 10, 'Treatment Options: [Insert Treatment Options]', ln=True)

        pdf.ln(10)
        pdf.cell(0, 10, 'Doctor\'s Signature:', ln=True, align='R')
        pdf.cell(0, 10, '[Doctor\'s Name]', ln=True, align='R')
        pdf.cell(0, 10, '[Doctor\'s Title]', ln=True, align='R')
        pdf.cell(0, 10, f'Date: {datetime.now().date().strftime("%Y-%m-%d")}', ln=True, align='R')

        pdf_file_path = 'patient_report.pdf'
        pdf.output(pdf_file_path)

        with open(pdf_file_path, 'rb') as f:
            pdf_output = io.BytesIO(f.read())

        #return pdf_output
        st.download_button("Download Report as PDF", pdf_output, "patient_report.pdf", "application/pdf")
    else:
        st.error("No patient found with the provided ID.")

st.title("Lumbar Spine Disease Report Generator")
st.markdown("### Generate a professional report for lumbar spine disease")

patient_id = st.text_input("Enter Patient ID:")

ct_scan_image = st.file_uploader("Upload Spine CT Scan Image", type=["png", "jpg", "jpeg"])

if st.button("Generate Report"):
    if ct_scan_image is not None:
        image = Image.open(ct_scan_image)  
        generate_report(patient_id, image) 
    else:
        st.error("Please upload a CT scan image.")
