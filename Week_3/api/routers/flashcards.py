from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from Week_3.core.flashcard_engine import generate_flashcards

router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcard Generation"]
)

class FlashcardRequest(BaseModel):
    topic: str = Field(..., description="The topic for which to generate flashcards.")

@router.post("/generate")
def generate_flashcards_endpoint(request: FlashcardRequest):
    """
    Generates a set of flashcards based on the provided topic using the syllabus context.
    """
    try:
        flashcard_set = generate_flashcards(request.topic)
        return flashcard_set
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
