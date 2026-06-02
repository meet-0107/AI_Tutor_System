from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from Week_2 import get_llm
from Week_1 import get_vector_store

class Flashcard(BaseModel):
    term: str = Field(description="The key term or concept")
    definition: str = Field(description="A clear, concise definition or explanation of the term based strictly on the context")

class FlashcardSet(BaseModel):
    flashcards: list[Flashcard] = Field(description="A list of exactly 5 flashcards")

def generate_flashcards(topic: str) -> FlashcardSet:
    """
    Generates 5 digital flashcards on the provided topic by first retrieving
    relevant context from the syllabus PDFs (VectorStore) and then using
    the LLM to extract the most important terms and definitions.
    """
    llm = get_llm()
    vector_store = get_vector_store()
    
    # Retrieve top chunks related to the topic
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(topic)
    
    # Format context
    context = "\n\n".join(doc.page_content for doc in docs)
    
    # Fallback context if vector store is empty or nothing found
    if not context.strip():
        context = "No specific syllabus context found. Use general academic knowledge."

    # Enforce structured output based on the FlashcardSet Pydantic schema
    structured_llm = llm.with_structured_output(FlashcardSet)
    
    # Prompt template for flashcard generation
    prompt = PromptTemplate.from_template(
        "You are an expert curriculum designer. Based on the following syllabus context, "
        "extract the 5 most important key terms related to '{topic}' and provide a concise, accurate definition for each.\n\n"
        "Context:\n{context}\n\n"
        "Generate exactly 5 flashcards."
    )
    
    # Create the chain
    flashcard_chain = prompt | structured_llm
    
    # Execute the chain
    return flashcard_chain.invoke({"topic": topic, "context": context})
