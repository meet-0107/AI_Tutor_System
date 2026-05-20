# AI_Tutor_System

This AI tutor transforms course materials into an interactive chat using a strict RAG pipeline. Built with FastAPI, LangChain, and ChromaDB, it provides hallucination-free guidance, source citations, [...]

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

# System Architecture (Week 1 & Week 2)

```text
                            ┌─────────────────────────────────────────────────────────────┐
                            │               WEEK 1: DATA INGESTION                        │
                            └─────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │   PDF Documents      │
                    │   (Course Materials) │
                    └──────────┬───────────┘
                               │
                               v
                    ┌──────────────────────┐
                    │ document_parser.py   │
                    │ - PDF Loading        │
                    │ - Text Chunking      │
                    └──────────┬───────────┘
                               │
                               v
                    ┌──────────────────────────────┐
                    │ vector_store.py              │
                    │ - Embedding Generation       │
                    │   (GoogleGenerativeAI)       │
                    │ - ChromaDB Storage           │
                    └──────────┬───────────────────┘
                               │
                               v
                    ┌──────────────────────────────┐
                    │   ChromaDB                   │
                    │   Vector Database            │
                    │   (Stored Embeddings)        │
                    └──────────────────────────────┘


                            ┌─────────────────────────────────────────────────────────────┐
                            │         WEEK 2: RAG ENGINE & CORE API                      │
                            └─────────────────────────────────────────────────────────────┘

    ┌──────────────────────┐                              ┌─────────────────────────┐
    │  User Query/Chat     │──────────────────────────>  │   FastAPI Backend       │
    │  Request             │        HTTP Request          │   (Week_2/main.py)      │
    └──────────────────────┘                              ├─────────────────────────┤
                                                          │  API Routes:            │
                                                          │  - /chat                │
                                                          │  - /ingest              │
                                                          │  - /schemas             │
                                                          └────────────┬────────────┘
                                                                       │
                                                                       v
                                                          ┌─────────────────────────┐
                                                          │   RAG Engine Core       │
                                                          ├─────────────────────────┤
                                                          │  1. Semantic Search     │
                                                          │     (ChromaDB Query)    │
                                                          │  2. Prompt Building     │
                                                          │  3. LLM Generation      │
                                                          │     (Gemini via LC)     │
                                                          │  4. Response with       │
                                                          │     Citations           │
                                                          └────────────┬────────────┘
                                                                       │
                                                                       v
                                                          ┌─────────────────────────┐
                                                          │   LangChain Framework   │
                                                          ├─────────────────────────┤
                                                          │  - Vector Retriever     │
                                                          │  - Prompt Templates     │
                                                          │  - LLM Integration      │
                                                          └────────────┬────────────┘
                                                                       │
                                                                       v
                                                          ┌─────────────────────────┐
                                                          │   Gemini LLM API        │
                                                          │   (Google AI)           │
                                                          └────────────┬────────────┘
                                                                       │
                                                                       v
                                                          ┌─────────────────────────┐
                                                          │   Generated Response    │
                                                          │   + Source Citations    │
                                                          └─────────────────────────┘
                                                                       ^
                                                                       │
                                                                       │ Retrieves Context
                                                                       │
                                                          ┌─────────────────────────┐
                                                          │    ChromaDB             │
                                                          │    Vector Database      │
                                                          │   (From Week 1)         │
                                                          └─────────────────────────┘
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
