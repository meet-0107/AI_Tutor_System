from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from Week_2 import get_llm

from Week_1 import get_vector_store

# Define the structured output schema for the quiz
class Question(BaseModel):
    question_text: str = Field(description="The multiple-choice question text")
    options: list[str] = Field(description="A list of exactly 4 choices")
    correct_answer: str = Field(description="The exact text of the correct choice")
    explanation: str = Field(description="Why this answer is correct")

class Quiz(BaseModel):
    questions: list[Question] = Field(description="A list of exactly 5 multiple-choice questions")

def generate_quiz(topic: str) -> Quiz:
    """
    Generates a 5-question multiple-choice quiz on the provided topic
    by retrieving syllabus context from the VectorStore, then using
    Ollama/Mistral's structured JSON output capability.
    """
    llm = get_llm()
    
    # Retrieve top chunks related to the topic
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(topic)
    
    # Format context
    context = "\n\n".join(doc.page_content for doc in docs)
    if not context.strip():
        context = "No specific syllabus context found. Generate a quiz using general academic knowledge."
        
    # Enforce structured output based on the Quiz Pydantic schema
    structured_llm = llm.with_structured_output(Quiz)
    
    # Prompt template for quiz generation
    prompt = PromptTemplate.from_template(
        "You are an expert curriculum designer. Based on the syllabus context provided below, "
        "generate a multiple-choice quiz about '{topic}'. "
        "The quiz must contain exactly 5 questions. Ensure the distractors (incorrect options) are plausible.\n\n"
        "Syllabus Context:\n{context}"
    )
    
    # Create the LCEL chain
    quiz_chain = prompt | structured_llm
    
    # Execute the chain and return the structured Pydantic object
    return quiz_chain.invoke({"topic": topic, "context": context})
