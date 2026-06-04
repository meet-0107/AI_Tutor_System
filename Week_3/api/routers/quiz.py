from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from Week_3 import generate_quiz

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz Generation"]
)

class QuizRequest(BaseModel):
    topic: str = Field(..., description="The topic for which to generate the multiple-choice quiz.")
    session_id: str = Field("default", description="The session ID to track conversation history.")

@router.post("/generate")
def generate_quiz_endpoint(request: QuizRequest):
    """
    Generates a structured multiple-choice quiz based on the provided topic.
    """
    try:
        # Log student query
        from Week_2.api.routers.chat import log_student_query
        log_student_query(f"Generate quiz: {request.topic}", request.session_id)
        
        quiz = generate_quiz(request.topic)
        # Fast API automatically serializes the Pydantic object to JSON
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
