import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_groq import ChatGroq
from groq import Groq




# Retrieve API keys from environment variables
GOOGLE_API_KEY=os.getenv("GEMINI_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
CORRECT_PASSWORD =os.getenv("PASSWORD")  # Get passsword from environment

# Configure Gemini
client = Groq(

    api_key=GROQ_API_KEY,
)
genai.configure(api_key=GOOGLE_API_KEY)

# Set up Streamlit page configuration
st.set_page_config(page_title="LLM Chatbot", layout="wide")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def chat_with_gemini(prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response =model.generate_content(prompt)
    return response.text



# User selects the LLM
st.sidebar.title("Select LLM")
llm_option = st.sidebar.selectbox("Choose an LLM:", ["Gemini", "Llama", "Gemma", "Whisper", "Hugging Face"])

# Password Authentication
st.sidebar.title("Authentication")
password = st.sidebar.text_input("Password", type="password")

if password == CORRECT_PASSWORD:
    # Proceed with the chat functionality if password matches
    st.title("Chatbot Application")
    st.write("Select an LLM from the sidebar to start chatting.")

    # Input box for user message
    user_input = st.text_input(" ", placeholder="Type your message here...")

    # Submit button
    if st.button("Send"):
        if user_input:
            # Store user message
            st.session_state["messages"].append({"role": "user", "content": user_input})

            # Generate response based on selected LLM
            if llm_option == "Gemini":
                bot_response = chat_with_gemini(user_input)
            elif llm_option == "Llama":
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                )
                bot_response = chat_completion.choices[0].message.content
            elif llm_option == "Whisper":
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="whisper-large-v3-turbo",
                )
                bot_response = chat_completion.choices[0].message.content
            elif llm_option == "Gemma":
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="gemma2-9b-it",
                )
                bot_response = chat_completion.choices[0].message.content
            elif llm_option == "Hugging Face":
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="distil-whisper-large-v3-en",
                )
                bot_response = chat_completion.choices[0].message.content

            # Store bot response
            st.session_state["messages"].append({"role": "bot", "content": bot_response})

            # Display bot response
            st.write(bot_response)

    # Display conversation history
    if st.session_state["messages"]:
        for message in st.session_state["messages"]:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            elif message["role"] == "bot":
                st.markdown(f"**Bot:** {message['content']}")

else:
    st.error("Invalid password. Please try again.")
