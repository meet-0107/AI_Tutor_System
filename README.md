# AI_Tutor_System

This AI tutor transforms course materials into an interactive chat using a strict RAG pipeline. Built with FastAPI, LangChain, and ChromaDB, it provides hallucination-free guidance, source citations, conversational memory, token streaming, and dynamic MCQ quizzes for a personalized learning experience.

## 🗂️ Project Structure

```text
AI_Tutor_System/
├── Week_1/                  # Data Ingestion & Vector Database
│   ├── document_parser.py   # PDF loading and text chunking
│   └── vector_store.py      # ChromaDB setup and embedding generation
├── Week_2/                  # RAG Engine & Core API
│   ├── api/                 # FastAPI routes (chat, ingest) and schemas
│   ├── core/                # RAG logic, Prompts, and LLM setup
│   └── main.py              # FastAPI application entry point
├── Week_3/                  # Memory & Quiz Engine
│   ├── api/                 # Quiz generation endpoints
│   └── core/                # Conversation memory and dynamic MCQ generation
├── Week_4/                  # Frontend & Streaming
│   ├── frontend/            # Streamlit application UI (Student/Educator views)
│   └── core/                # Token streaming handlers for real-time chat
├── data_samples/            # Sample documents for testing
├── .env                     # Environment variables (API keys)
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

# System Architecture

┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                       │
├─────────────────────────────────────────────────────────────────────┤
│  Streamlit Frontend                                                │
│  frontend/pages/1_Student_Tutor.py                                │
│                                                                     │
│  • Chat UI                                                          │
│  • Session State                                                    │
│  • Chat History                                                     │
│  • Student Input                                                    │
└───────────────────────┬─────────────────────────────────────────────┘
                        │ HTTP Request
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           FASTAPI BACKEND                          │
├─────────────────────────────────────────────────────────────────────┤
│  main.py                                                            │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ CORS Middleware                                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ API Router                                                   │   │
│  │ api/routers/chat.py                                          │   │
│  │                                                              │   │
│  │ POST /chat                                                   │   │
│  │ ├── Receive User Query                                       │   │
│  │ ├── Call RAG Pipeline                                        │   │
│  │ └── Return AI Response                                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         CORE RAG ENGINE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  core/rag.py                                                        │
│                                                                     │
│  User Question                                                      │
│        │                                                            │
│        ▼                                                            │
│  ┌────────────────────────────┐                                    │
│  │ ChromaDB Retriever         │                                    │
│  │ Retrieve Top 3 Chunks      │                                    │
│  └────────────┬───────────────┘                                    │
│               │                                                    │
│               ▼                                                    │
│  ┌────────────────────────────┐                                    │
│  │ Prompt Builder             │                                    │
│  │                            │                                    │
│  │ • System Prompt            │                                    │
│  │ • Retrieved Context        │                                    │
│  │ • User Question            │                                    │
│  └────────────┬───────────────┘                                    │
│               │                                                    │
│               ▼                                                    │
│  ┌────────────────────────────┐                                    │
│  │ Gemini LLM                 │                                    │
│  │ core/llm.py                │                                    │
│  │                            │                                    │
│  │ Gemini 1.5 Flash / Pro     │                                    │
│  │ temperature = 0            │                                    │
│  └────────────┬───────────────┘                                    │
│               │                                                    │
│               ▼                                                    │
│        Tutor Response                                               │
└───────────────────────┬─────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         VECTOR DATABASE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ChromaDB                                                           │
│  chroma_db/                                                         │
│                                                                     │
│  • Embedded syllabus chunks                                         │
│  • Semantic similarity search                                       │
│  • Persistent local storage                                         │
│                                                                     │
└───────────────────────┬─────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION PIPELINE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PDF Syllabus                                                       │
│        │                                                            │
│        ▼                                                            │
│  PyPDFLoader                                                        │
│        │                                                            │
│        ▼                                                            │
│  RecursiveCharacterTextSplitter                                     │
│  chunk_size = 1000                                                  │
│  chunk_overlap = 200                                                │
│        │                                                            │
│        ▼                                                            │
│  Gemini Embeddings                                                  │
│  (GoogleGenerativeAIEmbeddings)                                     │
│        │                                                            │
│        ▼                                                            │
│  Store vectors in ChromaDB                                          │
└─────────────────────────────────────────────────────────────────────┘


UPDATED TECH STACK
──────────────────────────────────────────────────────────────────────

Frontend:
- Streamlit

Backend:
- FastAPI
- Uvicorn

LLM:
- Gemini API (Google AI)

Framework:
- LangChain

Embeddings:
- GoogleGenerativeAIEmbeddings

Vector Database:
- ChromaDB

PDF Parsing:
- PyPDFLoader