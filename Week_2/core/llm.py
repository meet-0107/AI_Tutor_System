import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

def get_llm() -> ChatOllama:
    """
    Initializes and returns the local Ollama Chat Model (Phi3).
    Temperature is set to 0.1 to minimize hallucinations.
    """
    # We use phi3 running locally on Ollama as it is highly performant and memory-efficient 
    # for processing large blocks of retrieved text context.
    llm = ChatOllama(
        model="phi3",
        temperature=0.1
    )
    return llm
