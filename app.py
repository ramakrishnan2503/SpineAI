import streamlit as st
from chatbot import run_chatbot

def app():
    def display_chat_history(history):
        for chat in history:
            if chat['role'] == 'User':
                st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <img src="https://img.icons8.com/ios/50/000000/user-male-circle.png" 
                             alt="user-icon" width="30" height="30" style="margin-right: 10px;">
                        <div style="background-color: #DCF8C6; padding: 10px; border-radius: 10px; max-width: 70%; word-wrap: break-word;">
                            {chat['message']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <img src="https://img.icons8.com/ios/50/000000/robot.png" 
                             alt="bot-icon" width="30" height="30" style="margin-right: 10px;">
                        <div style="background-color: #ECECEC; padding: 10px; border-radius: 10px; max-width: 70%; word-wrap: break-word;">
                            {chat['message']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    display_chat_history(st.session_state.chat_history)

    user_query = st.text_input("Please enter your question:", "")
    button = st.button("Send")

    if button and user_query:
        st.session_state.chat_history.append({"role": "User", "message": user_query})
        
        with st.spinner("Bot is typing..."):
            bot_response = run_chatbot(user_query)
        
        st.session_state.chat_history.append({"role": "Bot", "message": bot_response})
        
        display_chat_history(st.session_state.chat_history)

if __name__ == "__main__":
    app()