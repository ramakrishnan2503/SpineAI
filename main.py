import numpy as np
import streamlit as st
import joblib
from PIL import Image
import time
from tensorflow import keras
from app import app
from report import generate_report
from db_helper import save_data,get_next_patient_id


from prediction import *

model = joblib.load(r"D:\SpineAI\cnn.h5")



st.set_page_config(page_title="Spine AI",page_icon="🩺", layout="wide")

def animated_title(text, delay=0.1):
    title_container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        title_container.markdown(f"<h1 style='text-align: center; color: #4A90E2;'>{displayed_text}</h1>", unsafe_allow_html=True)
        time.sleep(delay)

st.sidebar.title("Navigation")

page = st.sidebar.selectbox("Choose a page:", ["Home", "Prediction", "Chatbot", "Document Generation"])

# Home Page Content
if page == "Home":
    animated_title("🩺 Spine AI", delay=0.15)
    st.markdown("<p style='text-align: center;'>Welcome to Spine AI, an AI powered application to help classify spine condition severity</p>", unsafe_allow_html=True)
    st.write("""
        ### About Spine AI
        Spine AI is a powerful tool for analyzing spinal condition severity from medical imaging. 
        It leverages Deep learning and Computer Vision models to provide accurate classifications.

        ### Features:
        - *Image Classification*: Upload an image(png/jpg/jpeg) to get a severity prediction for spine conditions.
        - *Interactive Chatbot*: Ask questions about spine conditions, image classification, and get personalized suggestions.
        - *Document Generation*: Get detailed information about the patient details and the history of the patient

        ### Usage
        1. Navigate to the *Prediction* section to upload images and get predictions.
        2. Use the *Chatbot* to ask questions and get quick personalized responses.
        3. Access the *Documentation* for detailed insights into the application.
    """)

# Prediction Page Content
elif page == "Prediction":
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🩺 Spine AI - Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload an image to classify spine condition severity.</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose an image file", type=['dcm', 'jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        st.subheader("File Uploaded Successfully")
        st.write("File Name:", uploaded_file.name)

        predict_button = st.button("🚀 Predict")
        if predict_button:
            img = preprocess_image(uploaded_file, file_type)
            
            if img is not None:
                pred = model.predict(img)
                predicted_class = np.argmax(pred, axis=1)[0]
                label = get_prediction_label(predicted_class)

                if file_type == "dcm":
                    original_img = load_dicom_image(uploaded_file)
                else:
                    uploaded_file.seek(0)
                    original_img = load_standard_image(uploaded_file)

                st.image(original_img, caption="Uploaded Image", use_column_width=True)
                if label == "severe":
                    st.markdown(f"<h2 style='text-align: center; color: #FF0000;'>Prediction: {label.capitalize()}</h2>", unsafe_allow_html=True)
                elif label == "normal":
                    st.markdown(f"<h2 style='text-align: center; color: #50C878;'>Prediction: {label.capitalize()}</h2>", unsafe_allow_html=True)
                elif label == "moderate":
                    st.markdown(f"<h2 style='text-align: center; color: #FFFF00;'>Prediction: {label.capitalize()}</h2>", unsafe_allow_html=True)
                   
            else:
                st.error("Unable to process the image file. Please ensure it's a valid format.")
    else:
        st.write("Please upload a DICOM or image file to classify.")

# Chatbot Page Content
elif page == "Chatbot":
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>💬 Spine AI - Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask any questions about spine conditions, image classification, and more!</p>", unsafe_allow_html=True)
    
    ### ************************** ###
    app()
    #st.write("Chatbot coming soon! Here you’ll be able to interact with our AI for assistance on spine condition classifications and app usage.")

# Documentation Page Content
elif page == "Document Generation":
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📄 Spine AI - Document Generation</h1>", unsafe_allow_html=True)
    
    st.title("Lumbar Spine Disease Report Generator")
    st.markdown("### Generate a professional report for your condition")

    user_type = st.radio("Select User Type:", ["Old User", "New User"])

    if user_type == "Old User":
        patient_id = st.text_input("Enter Patient ID:")
        ct_scan_image = st.file_uploader("Upload Spine CT Scan Image", type=["dcm", "png", "jpg", "jpeg"])

        if st.button("Generate Report"):
            if ct_scan_image is not None:
                image = Image.open(ct_scan_image)
                generate_report(patient_id, ct_scan_image)
            else:
                st.error("Please upload a CT scan image.")
    else:
        st.subheader("Enter New Patient Details")

        next_patient_id = get_next_patient_id()  
        st.markdown(f"**Generated Patient ID:** `{next_patient_id}`")

        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        ct_scan_image = st.file_uploader("Upload Spine CT Scan Image", type=["dcm", "png", "jpg", "jpeg"])

        if st.button("Generate Report for New User"):
            if name and age and gender and ct_scan_image:
                image = Image.open(ct_scan_image)
                
                # Classify image
                file_type = ct_scan_image.name.split('.')[-1].lower()
                severity = classify(ct_scan_image, file_type)

                # Save new patient data
                save_data(next_patient_id, name=name, age=age, gender=gender, severity=severity)

                # Regenerate the report
                generate_report(next_patient_id, ct_scan_image)
            else:
                st.error("Please fill all fields and upload an image.")
    #st.markdown("Coming Sooon!! Her you will be able to get personalized documents based on patient history")
    #st.write("""
    #    ## Documentation
    #    - *Model Information*: Our model uses Convolutional Neural Networks (CNN) to analyze and classify images.
    #    - *Preprocessing Techniques*: Images are resized and normalized for accurate prediction results.
    #    - *Prediction Labels*: Classification is based on three categories:
    #        - Normal
    #        - Moderate
    #        - Severe
    #    - *File Support*: Both DICOM and common image formats (JPEG, PNG) are supported.
    #""")
    #st.markdown("<p>For additional information, please contact our support team or refer to the model's technical documentation.</p>", unsafe_allow_html=True)