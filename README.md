# Agentic AI Boilerplate

A production-ready Python boilerplate for building highly capable AI applications using LangChain, LangGraph, Streamlit, ChromaDB, and DuckDB. Powered by Google's Gemini.

## Architecture

* **UI:** Streamlit
* **Orchestration:** LangGraph & LangChain Agents
* **LLM:** ChatGoogleGenerativeAI (Gemini)
* **Vector DB:** ChromaDB (for RAG)
* **Structured Data:** DuckDB (for structured queries and storage)
* **Structured Output:** Pydantic V2

## Setup Instructions

1. Ensure you have Python 3.10+ installed.
2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your Google API Key:
   ```
   GOOGLE_API_KEY=your_actual_key_here
   ```
5. **Start the Backend API:** In your terminal, run the FastAPI server:
   ```powershell
   uvicorn api.main:app --reload
   ```
6. **Start the Frontend UI:** Open a *new* terminal window, activate your virtual environment, and run Streamlit:
   ```powershell
   streamlit run app.py
   ```
