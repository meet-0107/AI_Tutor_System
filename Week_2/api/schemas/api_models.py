from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_message: str = Field(..., description="The student's question for the AI tutor.")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI tutor's response strictly derived from the syllabus.")

class IngestResponse(BaseModel):
    message: str = Field(..., description="Success message describing the ingestion status.")
    num_chunks: int = Field(..., description="The number of parsed chunks stored in the database.")