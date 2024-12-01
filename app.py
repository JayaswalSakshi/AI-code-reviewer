import streamlit as st
import openai  # Ensure the OpenAI package is installed and the API key is set

# Configure your OpenAI API key
openai.api_key = "your-openai-api-key"

# Function to interact with OpenAI API
def review_code(code: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Python code reviewer."},
                {"role": "user", "content": f"Review this Python code:\n{code}"}
            ]
        )
        feedback = response['choices'][0]['message']['content']
        # Extract fixed code (if any) from feedback
        fixed_code = extract_fixed_code(feedback)
        return feedback, fixed_code
    except Exception as e:
        return f"Error: {str(e)}", ""

# Helper function to extract fixed code from feedback
def extract_fixed_code(feedback: str):
    if "```python" in feedback:
        return feedback.split("```python")[1].split("```")[0]
    return "No fixed code provided."

# Streamlit UI
st.title("GenAI Code Reviewer")
st.subheader("Submit your Python code for automated review and fixes.")

# Input box for user code
user_code = st.text_area("Paste your Python code here", height=300)

if st.button("Submit"):
    if user_code.strip():
        with st.spinner("Reviewing your code..."):
            feedback, fixed_code = review_code(user_code)
        st.subheader("Feedback")
        st.write(feedback)
        st.subheader("Fixed Code")
        st.code(fixed_code, language="python")
    else:
        st.warning("Please input Python code before submitting.")
