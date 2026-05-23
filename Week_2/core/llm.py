import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm() -> ChatGoogleGenerativeAI:
    """
    Initializes and returns the Gemini Chat Model.
    Temperature is set to 0 to minimize hallucinations.
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in .env file.")
        
    # We use gemini-2.5-flash as it is highly performant and cost-effective 
    # for processing large blocks of retrieved text context.
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.1,
        max_tokens=1024,
    )
    return llm
