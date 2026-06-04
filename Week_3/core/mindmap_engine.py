from langchain_core.prompts import PromptTemplate
from Week_2 import get_llm
from Week_1 import get_vector_store

def generate_mindmap(topic: str) -> str:
    """
    Generates a Mermaid.js flowchart (graph TD/LR) representing a mind map of the topic.
    First retrieves syllabus context, then prompts the LLM to outline branches.
    """
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(topic)
    context = "\n\n".join(doc.page_content for doc in docs)
    
    if not context.strip():
        context = "No specific syllabus context found. Generate a generic mind map for the topic."
        
    llm = get_llm()
    
    prompt_template = PromptTemplate.from_template(
        "You are an expert curriculum designer. Based on the syllabus context provided below, "
        "generate a detailed, hierarchical mind map for the topic '{topic}' in Mermaid.js flowchart format.\n\n"
        "Syllabus Context:\n{context}\n\n"
        "Instructions:\n"
        "1. Use a clear root node indicating the main topic.\n"
        "2. Include 3-5 primary branches (first level) representing sub-topics.\n"
        "3. Include secondary leaf nodes (second level) detailing concepts or key terms for each sub-topic.\n"
        "4. Start with `graph TD` or `graph LR`.\n"
        "5. Respond ONLY with the raw Mermaid.js graph code. Do not wrap in markdown code blocks, do not explain anything, do not include any other text."
    )
    
    chain = prompt_template | llm
    response = chain.invoke({"topic": topic, "context": context})
    
    # Clean up response content
    content = response.content.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines).strip()
        
    return content
