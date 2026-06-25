from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from .base_loader import BaseDocumentLoader

class PDFLoader(BaseDocumentLoader):
    def load(self, file_path: str) -> List[Document]:
        loader = PyPDFLoader(file_path)
        return loader.load()
