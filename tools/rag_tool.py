from langchain.tools import tool
from vector_db.chroma_manager import ChromaManager

@tool("search_documents")
def search_documents(query: str) -> str:
    """
    Search through uploaded documents using vector similarity search.
    Useful for answering questions based on the provided document context.
    
    Args:
        query (str): The search query.
        
    Returns:
        str: A concatenated string of the most relevant document contents.
    """
    try:
        manager = ChromaManager()
        results = manager.similarity_search(query)
        if not results:
            return "No relevant documents found."
        
        return "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        return f"Error searching documents: {str(e)}"
