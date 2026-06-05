from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Week_2.api.routers.chat import router as chat_router
from Week_2.api.routers.ingest import router as ingest_router
from Week_3.api.routers.quiz import router as quiz_router
from Week_3.api.routers.flashcards import router as flashcard_router
from Week_3.api.routers.mindmap import router as mindmap_router

app = FastAPI(
    title="Generative AI Tutor API",
    description="Backend API for the EdTech Adaptive Learning Platform",
    version="1.0.0"
)

# Add CORS middleware to allow the Streamlit frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, lock this down to the specific domain of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(chat_router)
app.include_router(ingest_router)
app.include_router(quiz_router)
app.include_router(flashcard_router)
app.include_router(mindmap_router)

@app.get("/")
def read_root():
    """Welcome message and guidance for direct API visits."""
    return {
        "status": "active",
        "message": "Generative AI Tutor API is running successfully!",
        "documentation": "http://127.0.0.1:8000/docs",
        "frontend_app": "http://127.0.0.1:8501"
    }

@app.get("/health")
def health_check():
    """Simple endpoint to verify the server is running."""
    return {"status": "healthy", "service": "AI Tutor API"}



if __name__ == "__main__":
    import uvicorn
    # This block allows you to run the file directly
    uvicorn.run("Week_2.main:app", host="0.0.0.0", port=8000, reload=True)