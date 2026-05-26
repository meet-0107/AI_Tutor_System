from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from Week_2 import get_llm

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
    using Ollama/Mistral's structured JSON output capability.
    """
    llm = get_llm()
    
    # Enforce structured output based on the Quiz Pydantic schema
    structured_llm = llm.with_structured_output(Quiz)
    
    # Simple prompt template for quiz generation
    prompt = PromptTemplate.from_template(
        "You are an expert curriculum designer. Generate a multiple-choice quiz about '{topic}'. "
        "The quiz must contain exactly 5 questions. Ensure the distractors (incorrect options) are plausible."
    )
    
    # Create the LCEL chain
    quiz_chain = prompt | structured_llm
    
    # Execute the chain and return the structured Pydantic object
    return quiz_chain.invoke({"topic": topic})
