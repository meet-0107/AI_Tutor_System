import json
import asyncio

async def generate_chat_stream(chain, question: str, session_id: str, on_completion=None):
    """
    Asynchronously yields tokens from the RAG chain in Server-Sent Events (SSE) format.
    """
    try:
        full_response = ""
        # We use astream to stream the response token-by-token
        async for chunk in chain.astream(
            {"question": question, "chat_history": []},
            config={"configurable": {"session_id": session_id}}
        ):
            # Handle different types of chunks depending on the output parser
            if isinstance(chunk, str):
                content = chunk
            elif hasattr(chunk, "content"):
                content = chunk.content
            elif isinstance(chunk, dict) and "response" in chunk:
                content = chunk["response"]
            else:
                content = str(chunk)
                
            if content:
                full_response += content
                # SSE format requires sending strings prefixed with 'data: ' and ending with '\n\n'
                # JSON encoding handles escaping newlines and quotes securely
                payload = json.dumps({"token": content})
                yield f"data: {payload}\n\n"
        
        # Trigger completion callback with full accumulated response
        if on_completion:
            try:
                on_completion(full_response)
            except Exception as cb_err:
                print(f"Error in on_completion callback: {cb_err}")
        
        # Yield a final message to indicate completion
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        error_payload = json.dumps({"error": str(e)})
        yield f"data: {error_payload}\n\n"
