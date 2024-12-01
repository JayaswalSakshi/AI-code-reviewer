import streamlit as st
import subprocess
import os

# Helper function to analyze code using flake8
def analyze_code_with_flake8(code):
    try:
        # Write user code to a temporary file
        with open("temp_code.py", "w") as temp_file:
            temp_file.write(code)

        # Run flake8 on the temporary file
        result = subprocess.run(
            ["flake8", "temp_code.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Clean up temporary file
        os.remove("temp_code.py")

        # Return analysis result
        if result.stdout:
            return result.stdout
        else:
            return "No issues found. Your code looks good!"
    except Exception as e:
        return f"Error during analysis: {e}"

# Streamlit UI
st.title("GenAI Code Reviewer")
st.subheader("Submit Your Python Code")

# Input: Text area for code or file upload
user_code = st.text_area("Paste your Python code here:", height=300)

uploaded_file = st.file_uploader("Or upload a Python file", type="py")
if uploaded_file is not None:
    user_code = uploaded_file.read().decode("utf-8")
    st.text_area("Uploaded Code", user_code, height=300)

# Analyze Code Button
if st.button("Review Code"):
    if user_code.strip():
        st.info("Analyzing your code...")
        feedback = analyze_code_with_flake8(user_code)
        st.subheader("Feedback:")
        st.code(feedback, language="markdown")
    else:
        st.error("Please paste or upload code for analysis!")
