import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import io
from fpdf import FPDF
from db_helper import get_patient_data,save_data,get_next_patient_id
from prediction import classify


def create_title_bar(pdf):
    
    pdf.set_font("Times", 'B', 35)
    pdf.set_text_color(255, 255, 255)
    title_text = 'Spine AI - Clinical Report'

    page_width = pdf.w - 2 * pdf.l_margin  

    pdf.set_fill_color(0, 0, 0)  
    pdf.cell(page_width, 15, title_text, ln=True, align='C', fill=True)
    


def add_datetime(pdf):
    
    pdf.set_text_color(0, 0, 0)  
    pdf.set_font("Arial", 'I', 10)

    page_width = pdf.w - 2 * pdf.l_margin 
    pdf.cell(page_width, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='R')
    pdf.cell(page_width, 10, f"Time: {datetime.now().strftime('%H:%M:%S')}", ln=True, align='R')

    
def fill_patient_info(pdf,report_data):
    
    pdf.set_font("Arial", 'B', 14)  
    pdf.cell(200, 10, 'Patient Information', ln=True, align='L')
    pdf.set_font("Arial", 'I', 12)  

    name = report_data.get("name", "N/A")
    age = report_data.get("age", "N/A")
    gender = report_data.get("gender", "N/A")

    pdf.cell(0, 10, f'Patient ID: {report_data["patient_id"]}', ln=True)
    pdf.cell(0, 10, f'Full Name: {name}', ln=True)
    pdf.cell(0, 10, f'Age: {age}', ln=True)
    pdf.cell(0, 10, f'Gender: {gender}', ln=True)

    pdf.ln(10)
    
    
def paste_image(pdf, category,ct_scan_image):

    page_width = pdf.w - 2 * pdf.l_margin
    image = Image.open(ct_scan_image)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(page_width, 10, 'CT Scan Image', ln=True, align='L')
    pdf.ln(10)

    image_path = 'ct_scan_image.png'
    image.save(image_path)

    img_width = 150
    img_height = 120  

    x_center = (pdf.w - img_width) / 2

    pdf.image(image_path, x=x_center, w=img_width, h=img_height)

    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)

    if category.lower() == 'severe':
        pdf.set_text_color(255, 0, 0)  
    elif category.lower() == 'moderate':
        pdf.set_text_color(255, 165, 0)  
    elif category.lower() == 'normal':
        pdf.set_text_color(0, 128, 0)  
    else:
        pdf.set_text_color(0, 0, 0)  

    severity_text = f'Severity: {category.capitalize()}'
    pdf.cell(page_width, 10, severity_text, ln=True, align='C')

    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    
def append_history(pdf,report_data):

    pdf.cell(200, 10, 'Medical History', ln=True, align='L')

    pdf.set_font("Arial", 'B', 12)  
    pdf.cell(50, 10, 'Date', border=1, align='C')
    pdf.cell(50, 10, 'Time', border=1, align='C')  
    pdf.cell(50, 10, 'Severity Level', border=1, align='C')  
    pdf.ln()

    severities = report_data.get("severity_history")
    severities = severities.split(',')
    history = []
    for i in severities:
        date,time,level = i.split(' ')
        history.append([date,time,level.capitalize()])
        
    i = 0
    history = history[::-1]

    while i < len(history) :
        pdf.set_font("Arial", '', 12)
        pdf.cell(50, 10, history[i][0], border=1, align='C') 
        pdf.cell(50, 10, history[i][1], border=1, align='C')  
        pdf.cell(50, 10, history[i][2], border=1, align='C')
        
        pdf.ln()
        
        i+=1
        
def add_content(pdf,severity_level):
    severity_level = severity_level.capitalize()  
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, 'Recommendations', ln=True)

    if severity_level == 'Severe':
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, ''' The condition is classified as severe, which indicates significant degeneration or other serious findings in the lumbar spine.\n It is strongly advised that the patient consult with a spine specialist as soon as possible for a comprehensive evaluation and possible surgical intervention.\n The risk of permanent damage to the spine increases in severe cases, so early intervention is crucial.''')

    elif severity_level == 'Moderate':
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, ''' The condition is classified as moderate, indicating moderate degeneration of the lumbar spine.\n While surgery may not be immediately necessary, lifestyle changes such as physical therapy, regular exercise, and proper posture are highly recommended.\n Follow-up consultations with a doctor or spine specialist will help to monitor progression and prevent further deterioration.''')

    elif severity_level == 'Mild':
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, ''' The condition is classified as mild, suggesting early-stage lumbar spine degeneration.\n It is important to maintain a healthy lifestyle with exercises that strengthen the core and improve flexibility.\n Avoid prolonged sitting or poor posture, and consider seeing a physical therapist for personalized exercises to prevent the condition from worsening.''')
    else:
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, ''' Severity level is undetermined. It is recommended to consult with a healthcare provider for further evaluation and diagnosis.''')
 
    pdf.ln(10)
    
    
def disclaimer(pdf):
    pdf.set_font("Arial", 'I', 10)  
    pdf.multi_cell(0, 10, '''\n*** This report is generated using AI-based tools. While every effort has been made to ensure accuracy, there may be occasional errors or inaccuracies. It is recommended to consult a healthcare professional for a comprehensive evaluation. ***''')


    
def generate_report(patient_id, ct_scan_image):
    patient_data = get_patient_data(patient_id)
    if not patient_data.empty:
        report_data = patient_data.iloc[0]

        pdf = FPDF()
        pdf.add_page()
        file_type = ct_scan_image.name.split('.')[-1].lower()
        severity_value = classify(ct_scan_image,file_type)
        
        create_title_bar(pdf)
        add_datetime(pdf)
        fill_patient_info(pdf, report_data)
        paste_image(pdf,severity_value,ct_scan_image)
        
        append_history(pdf,report_data)
        add_content(pdf,severity_level=severity_value)
        
        disclaimer(pdf)
            

        save_data(patient_id,severity=severity_value)
    
        pdf_file_path = 'patient_report.pdf'
        pdf.output(pdf_file_path)

        with open(pdf_file_path, 'rb') as f:
            pdf_output = io.BytesIO(f.read())

        st.download_button("Download Report as PDF", pdf_output, "patient_report.pdf", "application/pdf")
    else:
        st.error("No patient found with the provided ID.")


# st.title("Lumbar Spine Disease Report Generator")
# st.markdown("### Generate a professional report for lumbar spine disease")

# user_type = st.radio("Select User Type:", ["Old User", "New User"])

# if user_type == "Old User":
#     patient_id = st.text_input("Enter Patient ID:")
#     ct_scan_image = st.file_uploader("Upload Spine CT Scan Image", type=["dcm", "png", "jpg", "jpeg"])

#     if st.button("Generate Report"):
#         if ct_scan_image is not None:
#             image = Image.open(ct_scan_image)
#             generate_report(patient_id, ct_scan_image)
#         else:
#             st.error("Please upload a CT scan image.")
# else:
#     st.subheader("Enter New Patient Details")

#     next_patient_id = get_next_patient_id()  
#     st.markdown(f"**Generated Patient ID:** `{next_patient_id}`")

#     name = st.text_input("Full Name")
#     age = st.number_input("Age", min_value=1, max_value=120, step=1)
#     gender = st.selectbox("Gender", ["Male", "Female", "Other"])
#     ct_scan_image = st.file_uploader("Upload Spine CT Scan Image", type=["dcm", "png", "jpg", "jpeg"])

#     if st.button("Generate Report for New User"):
#         if name and age and gender and ct_scan_image:
#             image = Image.open(ct_scan_image)
            
#             # Classify image
#             file_type = ct_scan_image.name.split('.')[-1].lower()
#             severity = classify(ct_scan_image, file_type)

#             # Save new patient data
#             save_data(next_patient_id, name=name, age=age, gender=gender, severity=severity)

#             # Regenerate the report
#             generate_report(next_patient_id, ct_scan_image)
#         else:
#             st.error("Please fill all fields and upload an image.")