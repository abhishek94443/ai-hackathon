# Enterprise AI Agentic Application 🚀

An advanced, extensible boilerplate for building scalable Agentic Applications. It leverages **LangGraph**, **FastAPI**, **Streamlit**, and **Google Gemini** to provide a robust multi-agent architecture capable of reasoning, data analysis, database querying, and document research.

## 🌟 Features

- **Multi-Agent Architecture**: Uses **LangGraph** as a supervisor to intelligently route tasks between specialized agents:
  - **Research Agent**: Queries knowledge bases and vector databases using RAG (Retrieval-Augmented Generation).
  - **Analysis Agent**: Interacts with databases, analyzes structured data, and parses complex information.
  - **Chat Agent**: Handles general conversation and greetings efficiently.
- **Interactive UI**: A sleek **Streamlit** frontend offering a modern chat interface and document upload capabilities.
- **Robust Backend**: A high-performance **FastAPI** backend exposing endpoints for conversational AI (`/chat`) and file processing (`/upload`).
- **Document Processing**: Out-of-the-box support for PDF and TXT file uploads, chunking, and automatic embedding into a local **ChromaDB** instance.
- **Structured Data Storage**: Integrates **DuckDB** for tracking conversational history and running fast, local analytical queries.
- **State-of-the-Art LLM**: Powered by Google's **Gemini** models for both intricate reasoning and seamless generation.

## 🏗️ Architecture & Directory Structure

```text
hackathon/
├── agents/             # LangGraph definitions (Supervisor, Research, Analysis)
├── api/                # FastAPI application (main.py)
├── database/           # DuckDB integration for structured data storage
├── loaders/            # Base and custom file loaders (TXT, PDF, etc.)
├── models/             # Pydantic models for structured agent outputs
├── prompts/            # System prompts guiding agent behavior
├── services/           # Services for document processing and Gemini LLM setup
├── tools/              # Agent tools (RAG, Database Query, Analysis)
├── vector_db/          # ChromaDB integration for vector storage
├── app.py              # Streamlit frontend entrypoint
└── requirements.txt    # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Google Gemini API Key

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd hackathon
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory (reference the `.env.example` file if available) and add your API credentials:

   ```env
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

### Running the Application

The application requires both the FastAPI backend and the Streamlit frontend to be running simultaneously.

1. **Start the FastAPI Backend:**
   Open a terminal and run:

   ```bash
   uvicorn api.main:app --reload --port 8000
   ```
   *The API will be available at `http://localhost:8000`. You can view the Swagger UI documentation at `http://localhost:8000/docs`.*

2. **Start the Streamlit Frontend:**
   Open a new terminal window (ensure your virtual environment is activated) and run:

   ```bash
   streamlit run app.py
   ```
   *The application UI will automatically launch in your browser at `http://localhost:8501`.*

## 💡 Usage

- **Chat Interface**: Ask general questions, request complex data analysis, or query specific information. The Supervisor Agent will evaluate your prompt and dynamically route your request to the best-suited sub-agent.
- **Document Upload**: Use the sidebar to upload `.txt` or `.pdf` files. The system processes, chunks, and stores these documents in ChromaDB, enabling the **Research Agent** to answer questions directly based on your customized data context.

## 🛠️ Extending the Boilerplate

This boilerplate is built to scale. You can easily extend its capabilities:
- **Add New Agents**: Create new specialized agent files in the `agents/` directory and update the graph in `agents/supervisor_agent.py` to route tasks to them.
- **Add Custom Tools**: Implement custom tools in the `tools/` directory and bind them to existing or new agents.
- **Swap Vector Databases**: Modify `vector_db/chroma_manager.py` to seamlessly integrate with alternative vector stores like Pinecone, Qdrant, or Milvus.

## 📝 License

This project is provided as an open-source tool and is available under the MIT License.
