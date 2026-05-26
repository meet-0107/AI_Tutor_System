from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from Week_3 import generate_quiz

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz Generation"]
)

class QuizRequest(BaseModel):
    topic: str = Field(..., description="The topic for which to generate the multiple-choice quiz.")

@router.post("/generate")
def generate_quiz_endpoint(request: QuizRequest):
    """
    Generates a structured multiple-choice quiz based on the provided topic.
    """
    try:
        quiz = generate_quiz(request.topic)
        # Fast API automatically serializes the Pydantic object to JSON
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
