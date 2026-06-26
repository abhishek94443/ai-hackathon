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

## Project Roadmap: Manufacturing Quality Defect Analyzer

This boilerplate is currently being transformed into an **AI-driven tool that generates data-driven hypotheses and explanatory reports** to accelerate manufacturing defect resolution.

### 1. Problem Statement
Manufactures frequently encounter quality defects but identifying the root causes is often slow and inefficient. This project aims to replace manual data correlation and expert brainstorming with an AI assistant that automatically analyzes defect patterns across:
- **Production Parameters:** Machine settings, batch info
- **Environmental Conditions:** Humidity, temperature
- **Defect Logs:** Timestamps, types, severity

### 2. Planned Features & Architecture
To achieve this, the following architecture and feature updates are planned:

#### Frontend Dashboard (Streamlit)
- **Interactive Data Filtering:** Users will be able to filter data by time range, machine ID, batch number, and defect type via a sidebar.
- **Data Visualizations:** Dynamic charts visualizing defect rates correlated with production and environmental metrics.
- **Hypothesis Validation UI:** A dedicated section displaying AI-ranked root cause hypotheses (with confidence scores), allowing engineers to validate or reject them.
- **Reporting:** 1-click comprehensive analysis report generation.

#### Data Models & Schemas (Pydantic)
- **`RootCauseHypothesis`:** Structured output capturing the hypothesis rank, description, confidence score, supporting evidence, and recommended corrective actions.
- **`AnalysisReport`:** A comprehensive model summarizing multiple hypotheses in natural language.

#### Agents & Prompts (LangGraph)
- **Expert Manufacturing Quality Engineer Persona:** The analysis agent will be prompted to find statistical correlations and deduce root causes.
- **Specialized Tool Calling:** The agent will utilize tools to dynamically query DuckDB and aggregate data to support its hypotheses.

#### Data Integration & Synthetic Mocking
- **Mock APIs & Data Generation:** A synthetic data generator (`synthetic_data_generator.py`) will create realistic CSVs modeling defect logs, machine settings, and sensor data with built-in correlations (e.g., high humidity leading to adhesion defects).
- **DuckDB Integration:** Synthetic data will be loaded into DuckDB, simulating integration with real-time Quality Management Systems (QMS) and IoT Sensor APIs.
- **Manufacturing Tools (`tools/manufacturing_tools.py`):** Tools will be built for the LLM to query `fetch_defect_logs`, `fetch_sensor_data`, and `fetch_machine_settings`.

### 3. Measuring Success
The ultimate success of this tool will be measured by its accuracy in identifying correct root causes (validated via our synthetic correlation data) and its overall user adoption rate among quality engineers.

### 4. Implementation Checklist: Files & Dependencies

We have verified that all necessary dependencies (like `pandas`, `duckdb`, `altair` for charts, `fastapi`, and `streamlit`) are **already included** in the existing `requirements.txt`. No new packages need to be added.

#### What We Already Have (Baseline Boilerplate)
- `app.py`: The basic Streamlit frontend.
- `api/main.py`: The FastAPI backend handling agent routing.
- `models/response_models.py`: Basic Pydantic models for structured output.
- `agents/analysis_agent.py`: A generic data analysis LangGraph agent.
- `database/duckdb_manager.py`: DuckDB connector for structured data.
- `vector_db/chroma_manager.py`: ChromaDB for document RAG (useful for reading machine manuals).

#### Files That Need to Change
- **`app.py`**: *How it changes:* Overhaul the UI from a generic chatbot to a Manufacturing Dashboard. Add sidebar filters (Time, Machine ID, Batch) and integrate charting (e.g., Altair/Streamlit native charts) to display correlations.
- **`api/main.py`**: *How it changes:* Add API routes to serve or ingest our synthetic manufacturing data.
- **`models/response_models.py`**: *How it changes:* Create new schemas for `RootCauseHypothesis` (rank, description, confidence_score, evidence) and `AnalysisReport`.
- **`agents/analysis_agent.py`**: *How it changes:* Update the system prompt to assume the persona of an "Expert Manufacturing Quality Engineer" and bind it to the new `RootCauseHypothesis` parser.

#### New Files We Need to Create
- **`tools/manufacturing_tools.py`**: Will contain new LangChain tools for the agent: `fetch_defect_logs()`, `fetch_sensor_data()`, and `fetch_machine_settings()`.
- **`data/synthetic_data_generator.py`**: A new Python script to generate realistic mock CSV data (timestamps, defect types, severity, machine settings, environmental data) with built-in correlations for the AI to discover and load it into DuckDB.
