import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from Week_2.api.schemas.api_models import IngestResponse
from Week_1 import load_and_chunk_pdf, create_vector_store

router = APIRouter(
    prefix="/ingest",
    tags=["Document Ingestion"]
)

@router.post("/", response_model=IngestResponse)
async def ingest_file(file: UploadFile = File(...)):
    """
    Upload a syllabus PDF, parse it into chunks, and store the embeddings in Pinecone.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'temp'))
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save the uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse and chunk the PDF
        chunks = load_and_chunk_pdf(temp_file_path)
        
        # Create/Update vector store
        create_vector_store(chunks)
        
        return IngestResponse(
            message=f"Successfully ingested {file.filename} into vector store.",
            num_chunks=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
