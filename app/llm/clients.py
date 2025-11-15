import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_llm_client():
    """
    Initializes and returns the LLM client.
    Reads the API key from the .env file.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    return ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
