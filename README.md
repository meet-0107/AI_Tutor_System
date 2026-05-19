# AI_Tutor_System

This AI tutor transforms course materials into an interactive chat using a strict RAG pipeline. Built with FastAPI, LangChain, and ChromaDB, it provides hallucination-free guidance, source citations, and quiz generation.

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

```text
+-----------------------+        HTTP Request         +-----------------------+
|  Streamlit Frontend   |  ----------------------->  |    FastAPI Backend    |
+-----------------------+                            +-----------+-----------+
        |                                                    |
        |  User Input, Chat UI,                              |
        |  Session State, Quiz Pages                         |
        |                                                    v
        |                                          +-----------------------+
        +----------------------------------------->|  RAG Engine           |
                                                   +-----------------------+
                                                   | - ChromaDB Retrieval  |
                                                   | - Prompt Building     |
                                                   | - Gemini LLM          |
                                                   +-----------------------+
                                                            |
                                                            v
                                                   +-----------------------+
                                                   |   Vector Database     |
                                                   |   (ChromaDB)         |
                                                   +-----------------------+
                                                            ^
                                                            |
                                                   +-----------------------+
                                                   |  Data Ingestion       |
                                                   |  (PDF Parsing,        |
                                                   |   Embeddings)         |
                                                   +-----------------------+
```

## Component Overview
- **Frontend:** Streamlit app for interactive UI (Student/Educator views, chat, quizzes)
- **Backend:** FastAPI provides REST API for chat, ingestion, and quiz endpoints
- **RAG Engine:** Retrieves context chunks from ChromaDB, constructs prompts, and uses Gemini LLM via LangChain
- **Vector Database:** ChromaDB stores embedded document vectors and handles semantic search
- **Data Ingestion:** Parsers PDF syllabus, splits text, computes embeddings (GoogleGenerativeAIEmbeddings), stores in ChromaDB

## UPDATED TECH STACK

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
