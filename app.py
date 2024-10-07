import streamlit as st
from chatbot import run_chatbot


user_query = st.text_input("Please enter your question:", "")
button = st.button("Submit")

if user_query and button:
    output = run_chatbot(user_query)
    st.write(output)
    
    
    