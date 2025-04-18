import numpy as np
import pydicom
import cv2
import streamlit as st
import joblib
from tensorflow import keras

def load_dicom_image(file, img_size=(128, 128)):
    dicom = pydicom.dcmread(file)
    img = dicom.pixel_array
    img = img / np.max(img) if np.max(img) > 0 else img  
    img_resized = cv2.resize(img, img_size)
    img_resized = np.stack((img_resized,) * 3, axis=-1)  
    return img_resized

def load_standard_image(file, img_size=(128, 128)):
    file_data = file.read()
    file_bytes = np.asarray(bytearray(file_data), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        st.error("Error decoding the image. Please upload a valid image file.")
        return None
    img_resized = cv2.resize(img, img_size)
    img_resized = img_resized / 255.0  
    return img_resized

def preprocess_image(file, file_type, img_size=(128, 128)):
    if file_type == "dcm":
        img = load_dicom_image(file, img_size)
    else:
        img = load_standard_image(file, img_size)
        if img is None:
            return None
    img = np.expand_dims(img, axis=0)  
    return img

def get_prediction_label(predicted_class):
    labels = {0: "normal", 1: "moderate", 2: "severe"}
    return labels.get(predicted_class, "Unknown")


model = joblib.load("D:/SpineAI/cnn.h5")  

def classify(image_file, file_type):
    image_file.seek(0)

    preprocessed_img = preprocess_image(image_file, file_type)
    if preprocessed_img is None:
        return "Unknown"

    prediction = model.predict(preprocessed_img)
    predicted_class = np.argmax(prediction, axis=1)[0]
    label = get_prediction_label(predicted_class)
    return label


