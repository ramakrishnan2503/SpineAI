import numpy as np
import pydicom
import cv2
import streamlit as st
import joblib
import time
from tensorflow import keras
from app import app

# Load the CNN model
model = joblib.load(r'C:\Users\Ramakrishnan\Downloads\cnn.h5')

# Function to load and preprocess DICOM images
def load_dicom_image(file, img_size=(128, 128)):
    dicom = pydicom.dcmread(file)
    img = dicom.pixel_array
    img = img / np.max(img) if np.max(img) > 0 else img  # Normalize
    img_resized = cv2.resize(img, img_size)
    img_resized = np.stack((img_resized,) * 3, axis=-1)  # Convert to 3 channels
    return img_resized

# Function to load and preprocess standard images (JPEG/PNG)
def load_standard_image(file, img_size=(128, 128)):
    file_data = file.read()
    file_bytes = np.asarray(bytearray(file_data), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        st.error("Error decoding the image. Please upload a valid image file.")
        return None
    img_resized = cv2.resize(img, img_size)
    img_resized = img_resized / 255.0  # Normalize
    return img_resized

# General preprocessing function
def preprocess_image(file, file_type, img_size=(128, 128)):
    if file_type == "dcm":
        img = load_dicom_image(file, img_size)
    else:
        img = load_standard_image(file, img_size)
        if img is None:
            return None
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Function to get prediction label
def get_prediction_label(predicted_class):
    labels = {0: "normal", 1: "moderate", 2: "severe"}
    return labels.get(predicted_class, "Unknown")

# Set up the Streamlit app layout
st.set_page_config(page_title="Spine AI",page_icon="🩺", layout="wide")

# Typing animation for "Spine AI" on the Home page
def animated_title(text, delay=0.1):
    title_container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        title_container.markdown(f"<h1 style='text-align: center; color: #4A90E2;'>{displayed_text}</h1>", unsafe_allow_html=True)
        time.sleep(delay)

# Sidebar Navigation with Home as a default option
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

                st.image(original_img, caption="Uploaded Image", use_container_width=True)
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
    ###app()
    # Placeholder for chatbot implementation
    st.write("Chatbot coming soon! Here you’ll be able to interact with our AI for assistance on spine condition classifications and app usage.")

# Documentation Page Content
elif page == "Document Generation":
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📄 Spine AI - Document Generation</h1>", unsafe_allow_html=True)
    st.markdown("Coming Sooon!! Her you will be able to get personalized documents based on patient history")
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