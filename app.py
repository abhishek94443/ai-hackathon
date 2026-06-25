import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Agentic Boilerplate", page_icon="🤖", layout="wide")

API_URL = "http://localhost:8000"

def main():
    st.title("Enterprise AI Agentic Application 🚀")

    # Initialize session state for chat history
    # Storing messages as simple dicts {"role": "...", "content": "..."}
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for configuration and file uploads
    with st.sidebar:
        st.header("Configuration & Data")
        st.info(
            "Welcome to the Enterprise AI Agent! 🤖\n\n"
            "This application uses specialized AI agents to help you "
            "analyze data, query databases, and read through your uploaded documents."
        )

        uploaded_file = st.file_uploader("Upload a document (PDF, TXT)", type=["pdf", "txt"])
        if uploaded_file and st.button("Process Document"):
            with st.spinner("Processing document..."):
                try:
                    # Send the file to FastAPI backend
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Document processed successfully."))
                    else:
                        st.error(f"Error processing document: {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {str(e)}")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat interface
    if prompt := st.chat_input("Ask a question or request an analysis..."):
        # User input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepare history, excluding the latest prompt
                    history = st.session_state.messages[:-1]
                    
                    payload = {
                        "messages": history,
                        "prompt": prompt
                    }
                    
                    print(f"\n>>> [Streamlit] Sending to FastAPI: {prompt}")
                    response = requests.post(f"{API_URL}/chat", json=payload)
                    
                    if response.status_code == 200:
                        assistant_response = response.json().get("response", "")
                        st.markdown(assistant_response)
                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    else:
                        st.error(f"API Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error connecting to backend: {str(e)}")

if __name__ == "__main__":
    main()
