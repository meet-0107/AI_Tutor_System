import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Week_2.core.llm import get_llm
from Week_2.core.prompts import get_tutor_prompt
from Week_1.vector_store import get_vector_store
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs) -> str:
    """Helper function to format retrieved chunks into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    """
    Builds the Retrieval-Augmented Generation (RAG) pipeline using LCEL.
    """
    # 1. Initialize core components
    vector_store = get_vector_store()
    
    # Configure the retriever to fetch the top 3 most relevant chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    llm = get_llm()
    prompt = get_tutor_prompt()
    
    # 2. Build the explicit LCEL Chain
    # The dictionary defines the prompt's input variables.
    # 'context': A Runnable pipeline that fetches documents and formats them.
    # 'question': RunnablePassthrough simply forwards the user's input string.
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# --- Testing the RAG pipeline locally ---
if __name__ == "__main__":
    try:
        chain = get_rag_chain()
        
        print("--- Testing RAG Chain ---")
        test_question = "who is internal guide?"
        print(f"Question: {test_question}\n")
        
        # Invoke the chain with a test string
        response = chain.invoke(test_question)
        print(f"AI Tutor Response:\n{response}")
        
    except Exception as e:
        print(f"\nFailed to run RAG chain: {e}")
        print("Ensure you have created the ChromaDB by running vector_store.py first!")