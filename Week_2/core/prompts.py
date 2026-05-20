from langchain_core.prompts import ChatPromptTemplate

def get_tutor_prompt():
    """
    Returns the ChatPromptTemplate for the AI Tutor.
    """
    template = """You are an expert tutor. Use
ONLY the following context to answer the student's question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:"""
    return ChatPromptTemplate.from_template(template)
