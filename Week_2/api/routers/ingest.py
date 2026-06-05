import os
import shutil
import json
import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from Week_2.api.schemas.api_models import IngestResponse
from Week_1 import load_and_chunk_pdf, create_vector_store

router = APIRouter(
    prefix="/ingest",
    tags=["Document Ingestion"]
)

@router.get("/files")
async def get_uploaded_files():
    """
    Returns a list of all syllabus files that have been successfully ingested.
    """
    metadata_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files', 'uploaded_files.json'))
    if not os.path.exists(metadata_file):
        return []
    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=IngestResponse)
async def ingest_file(file: UploadFile = File(...)):
    """
    Upload a syllabus PDF, parse it into chunks, store the embeddings in Pinecone,
    and save the metadata in the JSON registry. The physical file is deleted.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files'))
    os.makedirs(uploads_dir, exist_ok=True)
    metadata_file = os.path.join(uploads_dir, 'uploaded_files.json')
    
    # Check if the file has already been uploaded
    if os.path.exists(metadata_file):
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                uploaded_files = json.load(f)
            for uploaded in uploaded_files:
                if uploaded.get("filename") == file.filename:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File '{file.filename}' is already uploaded."
                    )
        except HTTPException:
            raise
        except Exception:
            pass

    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'temp'))
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save the uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse and chunk the PDF from the temp location
        chunks = load_and_chunk_pdf(temp_file_path)
        
        # Create/Update vector store
        create_vector_store(chunks)
        
        # Save metadata to uploaded_files/uploaded_files.json
        uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files'))
        os.makedirs(uploads_dir, exist_ok=True)
        metadata_file = os.path.join(uploads_dir, 'uploaded_files.json')
        
        uploaded_files = []
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, "r", encoding="utf-8") as f:
                    uploaded_files = json.load(f)
            except Exception:
                pass
                
        uploaded_files.append({
            "filename": file.filename,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chunks": len(chunks)
        })
        
        # Atomic write to prevent file corruption
        temp_metadata_file = metadata_file + ".tmp"
        try:
            with open(temp_metadata_file, "w", encoding="utf-8") as f:
                json.dump(uploaded_files, f, indent=4)
            os.replace(temp_metadata_file, metadata_file)
        except Exception as e:
            if os.path.exists(temp_metadata_file):
                os.remove(temp_metadata_file)
            raise e
        
        return IngestResponse(
            message=f"Successfully ingested {file.filename} into vector store.",
            num_chunks=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup physical temp file so it is not stored physically
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
