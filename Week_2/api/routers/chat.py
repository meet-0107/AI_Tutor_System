from fastapi import APIRouter, HTTPException
from api.schemas.api_models import ChatRequest, ChatResponse
from core.rag import get_rag_chain

router = APIRouter(
    prefix="/chat",
    tags=["Chat Interface"]
)

# Initialize the RAG chain once when the router loads to avoid rebuilding it on every request
rag_chain = get_rag_chain()

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Accepts a student's message, retrieves context from the syllabus, 
    and returns a Socratic response from the AI tutor.
    """
    try:
        # We use a standard 'def' instead of 'async def' because querying the local 
        # ChromaDB instance operates synchronously under the hood. 
        # FastAPI will automatically run this in a background thread pool to prevent blocking.
        answer = rag_chain.invoke(request.user_message)
        
        return ChatResponse(response=answer)
    except Exception as e:
        # Catch unexpected errors to prevent the API from crashing completely
        raise HTTPException(status_code=500, detail=str(e))