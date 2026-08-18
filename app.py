import streamlit as st
from groq import Groq
import os

# 1. Page Configuration
st.set_page_config(page_title="Groq AI Chat", page_icon="🤖", layout="centered")
st.title("🤖 My Groq AI Assistant")

# 2. Initialize Groq Client 
# Securely gets the API key from your Mac environment variables, or falls back to a string
# Securely gets the key from Streamlit's hidden online vault
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Initialize Chat History in Browser Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Chat History on Screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display Groq AI response
    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b", # Change to your preferred model
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error connecting to Groq: {e}")
