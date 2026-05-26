from fastapi import APIRouter, HTTPException
from Week_2.api.schemas.api_models import ChatRequest, ChatResponse
from Week_2 import get_rag_chain
from Week_3 import get_rag_chain_with_memory

router = APIRouter(
    prefix="/chat",
    tags=["Chat Interface"]
)

# Initialize the RAG chain once when the router loads to avoid rebuilding it on every request
rag_chain = get_rag_chain()
memory_chain = get_rag_chain_with_memory(rag_chain)

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Accepts a student's message, retrieves context from the syllabus, 
    and returns a Socratic response from the AI tutor with conversation history.
    """
    try:
        # Pass the input dictionary and session_id configuration
        answer = memory_chain.invoke(
            {"question": request.user_message, "chat_history": []}, 
            config={"configurable": {"session_id": request.session_id}}
        )
        
        return ChatResponse(response=answer)
    except Exception as e:
        # Catch unexpected errors to prevent the API from crashing completely
        raise HTTPException(status_code=500, detail=str(e))