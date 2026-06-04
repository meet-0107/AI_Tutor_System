from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from Week_3.core.mindmap_engine import generate_mindmap

router = APIRouter(
    prefix="/mindmap",
    tags=["Mind Map Generation"]
)

class MindMapRequest(BaseModel):
    topic: str = Field(..., description="The topic for which to generate the concept mind map.")
    session_id: str = Field("default", description="The session ID to track conversation history.")

@router.post("/generate")
def generate_mindmap_endpoint(request: MindMapRequest):
    """
    Generates a visual concept mind map in Mermaid.js syntax for the topic and logs the query.
    """
    try:
        from Week_2.api.routers.chat import log_student_query, save_chat_message
        
        # Log student query
        log_student_query(f"Generate mind map: {request.topic}", request.session_id)
        
        # Save user request message in chat history
        save_chat_message(request.session_id, "user", f"Generate mind map for: {request.topic}")
        
        # Generate Mermaid code
        mermaid_code = generate_mindmap(request.topic)
        
        # Save mindmap assistant response in chat history with custom type
        save_chat_message(request.session_id, "assistant", mermaid_code, msg_type="mindmap")
        
        return {"mermaid_code": mermaid_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
