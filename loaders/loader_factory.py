from .base_loader import BaseDocumentLoader
from .pdf_loader import PDFLoader
from .txt_loader import TXTLoader

class DocumentLoaderFactory:
    def __init__(self):
        self._loaders = {
            '.pdf': PDFLoader(),
            '.txt': TXTLoader()
        }
        
    def get_loader(self, file_extension: str) -> BaseDocumentLoader:
        """
        Returns the appropriate loader for the given extension.
        Raises a ValueError if the extension is not supported.
        """
        loader = self._loaders.get(file_extension.lower())
        if not loader:
            raise ValueError(f"Unsupported file type: {file_extension}")
        return loader
