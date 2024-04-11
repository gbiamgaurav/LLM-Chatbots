import os 
import streamlit as st 
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

st.set_page_config(
    page_title="Chat with your AI Assistant!",
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Setup google Gemini-Pro model
genai.configure (api_key = GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


# Funtion to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    

# Display input field for user to enter API key
GOOGLE_API_KEY = st.sidebar.text_input("Enter your Google API Key:", type="password")

# Setup google Gemini-Pro model
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("Please enter your Google API Key in the sidebar.")

# instantiate chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("Hi There!, I am your AI Assistant")


# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)


# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro....")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)