# AI_Tutor_System

This AI tutor transforms course materials into an interactive chat using a strict RAG pipeline. Built with FastAPI, LangChain, and ChromaDB, it provides hallucination-free guidance, source citations.

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

## Complete Data Flow & RAG Pipeline

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    WEEK 1 & 2: COMPLETE AI TUTOR PIPELINE                    │
└──────────────────────────────────────────────────────────────────────────────┘

                              DATA INGESTION PHASE (WEEK 1)
                              ════════════════════════════

        ┌──────────────────────┐
        │   PDF Documents      │
        │   (Course Materials) │
        └──────────┬───────────┘
                   │
                   v
        ┌──────────────────────────────────┐
        │  Week_1/document_parser.py       │
        ├──────────────────────────────────┤
        │  • PyPDFLoader (LangChain)       │
        │  • Load PDF pages                │
        │  • Verify file exists            │
        └──────────┬───────────────────────┘
                   │
                   v
        ┌──────────────────────────────────┐
        │  RecursiveCharacterTextSplitter  │
        ├──────────────────────────────────┤
        │  • Chunk Size: 1000 chars        │
        │  • Overlap: 200 chars            │
        │  • Semantic splitting            │
        └──────────┬───────────────────────┘
                   │
                   v
        ┌──────────────────────────────────┐
        │  Week_1/vector_store.py          │
        ├──────────────────────────────────┤
        │  • NomicOllamaEmbeddings         │
        │    (wrapper for nomic-embed-text)│
        │  • Add search prefixes           │
        │  • Filter empty chunks           │
        │  • Initialize Chroma Vector DB   │
        └──────────┬───────────────────────┘
                   │
                   v
        ┌──────────────────────────────────┐
        │   ChromaDB Vector Database       │
        ├──────────────────────────────────┤
        │  • Persistent Storage            │
        │  • Collection: ai_tutor_syllabus │
        │  • Local Path: chroma_db/        │
        │  • Embedded Document Vectors     │
        └──────────────────────────────────┘


                       QUERY & RAG EXECUTION PHASE (WEEK 2)
                       ══════════════════════════════════════

    ┌──────────────────────┐
    │  User Query/Chat     │
    │  Request             │
    │  (from Frontend)     │
    └──────────┬───────────┘
               │
               │ HTTP Request
               v
    ┌──────────────────────────────────────┐
    │     FastAPI Backend                  │
    │     (Week_2/main.py)                 │
    ├──────────────────────────────────────┤
    │  • CORS Middleware                   │
    │  • Allow Frontend Origin             │
    └──────────┬───────────────────────────┘
               │
               v
    ┌──────────────────────────────────────┐
    │     FastAPI Routes                   │
    ├──────────────────────────────────────┤
    │  • /chat (chat_router)               │
    │  • /ingest                           │
    │  • /health                           │
    └──────────┬───────────────────────────┘
               │
               v
    ┌──────────────────────────────────────┐
    │  RAG Engine Core (Week_2/core/)      │
    ├──────────────────────────────────────┤
    │ Step 1: Query Embedding              │
    │ Step 2: Vector Similarity Search     │
    │         (ChromaDB Retrieval)         │
    │ Step 3: Retrieve Context Chunks      │
    │ Step 4: Prompt Construction          │
    │ Step 5: LLM Generation               │
    │ Step 6: Response + Citations         │
    └──────────┬───────────────────────────┘
               │
       ┌───────┴───────────┐
       │                   │
       v                   v
    ┌─────────────────────────────────┐  ┌──────────────────────────┐
    │  LangChain Integration          │  │  ChromaDB Retriever      │
    ├─────────────────────────────────┤  ├──────────────────────────┤
    │  • Vector Retriever             │  │  • Get Query Embeddings  │
    │  • Prompt Templates             │  │  • Similarity Search     │
    │  • LLM Chain Integration        │  │  • Return Top K          │
    │  • Streaming Support            │  │    Relevant Chunks       │
    └──────────┬────────────────────┬─┘  └──────────────────────────┘
               │                    │
               └────────┬───────────┘
                        │
                        v
            ┌────────────────────────────────┐
            │  LLM API Integration           │
            ├────────────────────────────────┤
            │  • LLM Instance (configurable) │
            │  • Prompt: Context + Query     │
            │  • Generate Response           │
            │  • Stream Tokens (if enabled)  │
            └────────────┬───────────────────┘
                         │
                         v
            ┌────────────────────────────────┐
            │  Generated Response            │
            ├────────────────────────────────┤
            │  • Answer to User Query        │
            │  • Source Citations            │
            │  • Confidence/Metadata         │
            └────────────┬───────────────────┘
                         │
                         v
    ┌──────────────────────────────────┐
    │  HTTP Response to Frontend       │
    │  (Streamed or Complete Response) │
    └──────────────────────────────────┘
```

## Complete Data Flow

```text
PDF Input
   │
   ├─> [Document Parser] 
   │   (PyPDFLoader)
   │
   ├─> [Text Chunking]
   │   (RecursiveCharacterTextSplitter)
   │
   ├─> [Embedding Generation]
   │   (NomicOllamaEmbeddings with search prefixes)
   │
   ├─> [Vector Storage]
   │   (ChromaDB persistent database)
   │
   └─> [RAG Pipeline at Query Time]
       │
       ├─> Retrieve relevant chunks from ChromaDB
       ├─> Build context-aware prompt with retrieved chunks
       ├─> Send to LLM for generation
       ├─> Attach source citations
       └─> Return to user via FastAPI
```

## Component Overview

- **Frontend:** Streamlit app for interactive UI (Student/Educator views, chat, quizzes)
- **Backend:** FastAPI with Uvicorn provides REST API for chat, ingestion, and quiz endpoints
- **RAG Engine:** Retrieves context chunks from ChromaDB, constructs prompts, generates responses via LLM with LangChain
- **Vector Database:** ChromaDB stores embedded document vectors and handles semantic search
- **Data Ingestion:** Parses PDF documents, splits text into chunks, computes embeddings with Ollama (nomic-embed-text), and persists in ChromaDB
- **Embeddings:** NomicOllamaEmbeddings wrapper with search prefixes for optimal retrieval

## UPDATED TECH STACK

**Frontend:**
- Streamlit

**Backend:**
- FastAPI
- Uvicorn

**LLM:**
- Configurable (Gemini API or other LLMs via LangChain)

**Framework:**
- LangChain (document loaders, retrievers, chains, integrations)

**Embeddings:**
- Ollama (nomic-embed-text model)
- NomicOllamaEmbeddings (custom wrapper with search prefixes)

**Vector Database:**
- ChromaDB (persistent local storage at `chroma_db/`)

**PDF Parsing:**
- PyPDFLoader (from LangChain)

**Text Splitting:**
- RecursiveCharacterTextSplitter (1000 char chunks with 200 char overlap)
