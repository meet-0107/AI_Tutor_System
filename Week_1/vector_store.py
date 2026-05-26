import os
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import Pinecone as PineconeVectorStore
from langchain_core.embeddings import Embeddings
from langchain.embeddings import init_embeddings

# Load environment variables
load_dotenv()

# Define Pinecone index name
INDEX_NAME = "ai-tutor-syllabus"

class NomicPrefixEmbeddings(Embeddings):
    """
    Wrapper for wrapping any embedding model (like nomic-embed-text) 
    to add search_document: and search_query: prefixes required by Nomic.
    """
    def __init__(self, base_embeddings: Embeddings):
        self.base_embeddings = base_embeddings

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        prefixed_texts = [f"search_document: {text}" for text in texts]
        return self.base_embeddings.embed_documents(prefixed_texts)

    def embed_query(self, text: str) -> List[float]:
        prefixed_text = f"search_query: {text}"
        return self.base_embeddings.embed_query(prefixed_text)

def get_embeddings() -> Embeddings:
    """
    Initializes and returns the Embedding Model dynamically configured in the .env file.
    Uses LangChain's unified init_embeddings to load any model provider.
    """
    provider = os.getenv("EMBEDDING_PROVIDER").lower().strip()
    model_name = os.getenv("EMBEDDING_MODEL").strip()

    # Dynamically initialize any supported LangChain embedding model
    base_embeddings = init_embeddings(
        model=model_name,
        provider=provider
    )

    # Wrap with Nomic prefixes if using nomic-embed-text
    if "nomic-embed-text" in model_name.lower():
        return NomicPrefixEmbeddings(base_embeddings)
        
    return base_embeddings

def _init_pinecone_index(embeddings: Embeddings):
    """
    Initializes the Pinecone client and creates the index if it doesn't exist.
    Automatically handles index recreation if there's a dimension mismatch.
    """
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
            print(f"Warning: Found existing Pinecone index '{INDEX_NAME}' with dimension {desc.dimension}, "
                  f"but the configured embedding model requires {dimension} dimensions.")
            print(f"Deleting the incompatible index '{INDEX_NAME}' to recreate it...")
            pc.delete_index(INDEX_NAME)
            
    # Create the index if it does not exist (or if it was just deleted)
    if INDEX_NAME not in pc.list_indexes().names():
        print(f"Creating new Pinecone index: '{INDEX_NAME}' with dimension {dimension}...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=dimension,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    return pc

def create_vector_store(chunks: List[Document]) -> PineconeVectorStore:
    """
    Embeds document chunks using configured embedding model and saves them in a cloud Pinecone Vector Database.
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

    # Initialize Pinecone and create index if missing (passing embeddings to determine dimension)
    _init_pinecone_index(embeddings)

    print(f"Embedding {len(valid_chunks)} chunks and saving to Pinecone index '{INDEX_NAME}'...")
    
    try:
        vector_store = PineconeVectorStore.from_documents(
            documents=valid_chunks,
            embedding=embeddings,
            index_name=INDEX_NAME
        )
        print("Vector store successfully built and saved to Pinecone!")
        return vector_store
    except Exception as inner_e:
        print(f"Internal Pinecone/Embedding mapping failed. Raw error details: {inner_e}")
        raise inner_e

def get_vector_store() -> PineconeVectorStore:
    """
    Loads the existing Pinecone instance for querying.
    """
    embeddings = get_embeddings()
    _init_pinecone_index(embeddings) # Ensure index exists before querying
    return PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings
    )

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
                print("\nPipeline Test Complete. Check your Pinecone dashboard to verify.")
            else:
                print("\nNo valid PDF chunks were found in the data_samples folder.")
        except Exception as e:
            print(f"An error occurred during vector store creation: {e}")