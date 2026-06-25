from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from .base_loader import BaseDocumentLoader

class TXTLoader(BaseDocumentLoader):
    def load(self, file_path: str) -> List[Document]:
        # Determine encoding manually to avoid LangChain autodetect bugs
        detected_encoding = 'utf-8'
        for enc in ['utf-8', 'utf-16', 'utf-16le', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    f.read()
                detected_encoding = enc
                break
            except UnicodeDecodeError:
                continue
                
        loader = TextLoader(file_path, encoding=detected_encoding)
        return loader.load()
