import os
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

def get_gemini_llm(temperature: float = 0.0, model_name: str = "gemini-3.1-flash-lite") -> ChatGoogleGenerativeAI:
    """
    Returns a configured instance of ChatGoogleGenerativeAI.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    # Configure the underlying genai library if needed for other uses
    genai.configure(api_key=api_key)
    
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key,
    )
