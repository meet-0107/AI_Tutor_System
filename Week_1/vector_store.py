import os
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma 

# Load environment variables (specifically GOOGLE_API_KEY from your .env file)
load_dotenv()

# Define where the local database will be saved
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "ai_tutor_syllabus"

def create_vector_store(chunks: List[Document]) -> Chroma:
    """
    Embeds document chunks using Gemini and saves them in a local, persistent ChromaDB.
    """
    # 1. Verify API Key
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found. Please ensure it is set in your .env file.")

    # --- BUG FIX: Filter out empty or whitespace-only chunks ---
    valid_chunks = []
    for chunk in chunks:
        if chunk.page_content and chunk.page_content.strip():
            valid_chunks.append(chunk)
        else:
            print("⚠️ Warning: Skipped an empty or invalid text chunk to prevent index errors.")

    if not valid_chunks:
        raise ValueError("No valid text chunks remained after filtering empty content. Cannot build vector store.")

    print("Initializing Google Gemini Embeddings (models/gemini-embedding-001)...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    print(f"Embedding {len(valid_chunks)} chunks and saving to local database at '{CHROMA_PATH}'...")
    
    # 2. Create and persist the vector database safely
    try:
        vector_store = Chroma.from_documents(
            documents=valid_chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PATH,
            collection_name=COLLECTION_NAME
        )
        print("Vector store successfully built and saved to disk!")
        return vector_store
    except Exception as inner_e:
        # Catch explicit internal engine errors for clearer debugging
        print(f"Internal Chroma/Embedding mapping failed. Raw error details: {inner_e}")
        raise inner_e

def get_vector_store() -> Chroma:
    """
    Loads the existing local ChromaDB instance for querying.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )


# # --- Testing the pipeline locally ---
# if __name__ == "__main__":
#     try:
#         from document_parser import load_and_chunk_pdf
#     except ImportError:
#         print("Make sure this is in the same directory as document_parser.py")
#         exit(1)

#     data_samples_dir = "data_samples"
    
#     if not os.path.exists(data_samples_dir) or not os.listdir(data_samples_dir):
#         print(f"Cannot run test. Please place real PDFs in the '{data_samples_dir}' folder.")
#     else:
#         try:
#             print("--- Starting Document Ingestion Pipeline ---")
#             all_chunks = []
            
#             # Loop through all files in the data_samples directory
#             for filename in os.listdir(data_samples_dir):
#                 if filename.lower().endswith(".pdf"):
#                     pdf_path = os.path.join(data_samples_dir, filename)
#                     print(f"\nProcessing: {filename}")
#                     chunks = load_and_chunk_pdf(pdf_path)
#                     all_chunks.extend(chunks)
            
#             if all_chunks:
#                 db = create_vector_store(all_chunks)
#                 print("\nPipeline Test Complete. Check your project root for the 'chroma_db' folder.")
#             else:
#                 print("\nNo valid PDF chunks were found in the data_samples folder.")
#         except Exception as e:
#             print(f"An error occurred during vector store creation: {e}")