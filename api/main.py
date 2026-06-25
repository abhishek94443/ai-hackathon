import os
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from agents.supervisor_agent import create_supervisor_graph
from services.document_service import DocumentService
from vector_db.chroma_manager import ChromaManager
from database.duckdb_manager import DuckDBManager

app = FastAPI(title="Agentic Boilerplate API")

# We cache the graph
graph = create_supervisor_graph()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    prompt: str

class DummyFile:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    def read(self):
        return self.data

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    duckdb_manager = DuckDBManager()
    duckdb_manager.store_chat_message("user", request.prompt)
    
    # Reconstruct langchain messages from the history passed
    langchain_messages = []
    for msg in request.messages:
        if msg.role == "user":
            langchain_messages.append(HumanMessage(content=msg.content))
        else:
            langchain_messages.append(AIMessage(content=msg.content))
            
    # Add current prompt
    langchain_messages.append(HumanMessage(content=request.prompt))

    try:
        final_state = graph.invoke(
            {"messages": langchain_messages},
            config={"recursion_limit": 10}
        )
        response_message = final_state["messages"][-1]
        
        duckdb_manager.store_chat_message("assistant", response_message.content)
        
        return {"response": response_message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    try:
        content = await file.read()
        dummy_file = DummyFile(file.filename, content)
        
        doc_service = DocumentService()
        chunks = doc_service.process_uploaded_file(dummy_file)
        
        chroma_manager = ChromaManager()
        chroma_manager.add_documents(chunks)
        
        return {"message": f"Document processed and added to ChromaDB ({len(chunks)} chunks)."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
