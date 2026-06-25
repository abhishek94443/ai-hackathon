from services.gemini_service import get_gemini_llm
from tools.rag_tool import search_documents
from langgraph.prebuilt import create_react_agent

def create_research_agent():
    """
    Creates an agent specialized in researching documents.
    """
    llm = get_gemini_llm(temperature=0.0)
    tools = [search_documents]
    
    system_prompt = "You are a Research Assistant. Your job is to answer questions by searching through provided documents. Always use the search_documents tool to find relevant information."
    
    agent_executor = create_react_agent(llm, tools, prompt=system_prompt)
    return agent_executor
