import streamlit as st
import pdfplumber
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Now you can safely use your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI for the app
st.title("PDF-Based Question Answering System")

# File uploader for multiple PDF files
uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=['pdf'])
documents = []

# Extract text from uploaded PDF files using pdfplumber
if uploaded_files:
    for uploaded_file in uploaded_files:
        with pdfplumber.open(uploaded_file) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() or ""  # Append text from each page
            documents.append(full_text)
    if documents:
        st.success("PDFs processed successfully. You can now ask questions.")

# Text input for user to ask a question
question = st.text_input("Enter your question here:")

# Process the question against the extracted text
if question and documents:
    # Combine documents into a single text for simplicity in this example
    combined_text = "\n".join(documents[:3])  # Limiting to first 3 documents for performance
    
    # Set up the messages to send to the chat model
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question},
        {"role": "system", "content": combined_text}
    ]

    # Send the request to OpenAI's chat model
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Adjusted model name for chat capabilities
        messages=messages,
        max_tokens=500  # Adjusted max_tokens to potentially allow more room for the answer
    )

    # Display the answer
    st.write("Answer:", response.choices[0].message['content'])
