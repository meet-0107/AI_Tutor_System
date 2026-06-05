import os
import json
import uuid
import shutil
from fastapi.testclient import TestClient

# Import the FastAPI app
from Week_2.main import app

# Import the functions we want to test directly
from Week_2.api.routers.chat import save_chat_message, log_student_query, clear_chat_history_endpoint

# Define the path to the uploaded_files directory
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploaded_files'))
QUERIES_FILE = os.path.join(DATA_DIR, 'student_queries.json')
CONVS_FILE = os.path.join(DATA_DIR, 'student_conversations.json')
META_FILE = os.path.join(DATA_DIR, 'session_metadata.json')

def _load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_storage_persistence(tmp_path):
    """Verify that student queries and conversation messages are persisted correctly.

    The test directly calls the storage helpers to avoid external RAG dependencies.
    """
    # Use a temporary directory for uploaded_files to keep repo clean
    backup_dir = None
    if os.path.isdir(DATA_DIR):
        backup_dir = str(tmp_path / "uploaded_files_backup")
        shutil.copytree(DATA_DIR, backup_dir)
    # Redirect the helpers to a temporary directory for isolation
    # Monkey‑patch the os.path calls inside the helpers by temporarily changing __file__ location is complex;
    # Instead we let the helpers write to the real location but clean up afterwards.
    session_id = str(uuid.uuid4())
    user_msg = "What is the Pythagorean theorem?"
    assistant_msg = "The Pythagorean theorem states that ..."

    # Log query and save messages
    log_student_query(user_msg, session_id)
    save_chat_message(session_id, "user", user_msg)
    save_chat_message(session_id, "assistant", assistant_msg)

    # Verify queries file contains our entry
    queries = _load_json(QUERIES_FILE)
    assert queries is not None, "student_queries.json was not created"
    assert any(q["query"] == user_msg and q["session_id"] == session_id for q in queries)

    # Verify conversation file contains both messages
    convs = _load_json(CONVS_FILE)
    assert convs is not None, "student_conversations.json was not created"
    assert session_id in convs, "Session ID missing in conversations"
    messages = convs[session_id]
    roles = {m["role"] for m in messages}
    assert "user" in roles and "assistant" in roles

    # Cleanup: remove the test session data
    clear_chat_history_endpoint(session_id)
    # Ensure cleanup removed entries
    queries_after = _load_json(QUERIES_FILE) or []
    assert not any(q["session_id"] == session_id for q in queries_after)
    convs_after = _load_json(CONVS_FILE) or {}
    assert session_id not in convs_after

    # Restore original uploaded files if a backup existed
    if backup_dir:
        shutil.rmtree(DATA_DIR)
        shutil.move(backup_dir, DATA_DIR)
