import os
import json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# In-memory dictionary to store session histories
store = {}

# Path to the persistent conversations file
CONVS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'Week_2', 'uploaded_files', 'student_conversations.json')
)

def _load_history_from_disk(session_id: str) -> ChatMessageHistory:
    """
    Loads persisted conversation messages from disk for a given session_id.
    Returns an empty ChatMessageHistory if no history is found.
    """
    history = ChatMessageHistory()
    try:
        if os.path.exists(CONVS_FILE):
            with open(CONVS_FILE, "r", encoding="utf-8") as f:
                convs = json.load(f)
            messages = convs.get(session_id, [])
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    history.add_message(HumanMessage(content=content))
                elif role == "assistant":
                    history.add_message(AIMessage(content=content))
    except Exception as e:
        print(f"[Memory] Warning: Could not load history for session {session_id}: {e}")
    return history

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieves or creates a message history for a given session ID.
    On first access, loads persisted history from disk so AI remembers
    conversations across server restarts.
    """
    if session_id not in store:
        store[session_id] = _load_history_from_disk(session_id)
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
