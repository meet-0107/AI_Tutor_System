import os
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain.embeddings import init_embeddings
from langchain_core.vectorstores import VectorStore

# Load environment variables
load_dotenv()

# Define centralized vector store settings
VECTOR_STORE_PROVIDER = os.getenv("VECTOR_STORE_PROVIDER")
if VECTOR_STORE_PROVIDER:
    VECTOR_STORE_PROVIDER = VECTOR_STORE_PROVIDER.lower().strip()

INDEX_NAME = os.getenv("VECTOR_STORE_INDEX_NAME")
if INDEX_NAME:
    INDEX_NAME = INDEX_NAME.strip()

chroma_dir = os.getenv("CHROMA_PERSIST_DIRECTORY")
CHROMA_PERSIST_DIR = chroma_dir.strip() if chroma_dir else None

def get_embeddings() -> Embeddings:
    """
    Initializes and returns the Embedding Model dynamically configured in the .env file.
    Uses LangChain's unified init_embeddings to load any model provider.
    """
    provider = os.getenv("EMBEDDING_PROVIDER").lower().strip()
    model_name = os.getenv("EMBEDDING_MODEL").strip()

    # Dynamically initialize any supported LangChain embedding model
    return init_embeddings(
        model=model_name,
        provider=provider
    )

def _init_index(embeddings: Embeddings):
    """
    Initializes the cloud index if using Pinecone.
    Automatically handles index recreation if there's a dimension mismatch.
    """
    if VECTOR_STORE_PROVIDER == "pinecone":
        from pinecone import Pinecone, ServerlessSpec
        
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set.")
        
        pc = Pinecone(api_key=api_key)
        
        # Determine the target dimension dynamically
        print("Determining embedding model dimension dynamically...")
        dummy_vector = embeddings.embed_query("dimension_test")
        dimension = len(dummy_vector)
        
        # Check if the index already exists and verify its dimension
        if INDEX_NAME in pc.list_indexes().names():
            desc = pc.describe_index(INDEX_NAME)
            if desc.dimension != dimension:
                print(f"Warning: Found existing index '{INDEX_NAME}' with dimension {desc.dimension}, "
                      f"but the configured embedding model requires {dimension} dimensions.")
                print(f"Deleting the incompatible index '{INDEX_NAME}' to recreate it...")
                pc.delete_index(INDEX_NAME)
                
        # Create the index if it does not exist (or if it was just deleted)
        if INDEX_NAME not in pc.list_indexes().names():
            print(f"Creating new index: '{INDEX_NAME}' with dimension {dimension}...")
            pc.create_index(
                name=INDEX_NAME,
                dimension=dimension,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )

def create_vector_store(chunks: List[Document]) -> VectorStore:
    """
    Embeds document chunks and saves them in the centralized Vector Database configured in .env.
    """
    # Filter out empty or whitespace-only chunks
    valid_chunks = []
    for chunk in chunks:
        if chunk.page_content and chunk.page_content.strip():
            valid_chunks.append(chunk)
        else:
            print("Warning: Skipped an empty or invalid text chunk to prevent index errors.")

    if not valid_chunks:
        raise ValueError("No valid text chunks remained after filtering empty content. Cannot build vector store.")

    # Initialize dynamic embeddings
    embeddings = get_embeddings()

    print(f"Using vector store provider: '{VECTOR_STORE_PROVIDER}'")
    
    try:
        if VECTOR_STORE_PROVIDER == "pinecone":
            from langchain_pinecone import Pinecone as PineconeVectorStore
            
            # Initialize index
            _init_index(embeddings)
            print(f"Embedding {len(valid_chunks)} chunks and saving to Pinecone index '{INDEX_NAME}'...")
            vector_store = PineconeVectorStore.from_documents(
                documents=valid_chunks,
                embedding=embeddings,
                index_name=INDEX_NAME
            )
            print("Vector store successfully built!")
            return vector_store
            
        elif VECTOR_STORE_PROVIDER == "chroma":
            from langchain_chroma import Chroma
            print(f"Embedding {len(valid_chunks)} chunks and saving to Chroma collection '{INDEX_NAME}' at '{CHROMA_PERSIST_DIR}'...")
            vector_store = Chroma.from_documents(
                documents=valid_chunks,
                embedding=embeddings,
                persist_directory=CHROMA_PERSIST_DIR,
                collection_name=INDEX_NAME
            )
            print("Vector store successfully built!")
            return vector_store
            
        else:
            raise ValueError(f"Unsupported VECTOR_STORE_PROVIDER '{VECTOR_STORE_PROVIDER}' configured in .env.")
            
    except Exception as e:
        print(f"Failed to create vector store: {e}")
        raise e

def get_vector_store() -> VectorStore:
    """
    Loads the configured centralized Vector Database instance for querying.
    """
    embeddings = get_embeddings()
    
    if VECTOR_STORE_PROVIDER == "pinecone":
        from langchain_pinecone import Pinecone as PineconeVectorStore
        _init_index(embeddings) # Ensure index exists
        return PineconeVectorStore(
            index_name=INDEX_NAME,
            embedding=embeddings
        )
    elif VECTOR_STORE_PROVIDER == "chroma":
        from langchain_chroma import Chroma
        return Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=embeddings,
            collection_name=INDEX_NAME
        )
    else:
        raise ValueError(f"Unsupported VECTOR_STORE_PROVIDER '{VECTOR_STORE_PROVIDER}' configured in .env.")

# --- Testing the pipeline locally ---
if __name__ == "__main__":
    try:
        from document_parser import load_and_chunk_pdf
    except ImportError:
        print("Make sure this is in the same directory as document_parser.py")
        exit(1)

    data_samples_dir = "data_samples"
    
    if not os.path.exists(data_samples_dir) or not os.listdir(data_samples_dir):
        print(f"Cannot run test. Please place real PDFs in the '{data_samples_dir}' folder.")
    else:
        try:
            print("--- Starting Document Ingestion Pipeline ---")
            all_chunks = []
            
            for filename in os.listdir(data_samples_dir):
                if filename.lower().endswith(".pdf"):
                    pdf_path = os.path.join(data_samples_dir, filename)
                    print(f"\nProcessing: {filename}")
                    chunks = load_and_chunk_pdf(pdf_path)
                    all_chunks.extend(chunks)
            
            if all_chunks:
                db = create_vector_store(all_chunks)
                print(f"\nPipeline Test Complete. Check your {VECTOR_STORE_PROVIDER} dashboard/directory to verify.")
            else:
                print("\nNo valid PDF chunks were found in the data_samples folder.")
        except Exception as e:
            print(f"An error occurred during vector store creation: {e}")