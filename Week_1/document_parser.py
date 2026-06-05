import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_pdf(file_path: str) -> List[Document]:
    """
    Loads a PDF document and splits it into semantically meaningful chunks.
    
    Args:
        file_path (str): The relative or absolute path to the PDF file.
        
    Returns:
        List[Document]: A list of LangChain Document objects containing the text chunks and metadata.
    """
    # Verify the file exists before attempting to load
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find the syllabus file at: {file_path}")

    print(f"Loading document: {file_path}...")
    
    # 1. Initialize the PDF Loader
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    print(f"Successfully loaded {len(pages)} pages. Splitting text...")

    # 2. Initialize the Text Splitter
    # chunk_size: 1000 characters is roughly 150-250 words, a good size for an LLM context window.
    # chunk_overlap: 200 characters ensures that if a concept spans across two chunks, 
    # the overlap prevents the context from being completely severed.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    # 3. Split the loaded pages into chunks
    chunks = text_splitter.split_documents(pages)
    
    print(f"Created {len(chunks)} text chunks.")
    
    return chunks



# --- Testing the pipeline locally ---
if __name__ == "__main__":
    # Define the path to the sample syllabus
    # Assuming this script is run from the root of the 'ai-tutor-platform' project
    sample_pdf_path = os.path.join("uploaded_files", "AIML-NOTE.pdf")
    
    # Create a dummy PDF for testing if it doesn't exist
    os.makedirs("uploaded_files", exist_ok=True)
    if not os.path.exists(sample_pdf_path):
        print("Creating a dummy PDF for testing...")
        # A quick way to test without a real PDF is to handle the error or create one manually.
        # For actual testing, make sure you drop a real PDF named 'sample_syllabus.pdf' into 'data_samples/'.
        print(f"Please place a real PDF at '{sample_pdf_path}' to run this test.")
    else:
        try:
            # Execute the parsing function
            document_chunks = load_and_chunk_pdf(sample_pdf_path)
            
            # Print a preview of the first chunk to verify metadata and content
            if document_chunks:
                print("\n--- Preview of Chunk 1 ---")
                print(f"Metadata: {document_chunks[0].metadata}")
                print(f"Content:\n{document_chunks[0].page_content[:300]}...\n")
        except Exception as e:
            print(f"An error occurred: {e}")