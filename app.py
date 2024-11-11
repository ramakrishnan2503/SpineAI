import streamlit as st
from chatbot import run_chatbot

def app():
    # Function to display chat history with icons
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

    # Initialize session state to store chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display conversation history
    #display_chat_history(st.session_state.chat_history)

    # User input for chatbot
    user_query = st.text_input("Please enter your question:", "")
    button = st.button("Send")

    if button and user_query:
        # Add user message to history
        st.session_state.chat_history.append({"role": "User", "message": user_query})
        
        with st.spinner("Bot is typing..."):
            # Get the bot response
            bot_response = run_chatbot(user_query)
        
        # Add bot response to history
        st.session_state.chat_history.append({"role": "Bot", "message": bot_response})
        
        # Display updated chat history
        display_chat_history(st.session_state.chat_history)

if __name__ == "__main__":
    app()