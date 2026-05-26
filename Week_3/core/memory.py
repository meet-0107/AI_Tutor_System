from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# In-memory dictionary to store session histories
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieves or creates a message history for a given session ID.
    In a production application, this would connect to a database (like Redis or PostgreSQL).
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_rag_chain_with_memory(rag_chain):
    """
    Wraps the core RAG chain with LangChain's RunnableWithMessageHistory
    so it automatically manages the chat history for each session.
    """
    return RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history"
    )
