from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_tutor_prompt():
    """
    Returns the ChatPromptTemplate for the AI Tutor with conversation history support.
    """
    return ChatPromptTemplate.from_messages([
        ("system", "You are an expert tutor. Use ONLY the following context to answer the student's question.\n"
                   "If you don't know the answer, just say that you don't know. Don't try to make up an answer.\n\n"
                   "Context:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
