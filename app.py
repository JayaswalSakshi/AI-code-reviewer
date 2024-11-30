import streamlit as st
import openai
import os

# Set up Streamlit page configuration
st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")

# Load OpenAI API Key from secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# Application Title
st.title("🤖 AI Code Reviewer")
st.subheader("Submit your Python code for review and get suggestions!")

# Input box for Python code
code_input = st.text_area("Paste your Python code here:", height=300)

# Submit button
if st.button("Review Code"):
    if not code_input.strip():
        st.error("Please paste your Python code before submitting!")
    else:
        try:
            # Send code to OpenAI API for review
            with st.spinner("Analyzing your code..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Use the appropriate model
                    messages=[
                        {"role": "system", "content": "You are an expert Python code reviewer."},
                        {"role": "user", "content": f"Review this Python code:\n{code_input}"}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                review = response['choices'][0]['message']['content']

            # Display the review results
            st.success("Code Review Complete!")
            st.subheader("📝 Feedback and Suggestions:")
            st.markdown(review)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
