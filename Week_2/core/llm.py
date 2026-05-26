import os
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

from langchain.chat_models import init_chat_model

def get_llm() -> BaseChatModel:
    """
    Initializes and returns the Chat Model dynamically configured in the .env file.
    """
    provider = os.getenv("LLM_PROVIDER").lower().strip()
    model_name = os.getenv("LLM_MODEL").strip()
    temperature = float(os.getenv("LLM_TEMPERATURE"))

    # Dynamically load and initialize the model using LangChain's unified interface
    return init_chat_model(
        model=model_name,
        model_provider=provider,
        temperature=temperature
    )


if __name__ == "__main__":
    try:
        print("Testing dynamic LLM initialization from .env...")
        llm = get_llm()
        print(f"Success! Loaded LLM instance of type: {type(llm).__name__}")
        print(f"Model Name: {llm.model_name if hasattr(llm, 'model_name') else getattr(llm, 'model', 'unknown')}")
        print("Testing API connectivity...")
        res = llm.invoke("Say 'System OK' in two words.")
        print(f"Response: {res.content.strip()}")
    except Exception as e:
        print(f"Error initializing LLM: {e}")


