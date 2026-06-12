import os
import json
import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import SystemMessage, HumanMessage
from Week_2.api.schemas.api_models import ChatRequest, ChatResponse
from Week_2 import get_rag_chain, get_llm
from Week_3 import get_rag_chain_with_memory
from Week_4 import generate_chat_stream

router = APIRouter(
    prefix="/chat",
    tags=["Chat Interface"]
)

_memory_chain = None

def get_cached_memory_chain():
    """Lazily initializes and caches the memory chain."""
    global _memory_chain
    if _memory_chain is None:
        rag_chain = get_rag_chain()
        _memory_chain = get_rag_chain_with_memory(rag_chain)
    return _memory_chain

def atomic_write_json(file_path: str, data: dict | list):
    """Writes JSON data to a file atomically using a temp file and explicit UTF-8 encoding."""
    temp_path = file_path + ".tmp"
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        os.replace(temp_path, file_path)
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        raise e

def log_student_query(query: str, session_id: str):
    """Logs the student's question to a local file for analytics purposes."""
    try:
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files'))
        os.makedirs(data_dir, exist_ok=True)
        queries_file = os.path.join(data_dir, 'student_queries.json')
        
        queries = []
        if os.path.exists(queries_file):
            try:
                with open(queries_file, "r", encoding="utf-8") as f:
                    queries = json.load(f)
            except (json.JSONDecodeError, ValueError) as parse_err:
                print(f"[WARN] student_queries.json is corrupted ({parse_err}), starting fresh.")
                queries = []
        
        queries.append({
            "query": query,
            "session_id": session_id,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Keep last 1000 queries to prevent file bloat
        if len(queries) > 1000:
            queries = queries[-1000:]
            
        atomic_write_json(queries_file, queries)
        print(f"[DEBUG] Logged student query to {queries_file}: {query} (session {session_id})")
    except Exception as e:
        import traceback
        print(f"[ERROR] Failed to log student query: {e}")
        traceback.print_exc()

def save_chat_message(session_id: str, role: str, content: str | dict | list, msg_type: str = "text"):
    """Saves a single message (user or assistant) to a persistent JSON registry and updates session metadata."""
    try:
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files'))
        os.makedirs(data_dir, exist_ok=True)
        convs_file = os.path.join(data_dir, 'student_conversations.json')
        
        convs = {}
        if os.path.exists(convs_file):
            try:
                with open(convs_file, "r", encoding="utf-8") as f:
                    convs = json.load(f)
                if not isinstance(convs, dict):
                    print(f"[WARN] student_conversations.json contained {type(convs).__name__} instead of dict, resetting.")
                    convs = {}
            except (json.JSONDecodeError, ValueError) as parse_err:
                print(f"[WARN] student_conversations.json is corrupted ({parse_err}), starting fresh.")
                convs = {}
                
        if session_id not in convs:
            convs[session_id] = []
            
        message_entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if msg_type != "text":
            message_entry["type"] = msg_type
            
        convs[session_id].append(message_entry)
        
        atomic_write_json(convs_file, convs)
        
        # Verify write succeeded by checking file exists and is non-empty
        if not os.path.exists(convs_file) or os.path.getsize(convs_file) == 0:
            print(f"[ERROR] student_conversations.json write verification failed! File missing or empty.")
        else:
            print(f"[DEBUG] Saved chat message for session {session_id} (role: {role}, file size: {os.path.getsize(convs_file)} bytes)")

        # Update session metadata immediately
        meta_file = os.path.join(data_dir, 'session_metadata.json')
        meta = {}
        if os.path.exists(meta_file):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except (json.JSONDecodeError, ValueError):
                print(f"[WARN] session_metadata.json is corrupted, starting fresh.")
                meta = {}

        if session_id not in meta:
            title = "New Chat"
            if role == "user":
                title = content[:30] + "..." if len(content) > 30 else content
            meta[session_id] = {
                "title": title,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_pinned": False
            }
        else:
            # Update the latest activity timestamp
            meta[session_id]["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # If the title is still "New Chat" and we now have a user message, update the title
            if meta[session_id].get("title") == "New Chat" and role == "user":
                meta[session_id]["title"] = content[:30] + "..." if len(content) > 30 else content
                
        atomic_write_json(meta_file, meta)
            
    except Exception as e:
        import traceback
        print(f"[ERROR] Failed to save chat message (session={session_id}, role={role}): {e}")
        traceback.print_exc()

def query_guardrail(query: str) -> bool:
    """
    Custom middleware function to analyze the query before passing to the RAG chain.
    If the query is completely off-topic (not related to education or the syllabus),
    it blocks the execution.
    Returns True (allow) if the LLM check itself fails (fail-safe: never crash the chat).
    """
    try:
        query_lower = query.lower()
        
        # Bypass guardrail if the query contains clear educational terms
        academic_keywords = [
            "explain", "what is", "how to", "why", "define", "regression", 
            "model", "algorithm", "concept", "syllabus", "course", "tutor",
            "study", "learn", "teach", "curriculum", "ai", "ml", "neural", "network"
        ]
        if any(ac in query_lower for ac in academic_keywords):
            return True
            
        # Match whole words for spam keywords to prevent false positives in compound words
        import re
        words = set(re.findall(r'\b\w+\b', query_lower))
        
        spam_keywords = [
            "joke", "recipe", "hack", "malware", "movie", "song", "cricket", 
            "football", "weather", "girlfriend", "boyfriend", "dating"
        ]
        
        for spam in spam_keywords:
            if spam in words:
                return False
                
        return True
    except Exception as e:
        print(f"[Guardrail] Error: {e}")
        return True

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Accepts a student's message, retrieves context from the syllabus, 
    and returns a Socratic response from the AI tutor with conversation history.
    """
    try:
        # Log student query for analytics
        log_student_query(request.user_message, request.session_id)
        
        # Pre-load session history from disk before writing user message to prevent double-logging
        from Week_3.core.memory import get_session_history
        get_session_history(request.session_id)
        
        # Save user message to persistent conversations list
        save_chat_message(request.session_id, "user", request.user_message)
        
        # 1. Custom Middleware Guardrail
        if not query_guardrail(request.user_message):
            rejection_msg = "I am locked to your Course Curriculum and only ask your syllabus question. Please ask questions related to your syllabus."
            save_chat_message(request.session_id, "assistant", rejection_msg)
            return ChatResponse(response=rejection_msg)
        
        # 2. Proceed to Vector Database Search and RAG Chain
        memory_chain = get_cached_memory_chain()
        answer = memory_chain.invoke(
            {"question": request.user_message, "chat_history": []}, 
            config={"configurable": {"session_id": request.session_id}}
        )
        
        # Save assistant response
        save_chat_message(request.session_id, "assistant", answer)
        
        return ChatResponse(response=answer)
    except Exception as e:
        # Catch unexpected errors to prevent the API from crashing completely
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    Accepts a student's message and streams the AI's response token-by-token using SSE.
    """
    try:
        # Log student query
        log_student_query(request.user_message, request.session_id)
        
        # Pre-load session history from disk before writing user message to prevent double-logging
        from Week_3.core.memory import get_session_history
        get_session_history(request.session_id)
        
        # Save user message to persistent conversations list
        save_chat_message(request.session_id, "user", request.user_message)
        
        # 1. Custom Middleware Guardrail
        if not query_guardrail(request.user_message):
            rejection_msg = "I am locked to your Course Curriculum and only ask your syllabus question. Please ask questions related to your syllabus."
            save_chat_message(request.session_id, "assistant", rejection_msg)
            
            # Create a simple generator that yields the rejection message in SSE format and stops
            async def sync_generator():
                import json
                yield f"data: {json.dumps({'token': rejection_msg})}\n\n"
                yield "data: [DONE]\n\n"
                
            return StreamingResponse(
                sync_generator(),
                media_type="text/event-stream"
            )
            
        # Callback to save assistant response on completion
        def save_response(full_response: str):
            save_chat_message(request.session_id, "assistant", full_response)
            
        # Return a StreamingResponse utilizing the generator from stream_handler
        memory_chain = get_cached_memory_chain()
        return StreamingResponse(
            generate_chat_stream(memory_chain, request.user_message, request.session_id, on_completion=save_response),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
def get_chat_history_endpoint(session_id: str):
    """
    Returns the persistent conversation history for a given session ID.
    """
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files'))
    convs_file = os.path.join(data_dir, 'student_conversations.json')
    if not os.path.exists(convs_file) or os.path.getsize(convs_file) == 0:
        return []
    try:
        with open(convs_file, "r", encoding="utf-8") as f:
            convs = json.load(f)
        if isinstance(convs, dict):
            return convs.get(session_id, [])
        return []
    except (json.JSONDecodeError, ValueError) as parse_err:
        print(f"[WARN] student_conversations.json is corrupted ({parse_err}) in get_chat_history_endpoint.")
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history/{session_id}")
def clear_chat_history_endpoint(session_id: str):
    """
    Clears the persistent conversation history, metadata, and student query logs for a given session ID from disk and active memory.
    """
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files'))
    convs_file = os.path.join(data_dir, 'student_conversations.json')
    meta_file = os.path.join(data_dir, 'session_metadata.json')
    queries_file = os.path.join(data_dir, 'student_queries.json')
    
    # 1. Clear active LangChain chat history memory
    try:
        from Week_3.core.memory import store
        if session_id in store:
            del store[session_id]
    except Exception as mem_err:
        print(f"Error clearing memory store: {mem_err}")
            
    # 2. Clear from conversation history disk storage
    if os.path.exists(convs_file):
        try:
            with open(convs_file, "r", encoding="utf-8") as f:
                convs = json.load(f)
            if session_id in convs:
                del convs[session_id]
                atomic_write_json(convs_file, convs)
                # Also remove related queries for this session
                if os.path.exists(queries_file):
                    try:
                        with open(queries_file, "r", encoding="utf-8") as f:
                            queries = json.load(f)
                        queries = [q for q in queries if q.get("session_id") != session_id]
                        atomic_write_json(queries_file, queries)
                    except Exception as e:
                        print(f"Error clearing queries for session {session_id}: {e}")
        except Exception as e:
            print(f"Error clearing conversation history for session {session_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error clearing conversations: {str(e)}")
            
    # 3. Clear from session metadata disk storage
    if os.path.exists(meta_file):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            if session_id in meta:
                del meta[session_id]
                atomic_write_json(meta_file, meta)
        except Exception as e:
            print(f"Error clearing metadata for session {session_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error clearing metadata: {str(e)}")

    # 4. Clear matching student query logs from student_queries.json
    if os.path.exists(queries_file):
        try:
            with open(queries_file, "r", encoding="utf-8") as f:
                queries = json.load(f)
            filtered_queries = [q for q in queries if q.get("session_id") != session_id]
            if len(filtered_queries) < len(queries):
                atomic_write_json(queries_file, filtered_queries)
        except Exception as e:
            print(f"Error clearing query logs for session {session_id}: {e}")

    return {"status": "success", "message": f"History, metadata, and queries cleared for session {session_id}"}
            
@router.get("/search")
def search_endpoint(query: str):
    """
    Search syllabus using similarity search in Pinecone.
    """
    try:
        from Week_1.vector_store import get_vector_store
        vector_store = get_vector_store()
        results = vector_store.similarity_search_with_score(query, k=4)
        
        serialized = []
        for doc, score in results:
            serialized.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })
        return serialized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics")
def get_analytics():
    """
    Analyzes logged student queries using the LLM to identify top topics and curriculum gaps.
    """
    queries_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files', 'student_queries.json'))
    if not os.path.exists(queries_file):
        return {
            "top_topics": [],
            "curriculum_gaps": [],
            "total_queries": 0,
            "recent_queries": []
        }
        
    try:
        with open(queries_file, "r", encoding="utf-8") as f:
            queries = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read queries log: {e}")
        
    total_queries = len(queries)
    recent_queries = queries[-15:]  # Get last 15 queries for displaying in dashboard
    
    if not queries:
        return {
            "top_topics": [],
            "curriculum_gaps": [],
            "total_queries": 0,
            "recent_queries": []
        }
        
    import collections
    import re

    # ── Spam keyword filter (no LLM needed) ─────────────────────────────────
    SPAM_KEYWORDS = [
        "joke", "funny", "laugh", "recipe", "cook", "food", "game", "movie",
        "song", "music", "love", "relationship", "weather", "news", "sport",
        "cricket", "football", "bollywood", "instagram", "tiktok", "youtube",
        "hello", "hi", "hey", "test", "testing", "abc", "xyz", "asdf"
    ]

    def is_spam(q: str) -> bool:
        words = set(re.findall(r'\b\w+\b', q.lower()))
        return any(kw in words for kw in SPAM_KEYWORDS)

    def normalize_query(q: str) -> str:
        """Lowercase, strip punctuation, collapse whitespace."""
        return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', q.lower().strip()))

    # ── Count all queries from the last 500 entries ──────────────────────────
    recent = queries[-500:]
    counter = collections.Counter(
        normalize_query(q["query"]) for q in recent if not is_spam(q["query"])
    )

    # ── Build top_topics: only questions asked 3 OR MORE TIMES, top 7 ──────
    top_topics = []
    for normalized_q, count in counter.most_common(20):
        if count < 3:          # skip if asked less than 3 times
            continue
        if len(top_topics) >= 7:
            break
        # Find the original (non-normalized) question text for display
        original_q = next(
            (q["query"] for q in reversed(recent)
             if normalize_query(q["query"]) == normalized_q and not is_spam(q["query"])),
            normalized_q
        )
        top_topics.append({
            "topic": original_q.strip().rstrip(".").capitalize(),
            "count": count
        })

    # ── Use LLM only for Curriculum Gaps (optional, fail-safe) ───────────────
    curriculum_gaps = []
    try:
        llm = get_llm()
        freq_list_str = "\n".join(
            [f"- '{t['topic']}' (asked {t['count']} times)" for t in top_topics]
        )
        if freq_list_str:
            system_prompt = (
                "You are an EdTech Analytics AI. Based on the most frequently asked student questions below, "
                "identify the top 2-3 curriculum gaps — topics where students seem confused or under-taught. "
                "Reply ONLY with a valid JSON array (no markdown). Schema: "
                "[{\"gap\": \"...\", \"description\": \"...\", \"recommendation\": \"...\"}]"
            )
            human_prompt = "Most asked questions:\n" + freq_list_str
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            content = response.content.strip()
            if content.startswith("```"):
                lines = content.splitlines()
                lines = [l for l in lines if not l.strip().startswith("```")]
                content = "\n".join(lines).strip()
            curriculum_gaps = json.loads(content)
    except Exception as e:
        curriculum_gaps = [{
            "gap": "Analysis Unavailable",
            "description": f"Could not run gap analysis: {e}",
            "recommendation": "Check API connectivity and try refreshing."
        }]

    return {
        "top_topics": top_topics,
        "curriculum_gaps": curriculum_gaps,
        "total_queries": total_queries,
        "recent_queries": recent_queries
    }

from pydantic import BaseModel

class SessionMetadataRequest(BaseModel):
    title: str = None
    is_pinned: bool = None

@router.post("/session/{session_id}/metadata")
def update_session_metadata_endpoint(session_id: str, request: SessionMetadataRequest):
    """
    Updates the title or pinned status for a given session.
    """
    try:
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files'))
        os.makedirs(data_dir, exist_ok=True)
        meta_file = os.path.join(data_dir, 'session_metadata.json')
        
        meta = {}
        if os.path.exists(meta_file):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                pass
                
        if session_id not in meta:
            meta[session_id] = {
                "title": "New Chat",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_pinned": False
            }
            
        if request.title is not None:
            meta[session_id]["title"] = request.title
        if request.is_pinned is not None:
            meta[session_id]["is_pinned"] = request.is_pinned
            
        atomic_write_json(meta_file, meta)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions")
def get_chat_sessions_endpoint():
    """Return list of session metadata quickly without loading full conversations."""
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploaded_files'))
    meta_file = os.path.join(data_dir, 'session_metadata.json')
    convs_file = os.path.join(data_dir, 'student_conversations.json')
    
    # 1. Load metadata safely
    meta = {}
    if os.path.exists(meta_file):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            pass

    # 2. Check student_conversations.json for missing sessions
    convs = {}
    if os.path.exists(convs_file):
        try:
            with open(convs_file, "r", encoding="utf-8") as f:
                convs = json.load(f)
        except Exception:
            pass

    meta_updated = False
    for sid, messages in convs.items():
        if sid not in meta:
            # We found a session that is in conversations but missing in metadata
            title = "New Chat"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Use first user message as title if available
            user_msgs = [m for m in messages if m.get("role") == "user"]
            if user_msgs:
                first_content = user_msgs[0].get("content", "").strip()
                if first_content:
                    title = first_content[:30] + "..." if len(first_content) > 30 else first_content
                timestamp = user_msgs[0].get("timestamp", timestamp)
            elif messages:
                # Fallback to first message overall
                first_content = messages[0].get("content", "").strip()
                if first_content:
                    title = first_content[:30] + "..." if len(first_content) > 30 else first_content
                timestamp = messages[0].get("timestamp", timestamp)
                
            meta[sid] = {
                "title": title,
                "timestamp": timestamp,
                "is_pinned": False
            }
            meta_updated = True

    # 3. Save updated metadata back to file if changes were made
    if meta_updated:
        try:
            atomic_write_json(meta_file, meta)
        except Exception as e:
            print(f"Error saving updated session metadata: {e}")

    # 4. Build sessions list from metadata
    sessions = []
    for sid, info in meta.items():
        title = info.get("title", "New Chat")
        timestamp = info.get("timestamp", "")
        is_pinned = info.get("is_pinned", False)
        sessions.append({
            "session_id": sid,
            "title": title,
            "timestamp": timestamp,
            "is_pinned": is_pinned,
        })
    # Sort by pinned then timestamp descending
    sessions = sorted(sessions, key=lambda x: (x["is_pinned"], x["timestamp"]), reverse=True)
    return sessions

from pydantic import BaseModel

class TopicRequest(BaseModel):
    topic: str

@router.post("/suggest-questions")
def suggest_questions_endpoint(request: TopicRequest):
    """
    Generates 3-5 thought-provoking questions a student could ask about a specific topic.
    """
    try:
        llm = get_llm()
        system_prompt = (
            "You are an EdTech assistant. Given a specific topic, generate 3-5 interesting, "
            "thought-provoking questions a student could ask an AI Tutor to learn more about it.\n"
            "Return strictly a JSON list of strings. Do not include markdown code block formatting (like ```json ... ```), "
            "do not write any conversational text. Respond ONLY with the raw JSON string.\n"
            "Example output: [\"Question 1?\", \"Question 2?\"]"
        )
        human_prompt = f"Topic: {request.topic}"
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])
        
        content = response.content.strip()
        # Clean up markdown code block wrappers if the LLM returned them
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines).strip()
            
        return json.loads(content)
    except Exception as e:
        # Fallback suggestions if LLM fails or returns invalid JSON
        return [
            f"What are the core concepts of {request.topic}?",
            f"Can you explain {request.topic} with a real-world example?",
            f"What are the common pitfalls or limitations of {request.topic}?"
        ]