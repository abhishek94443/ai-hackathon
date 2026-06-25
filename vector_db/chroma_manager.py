import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
from langchain_core.documents import Document

class ChromaManager:
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.persist_directory = persist_directory
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY must be set to initialize ChromaManager.")
            
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents: List[Document]):
        """Adds documents to ChromaDB."""
        try:
            self.vector_store.add_documents(documents)
        except Exception as e:
            raise RuntimeError(f"Error adding documents to Chroma: {str(e)}")

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Performs a similarity search."""
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            raise RuntimeError(f"Error performing similarity search: {str(e)}")
