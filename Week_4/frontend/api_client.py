import json
import requests
import os

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Robust Retry Strategy to prevent WinError 10061 (Connection Refused) crashes.
# NOTE: 500 is intentionally NOT in status_forcelist. A 500 from our backend means the
# Gemini API is rate-limited (429). Retrying it 5 times makes the rate limit far worse.
retry_strategy = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[429, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "DELETE"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http_client = requests.Session()
http_client.mount("http://", adapter)
http_client.mount("https://", adapter)


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def stream_chat_response(message: str, session_id: str):
    """
    Connects to the SSE endpoint and yields tokens.
    """
    url = f"{API_BASE_URL}/chat/stream"
    payload = {
        "user_message": message,
        "session_id": session_id
    }
    
    # We use stream=True to iterate over the response
    with http_client.post(url, json=payload, stream=True, timeout=120) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        data_json = json.loads(data_str)
                        if "token" in data_json:
                            yield data_json["token"]
                        elif "error" in data_json:
                            yield f"\n\n**Error:** {data_json['error']}"
                    except json.JSONDecodeError:
                        continue

def ingest_syllabus(file) -> dict:
    """
    Uploads a PDF file to the ingest endpoint.
    """
    url = f"{API_BASE_URL}/ingest/"
    files = {"file": (file.name, file, "application/pdf")}
    try:
        response = http_client.post(url, files=files, timeout=30)
        if response.status_code != 200:
            try:
                detail = response.json().get("detail", f"Upload failed with status {response.status_code}")
            except Exception:
                detail = f"Upload failed with status {response.status_code}"
            raise Exception(detail)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        raise Exception("File upload timed out. The server may be busy. Please try again later.")
    except Exception as e:
        raise Exception(f"Error uploading syllabus: {e}")

def generate_quiz(topic: str, session_id: str = "default") -> dict:
    """
    Generates a quiz by calling the quiz generation endpoint.
    """
    url = f"{API_BASE_URL}/quiz/generate"
    payload = {"topic": topic, "session_id": session_id}
    try:
        # Increased timeout to handle longer processing times
        response = http_client.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        # Provide a clearer message for timeout issues
        raise Exception("Quiz generation is taking longer than expected. Please try again later.")
    except Exception as e:
        # Propagate other errors with context
        raise Exception(f"Error generating quiz: {e}")

def get_uploaded_files() -> list:
    """
    Retrieves the list of uploaded syllabus files.
    """
    url = f"{API_BASE_URL}/ingest/files"
    response = http_client.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

def get_chat_analytics() -> dict:
    """
    Retrieves topics analysis and curriculum gaps based on student questions.
    """
    url = f"{API_BASE_URL}/chat/analytics"
    try:
        # Extended timeout for heavy analytics computation
        response = http_client.get(url, timeout=120)
        if response.status_code != 200:
            try:
                detail = response.json().get("detail", f"Analytics request failed with status {response.status_code}")
            except Exception:
                detail = f"Analytics request failed with status {response.status_code}"
            raise Exception(detail)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        # Return empty analytics on timeout to keep UI responsive
        return {"top_topics": [], "curriculum_gaps": [], "total_queries": 0, "recent_queries": []}
    except Exception as e:
        raise Exception(f"Error fetching analytics: {e}")

def get_chat_history(session_id: str) -> list:
    """
    Retrieves the persistent conversation history for a given session.
    """
    url = f"{API_BASE_URL}/chat/history/{session_id}"
    response = http_client.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def clear_chat_history(session_id: str) -> dict:
    """
    Deletes the persistent conversation history for a given session.
    """
    url = f"{API_BASE_URL}/chat/history/{session_id}"
    response = http_client.delete(url, timeout=10)
    response.raise_for_status()
    return response.json()

def get_chat_sessions() -> list:
    """
    Retrieves the metadata of all past student chat sessions.
    """
    url = f"{API_BASE_URL}/chat/sessions"
    try:
        # Increased timeout to accommodate potentially longer session retrieval
        response = http_client.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        raise Exception("Fetching chat sessions timed out. Please try again later.")
    except Exception as e:
        raise Exception(f"Error retrieving chat sessions: {e}")

def generate_flashcards(topic: str, session_id: str = "default") -> dict:
    """
    Generates flashcards by calling the flashcards endpoint.
    """
    url = f"{API_BASE_URL}/flashcards/generate"
    payload = {"topic": topic, "session_id": session_id}
    try:
        response = http_client.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        raise Exception("Flashcard generation timed out. Please try again later.")
    except Exception as e:
        raise Exception(f"Error generating flashcards: {e}")

def get_suggested_questions(topic: str) -> list:
    """
    Retrieves a list of suggested questions based on the topic.
    """
    url = f"{API_BASE_URL}/chat/suggest-questions"
    payload = {"topic": topic}
    response = http_client.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

def update_session_metadata(session_id: str, title: str = None, is_pinned: bool = None) -> dict:
    """
    Updates the title or pinned status for a given session.
    """
    url = f"{API_BASE_URL}/chat/session/{session_id}/metadata"
    payload = {}
    if title is not None:
        payload["title"] = title
    if is_pinned is not None:
        payload["is_pinned"] = is_pinned
    response = http_client.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def search_syllabus(query: str) -> list:
    """
    Searches the syllabus using semantic similarity search.
    """
    url = f"{API_BASE_URL}/chat/search"
    params = {"query": query}
    try:
        response = http_client.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Error searching syllabus: {e}")

def generate_mindmap(topic: str, session_id: str = "default") -> dict:
    """
    Generates a concept mind map flowchart in Mermaid.js syntax.
    """
    url = f"{API_BASE_URL}/mindmap/generate"
    payload = {"topic": topic, "session_id": session_id}
    try:
        response = http_client.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        raise Exception("Mind map generation timed out. Please try again later.")
    except Exception as e:
        raise Exception(f"Error generating mind map: {e}")

