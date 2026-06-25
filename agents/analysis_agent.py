from services.gemini_service import get_gemini_llm
from tools.database_tool import query_database
from tools.analysis_tool import analyze_data
from models.response_models import AnalysisResult
from langgraph.prebuilt import create_react_agent
from langchain_core.output_parsers import PydanticOutputParser

def create_analysis_agent():
    """
    Creates an agent specialized in data analysis and structured output.
    """
    llm = get_gemini_llm(temperature=0.1)
    tools = [query_database, analyze_data]
    
    parser = PydanticOutputParser(pydantic_object=AnalysisResult)
    
    system_prompt = (
        "You are a Data Analyst. Use the tools provided to query the database and analyze data. "
        "You must always return your final answer in the following JSON format:\n"
        f"{parser.get_format_instructions()}"
    )
    
    agent_executor = create_react_agent(llm, tools, prompt=system_prompt)
    return agent_executor, parser
