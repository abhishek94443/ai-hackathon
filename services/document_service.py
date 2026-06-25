import tempfile
from typing import List
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loaders.loader_factory import DocumentLoaderFactory

class DocumentService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.loader_factory = DocumentLoaderFactory()

    def process_uploaded_file(self, uploaded_file) -> List[Document]:
        """
        Takes a file uploaded via Streamlit (or FastAPI), saves it temporarily, loads and chunks it.
        """
        # Save uploaded file to a temporary file
        file_extension = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        try:
            # Get the correct loader from the factory (OCP)
            loader = self.loader_factory.get_loader(file_extension)
            documents = loader.load(temp_path)

            # Chunk the documents
            chunks = self.text_splitter.split_documents(documents)
            
            # Add source metadata
            for chunk in chunks:
                chunk.metadata['source'] = uploaded_file.name
                
            return chunks
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
