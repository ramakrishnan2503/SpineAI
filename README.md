# SpineAI

## Overview

**SpineAI** is a powerful application designed for detecting and classifying degenerative spine conditions using MRI data. Leveraging advanced computer vision and AI techniques, SpineAI aims to assist medical professionals in identifying spine-related issues more efficiently and accurately. 

While the core functionality revolves around medical image analysis, SpineAI also includes a specialized chatbot that helps users with spine-related information. The aim of this project is to develop a model for detecting and classifying degenerative spine conditions accurately.

## Core Features

### 1. Spine Image Classification
- **Description**: The app can classify images based on the type and severity of spine conditions.
- **How it Works**: Trained image classification models detect various conditions and categorize them, assisting doctors in quick decision-making.

### 2. Medical Report Generation
- **Description**: SpineAI generates detailed medical reports based on the MRI image analysis, including detected conditions and recommended next steps.
- **How it Works**: The AI processes the results of the image analysis and formats them into an easy-to-understand report for both medical professionals and patients.

### 3. Spine-Related Chatbot
- **Description**: A specialized chatbot that answers questions related to spine conditions, treatments, and other related topics.
- **How it Works**: The chatbot uses a specialized knowledge base and responds only to spine-related queries. It maintains conversation context using `ConversationBufferWindowMemory` to enhance user experience.
  

## Setup

### 1. Clone the Repository
```bash
  https://github.com/ramakrishnan2503/SpineAI.git
```

### 2. Install Dependencies
```bash
  pip install -r requirements.txt
```

### 3. Run the Application
```bash
  python app.py
```


### Technologies Used
  Deep Learning: For MRI image classification and condition detection.
  
  Python: Backend development.
  
  LangChain: For the chatbot and memory functionality.
  
  Groq API: Integration for using advanced LLMs (Large Language Models).
  
  Streamlit: For building a user interface
