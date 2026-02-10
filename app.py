import streamlit as st
import google.generativeai as genai
import json
import os

# 1. Setup API Key (Uses Streamlit Secrets for Deployment)
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. Load your memories
with open("memories.json", "r") as f:
    memories = json.load(f)

# 3. Define the System Persona
system_instruction = f"""
You are a warm, loving Memory Bot for Bhavya and {memories['boyfriend']}. 
Use these facts to answer questions: {json.dumps(memories)}.
Tone: Playful, romantic, and helpful. If asked about something not in memories, 
use your general knowledge but keep the loving tone.
"""

# Use Gemini 3 Flash for the best 2026 performance
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    system_instruction=system_instruction
)

st.title("💖 Our Love Story Bot")

# Initialize Chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display Messages
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User Input
if prompt := st.chat_input("Ask me about us..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = st.session_state.chat.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)