from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from Week_3.core.flashcard_engine import generate_flashcards

router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcard Generation"]
)

class FlashcardRequest(BaseModel):
    topic: str = Field(..., description="The topic for which to generate flashcards.")
    session_id: str = Field("default", description="The session ID to track conversation history.")

@router.post("/generate")
def generate_flashcards_endpoint(request: FlashcardRequest):
    """
    Generates a set of flashcards based on the provided topic using the syllabus context.
    """
    try:
        # Log student query
        from Week_2.api.routers.chat import log_student_query, save_chat_message
        log_student_query(f"Generate flashcards: {request.topic}", request.session_id)
        
        # Save user request message in chat history
        save_chat_message(request.session_id, "user", f"Generate flashcards for: {request.topic}")
        
        flashcard_set = generate_flashcards(request.topic)
        
        # Save flashcards response message in chat history
        if hasattr(flashcard_set, "model_dump"):
            flashcard_dict = flashcard_set.model_dump()
        else:
            flashcard_dict = flashcard_set.dict()
            
        save_chat_message(request.session_id, "assistant", flashcard_dict, msg_type="flashcards")
        
        return flashcard_set
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
