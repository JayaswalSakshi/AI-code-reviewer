import streamlit as st
import openai
import os
import google.generativeai as genai




from google.cloud import generativelanguage_v1beta2
from google.oauth2 import service_account
import json

# Page title
st.title("🤖 AI Text Generator using Google Gemini")

# Load credentials securely from Streamlit secrets
try:
    credentials_info = json.loads(st.secrets["google"]["credentials"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
except Exception as e:
    st.error("Failed to load Google API credentials. Check your Streamlit secrets.")
    st.stop()

# Initialize Google Gemini client
client = generativelanguage_v1beta2.TextServiceClient(credentials=credentials)

# Input text from the user
prompt = st.text_input("Enter a prompt for the AI model:", "Explain AI in simple terms")

# Button to trigger text generation
if st.button("Generate Text"):
    try:
        # Make a request to the Gemini API
        request = generativelanguage_v1beta2.GenerateTextRequest(
            model="models/text-bison-001",  # Replace with Google Gemini model name
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=100
        )
        response = client.generate_text(request=request)

        # Display the AI-generated response
        output = response.candidates[0].output
        st.success("Generated Text:")
        st.write(output)
    except Exception as e:
        st.error(f"An error occurred: {e}")
