from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator
from services.gemini_service import get_gemini_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent

# Define the state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_node: str

class Route(BaseModel):
    next_node: Literal["research", "analysis", "chat", "FINISH"]

def _format_content(content) -> str:
    if isinstance(content, list):
        return "".join([b.get("text", "") if isinstance(b, dict) else str(b) for b in content])
    return str(content)

def supervisor_node(state: AgentState):
    print(f"\n[DEBUG] --- Supervisor checking state (Messages: {len(state['messages'])}) ---")
    llm = get_gemini_llm(temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supervisor managing a conversation between a user and specialized workers. "
                   "Look at the conversation history. If the latest message is an AI response that fully answers the user's request, you MUST route to 'FINISH'. "
                   "If the user's request is unanswered and asks about uploaded documents, route to 'research'. "
                   "If the user's request is unanswered and asks to analyze data or query the database, route to 'analysis'. "
                   "If the user is just greeting you or asking a general question, route to 'chat'. "
                   "If you are unsure, route to 'chat'."),
        ("human", "{messages}")
    ])
    
    chain = prompt | llm.with_structured_output(Route)
    result = chain.invoke({"messages": state["messages"]})
    print(f"[DEBUG] --- Supervisor Decision: {result.next_node} ---\n")
    return {"next_node": result.next_node}

def research_node(state: AgentState):
    print("\n[DEBUG] --- Research Agent started ---")
    agent = create_research_agent()
    # Get the last human message
    last_message = state["messages"][-1].content
    result = agent.invoke({"messages": [("user", last_message)]})
    output_content = _format_content(result["messages"][-1].content)
    print("[DEBUG] --- Research Agent finished ---\n")
    return {"messages": [AIMessage(content=output_content, name="research")]}

def analysis_node(state: AgentState):
    print("\n[DEBUG] --- Analysis Agent started ---")
    agent, parser = create_analysis_agent()
    last_message = state["messages"][-1].content
    result = agent.invoke({"messages": [("user", last_message)]})
    output_content = _format_content(result["messages"][-1].content)
    
    # Attempt to parse, though the agent might return a string directly
    try:
        parsed_result = parser.parse(output_content)
        output_content = parsed_result.model_dump_json(indent=2)
    except Exception:
        pass
        
    print("[DEBUG] --- Analysis Agent finished ---\n")
    return {"messages": [AIMessage(content=output_content, name="analysis")]}

def chat_node(state: AgentState):
    print("\n[DEBUG] --- Chat Agent started ---")
    llm = get_gemini_llm(temperature=0.7)
    messages = [{"role": "system", "content": "You are a helpful AI assistant. Answer general questions and greet the user. Keep it brief."}]
    messages.extend([m for m in state["messages"]])
    
    response = llm.invoke(messages)
    output_content = _format_content(response.content)
    print("[DEBUG] --- Chat Agent finished ---\n")
    return {"messages": [AIMessage(content=output_content, name="chat")]}

def create_supervisor_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("chat", chat_node)
    
    workflow.add_edge(START, "supervisor")
    
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next_node"],
        {
            "research": "research",
            "analysis": "analysis",
            "chat": "chat",
            "FINISH": END
        }
    )
    
    workflow.add_edge("research", END)
    workflow.add_edge("analysis", END)
    workflow.add_edge("chat", END)
    
    return workflow.compile()
