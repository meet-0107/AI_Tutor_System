# AI_Tutor_System

This AI tutor transforms course materials into an interactive chat using a strict RAG (Retrieval-Augmented Generation) pipeline. Built with **FastAPI**, **LangChain**, **ChromaDB**, and **Streamlit**, it provides hallucination-free guidance, source citations, conversational memory, real-time token streaming, and dynamic MCQ quizzes for a personalized learning experience.

---

## 🗂️ Project Structure

```text
AI_Tutor_System/
├── Week_1/                      # Data Ingestion & Vector Database Setup
│   ├── document_parser.py       # PDF loading and intelligent text chunking
│   ├── vector_store.py          # ChromaDB/Pinecone integration & embeddings
│   └── utils/                   # Helper utilities for data processing
├── Week_2/                      # RAG Engine & FastAPI Backend
│   ├── api/
│   │   ├── chat_router.py       # Chat endpoints (/chat, /chat/stream)
│   │   ├── ingest_router.py     # Document ingestion endpoints
│   │   └── schemas.py           # Pydantic request/response models
│   ├── core/
│   │   ├── rag_engine.py        # RAG pipeline & retrieval logic
│   │   ├── prompts.py           # LLM prompt templates
│   │   ├── llm_setup.py         # LLM configuration (Ollama/OpenAI)
│   │   └── retrievers.py        # Vector store retriever setup
│   └── main.py                  # FastAPI application entry point
├── Week_3/                      # Conversational Memory & Quiz Engine
│   ├── api/
│   │   ├── quiz_router.py       # Quiz endpoints (/quiz/generate, /quiz/submit, etc.)
│   │   └── memory_router.py     # Memory & conversation management endpoints
│   ├── core/
│   │   ├── memory_manager.py    # Conversation memory & session handling
│   │   ├── quiz_generator.py    # Dynamic MCQ generation logic
│   │   ├── distractor_gen.py    # Plausible distractors generation
│   │   └── performance_tracker.py # Quiz analytics & performance metrics
│   └── database/
│       ├── models.py            # SQLAlchemy/ORM models for persistence
│       └── storage.py           # Session & conversation storage
├── Week_4/                      # Frontend & Real-Time Streaming
│   ├── frontend/
│   │   ├── app.py               # Streamlit multipage application
│   │   ├── pages/
│   │   │   ├── student_tutor.py # Student chat interface
│   │   │   ├── educator_dashboard.py # Educator document & quiz management
│   │   │   └── analytics.py     # Learning progress dashboard
│   │   └── components/          # Reusable Streamlit components
│   └── core/
│       ├── stream_handler.py    # SSE & token streaming logic
│       └── ui_helpers.py        # Frontend utility functions
├── data_samples/                # Sample documents for testing
├── .env                         # Environment variables (API keys, models)
├── .env.example                 # Example environment configuration
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Docker orchestration (optional)
├── Dockerfile                   # Container image (optional)
└── README.md                    # Project documentation
```

---

## 🏗️ System Architecture

### Complete Data Flow & Integrated Pipeline (Weeks 1-4)

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│         WEEKS 1-4: COMPLETE AI TUTOR SYSTEM WITH STREAMING FRONTEND          │
└──────────────────────────────────────────────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════════╗
║                  WEEK 1: DATA INGESTION & VECTORIZATION                        ║
╚════════════════════════════════════════════════════════════════════════════════╝

        ┌─────────────────────────────┐
        │  PDF Documents              │
        │  (Course Materials)         │
        └──────────────┬──────────────┘
                       │
                       v
        ┌──────────────────────────────────────┐
        │  Week_1/document_parser.py           │
        ├──────────────────────────────────────┤
        │  ✓ PyPDFLoader (LangChain)           │
        │  ✓ Extract pages & text             │
        │  ✓ Validation & error handling      │
        └──────────────┬──────────────────────┘
                       │
                       v
        ┌──────────────────────────────────────┐
        │  RecursiveCharacterTextSplitter      │
        ├──────────────────────────────────────┤
        │  ✓ Chunk Size: 1000 chars           │
        │  ✓ Overlap: 200 chars               │
        │  ✓ Semantic boundary preservation    │
        │  ✓ Empty chunk filtering             │
        └──────────────┬──────────────────────┘
                       │
                       v
        ┌──────────────────────────────────────┐
        │  Week_1/vector_store.py              │
        ├──────────────────────────────────────┤
        │  ✓ Embedding Generation              │
        │  ✓ Batch processing                 │
        │  ✓ Add metadata (source, page)      │
        │  ✓ Initialize Vector Store           │
        └──────────────┬──────────────────────┘
                       │
                       v
        ┌──────────────────────────────────────┐
        │   ChromaDB / Pinecone Vector Store   │
        ├──────────────────────────────────────┤
        │  ✓ Cloud/Local vector storage        │
        │  ✓ Index: ai_tutor_documents        │
        │  ✓ Embedded vectors with metadata   │
        │  ✓ Fast similarity search capability │
        └──────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════════╗
║                    WEEK 2: RAG ENGINE & QUERY PROCESSING                       ║
╚════════════════════════════════════════════════════════════════════════════════╝

    ┌──────────────────────────────────┐
    │  User Query / Chat Message       │
    │  (from Streamlit Frontend)       │
    └──────────────┬───────────────────┘
                   │
                   │ HTTP Request via FastAPI
                   v
    ┌──────────────────────────────────────────┐
    │  FastAPI Backend (Week_2/main.py)        │
    ├──────────────────────────────────────────┤
    │  ✓ CORS Middleware                       │
    │  ✓ Request validation (Pydantic)        │
    │  ✓ Authentication (optional)             │
    │  ✓ Logging & monitoring                 │
    └──────────────┬───────────────────────────┘
                   │
                   v
    ┌──────────────────────────────────────────┐
    │  FastAPI Routers (Week_2/api/)           │
    ├──────────────────────────────────────────┤
    │  ✓ /chat/complete (standard response)    │
    │  ✓ /chat/stream (streaming response)     │
    │  ✓ /ingest (document upload)             │
    │  ✓ /health (system status)               │
    │  ✓ /quiz/* (Week_3 quiz endpoints)       │
    │  ✓ /memory/* (conversation endpoints)    │
    └──────────────┬───────────────────────────┘
                   │
                   v
    ┌──────────────────────────────────────────┐
    │  RAG Engine Core (Week_2/core/)          │
    ├──────────────────────────────────────────┤
    │  Step 1: Embed user query                │
    │  Step 2: Semantic similarity search      │
    │          (Vector store retrieval)        │
    │  Step 3: Retrieve top-K context chunks   │
    │  Step 4: Construct prompt with context   │
    │  Step 5: Stream/generate LLM response    │
    │  Step 6: Format response + citations     │
    └──────────────┬───────────────────────────┘
                   │
        ┌──────────┼──────────┬──────────────┐
        │          │          │              │
        v          v          v              v
    ┌────────────────────┐ ┌──────────────────┐ ┌────────────────────┐
    │ Embedding Model    │ │ Vector Retriever │ │ LLM Engine         │
    ├────────────────────┤ ├──────────────────┤ ├────────────────────┤
    │ ✓ Sentence         │ │ ✓ ChromaDB/      │ │ ✓ Ollama/OpenAI    │
    │   Transformers     │ │   Pinecone       │ │ ✓ LangChain        │
    │ ✓ Query encoding   │ │ ✓ Similarity     │ │   integration      │
    │ ✓ Batch processing │ │   search         │ │ ✓ Token streaming  │
    │                    │ │ ✓ Top-K ranking  │ │ ✓ Temperature      │
    │                    │ │ ✓ Metadata       │ │   control          │
    │                    │ │   filtering      │ │                    │
    └────────────────────┘ └──────────────────┘ └────────────────────┘
        │                       │                      │
        └───────────────────────┼──────────────────────┘
                                │
                    ┌───────────v──────────────┐
                    │  Prompt Template Engine   │
                    ├───────────────────────────┤
                    │  ✓ System instructions    │
                    │  ✓ Retrieved context      │
                    │  ✓ Conversation history  │
                    │  ✓ Few-shot examples      │
                    │  ✓ Source citation format │
                    └───────────┬───────────────┘
                                │
                                v
                    ┌───────────────────────────┐
                    │  Response Generation      │
                    ├───────────────────────────┤
                    │  ✓ LLM token generation   │
                    │  ✓ Real-time streaming    │
                    │  ✓ Citation extraction    │
                    │  ✓ Quality validation     │
                    └───────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════════╗
║              WEEK 3: CONVERSATIONAL MEMORY & DYNAMIC QUIZ ENGINE                ║
╚════════════════════════════════════════════════════════════════════════════════╝

    CONVERSATION MEMORY FLOW:
    ═════════════════════════

    ┌────────────────────────────────┐
    │  User Message → Chat Endpoint  │
    └──────────────┬─────────────────┘
                   │
                   v
    ┌────────────────────────────────────────────┐
    │  Week_3/core/memory_manager.py             │
    ├────────────────────────────────────────────┤
    │  ✓ Session identification                  │
    │  ✓ Retrieve conversation history           │
    │  ✓ Context window management               │
    │  ✓ Semantic similarity ranking             │
    │  ✓ Store new message                       │
    └──────────────┬─────────────────────────────┘
                   │
        ┌──────────┼──────────┬────────────────┐
        │          │          │                │
        v          v          v                v
    ┌────────────┐┌────────────┐ ┌──────────────┐ ┌─────────────────┐
    │ Session DB ││ Message    │ │ Embedding    │ │ Performance     │
    │ Storage    ││ Store      │ │ Similarity   │ │ Metrics         │
    ├────────────┤├────────────┤ ├──────────────┤ ├─────────────────┤
    │ ✓ User ID  ││ ✓ Chat ID  │ │ ✓ Query      │ │ ✓ Quiz scores   │
    │ ✓ Session  ││ ✓ Messages │ │   embeddings │ │ ✓ Concepts      │
    │   ID       ││ ✓ Timestamp│ │ ✓ Response   │ │   mastered      │
    │ ✓ Metadata ││ ✓ Role     │ │   embeddings │ │ ✓ Weak areas    │
    │            ││ ✓ Content  │ │ ✓ Similarity │ │                 │
    │            ││            │ │   scores     │ │                 │
    └────────────┘└────────────┘ └──────────────┘ └─────────────────┘
        │            │              │                 │
        └────────────┼──────────────┼─────────────────┘
                     │
          ┌──────────v──────────────┐
          │ Enhanced Context        │
          │ Assembly               │
          ├───────────────────────┤
          │ ✓ Full conversation   │
          │   thread              │
          │ ✓ Top-K relevant msgs │
          │ ✓ Retrieved chunks    │
          │ ✓ Memory-aug prompt   │
          └──────────────────────┘


    DYNAMIC QUIZ ENGINE FLOW:
    ════════════════════════

    ┌─────────────────────────────┐
    │  Quiz Request from Frontend │
    │  (Topic/Difficulty Level)   │
    └──────────────┬──────────────┘
                   │
                   v
    ┌──────────────────────────────────────────┐
    │  Week_3/core/quiz_generator.py           │
    ├──────────────────────────────────────────┤
    │  ✓ Query vector store for relevant docs  │
    │  ✓ Filter by topic & difficulty          │
    │  ✓ Concept extraction                    │
    │  ✓ Question generation strategy          │
    └──────────────┬───────────────────────────┘
                   │
        ┌──────────┼────────┬──────────┬─────────────┐
        │          │        │          │             │
        v          v        v          v             v
    ┌────────────┐┌────────────┐ ┌───────────┐ ┌─────────────┐ ┌──────────┐
    │ Concept    ││ Question   │ │ Distractors
    │ Selection  ││ Crafting   │ │ Generation│ │ Validation  │ │ Ranking  │
    ├────────────┤├────────────┤ ├───────────┤ ├─────────────┤ ├──────────┤
    │ ✓ Extract  ││ ✓ LLM-based│ │ ✓ Generate│ │ ✓ Check Ans │ │ ✓ Score  │
    │   key      ││   Q generat│ │   wrong   │ │   validity  │ │  plausib │
    │   topics   ││ ✓ Include  │ │ ✓ Similar │ │ ✓ Grammar   │ │ ✓ Order  │
    │ ✓ Difficulty ││   context  │ │   to      │ │   check     │ │   options│
    │   selection ││ ✓ Grammar  │ │   correct │ │ ✓ Format    │ │ ✓ Shuffle│
    │ ✓ Sample   ││   check    │ │   answer  │ │   valid     │ │          │
    │   size     ││            │ │ ✓ Randomiz│ │             │ │          │
    │   selection││            │ │   order   │ │             │ │          │
    └────────────┘└────────────┘ └───────────┘ └─────────────┘ └──────────┘
        │            │               │              │              │
        └────────────┼───────────────┼──────────────┼──────────────┘
                     │
                     v
            ┌─────────────────────────┐
            │  Quiz Output Object     │
            ├─────────────────────────┤
            │ ✓ Questions (5 options) │
            │ ✓ Correct answers       │
            │ ✓ Explanations          │
            │ ✓ Source citations      │
            │ ✓ Difficulty level      │
            │ ✓ Est. time             │
            │ ✓ Topic tags            │
            └────────┬────────────────┘
                     │
                     v
            ┌─────────────────────────┐
            │  Week_3/api/            │
            │  quiz_router.py         │
            ├─────────────────────────┤
            │ ✓ /quiz/generate        │
            │ ✓ /quiz/submit          │
            │ ✓ /quiz/history         │
            │ ✓ /quiz/performance     │
            │ ✓ /quiz/analytics       │
            └────────┬────────────────┘
                     │
                     v
            ┌─────────────────────────┐
            │  Results & Analytics    │
            ├─────────────────────────┤
            │ ✓ Score calculation     │
            │ ✓ Performance metrics   │
            │ ✓ Weakness ID           │
            │ ✓ Personalized tips     │
            │ ✓ Progress tracking     │
            └─────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════════╗
║              WEEK 4: FRONTEND UI & REAL-TIME STREAMING                         ║
╚════════════════════════════════════════════════════════════════════════════════╝

    STREAMLIT FRONTEND ARCHITECTURE:
    ════════════════════════════════

    ┌─────────────────────────────────────────┐
    │      Streamlit Multipage App            │
    │      (Week_4/frontend/app.py)           │
    └────────────────┬────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        v            v            v
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Student      │ │ Educator     │ │ Analytics    │
    │ Tutor        │ │ Dashboard    │ │ Dashboard    │
    │ (pages/      │ │ (pages/      │ │ (pages/      │
    │ student_     │ │ educator_    │ │ analytics.py)│
    │ tutor.py)    │ │ dashboard.py)│ │              │
    ├──────────────┤ ├──────────────┤ ├──────────────┤
    │ ✓ Chat UI    │ │ ✓ PDF        │ │ ✓ Progress   │
    │ ✓ Message    │ │   upload     │ │   charts     │
    │   display    │ │ ✓ Ingestion  │ │ ✓ Quiz stats │
    │ ✓ Streaming  │ │   status     │ │ ✓ Weak areas │
    │   responses  │ │ ✓ Quiz       │ │ ✓ Compare    │
    │ ✓ Quiz page  │ │   generation │ │   progress   │
    │ ✓ History    │ │ ✓ Quiz mgmt  │ │ ✓ Export     │
    │ ✓ Settings   │ │ ✓ Vector DB  │ │   reports    │
    │              │ │   stats      │ │              │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            v
                ┌───────────────────────────┐
                │  HTTP Client Request      │
                │  (FastAPI Endpoints)      │
                └───────────┬───────────────┘
                            │
    ┌───────────────────────┼───────────────────────┐
    │                       │                       │
    v                       v                       v
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Standard Chat    │ │ Stream Chat      │ │ Quiz/Memory      │
│ Endpoints        │ │ Endpoints        │ │ Endpoints        │
│ /chat/complete   │ │ /chat/stream     │ │ /quiz/*          │
│                  │ │                  │ │ /memory/*        │
│ Response: JSON   │ │ Response: SSE    │ │                  │
│ (Complete text)  │ │ (Token stream)   │ │ Response: JSON   │
└────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                    │                    │
         │      ┌─────────────v──────────────┐     │
         │      │  Uvicorn Server            │     │
         │      │  (Async Event Loop)        │     │
         │      └─────────────┬──────────────┘     │
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                ┌─────────────v──────────────┐
                │  Backend Services Layer    │
                │  (RAG + Memory + Quiz)     │
                └────────────────────────────┘


    TOKEN STREAMING FLOW (SSE):
    ═══════════════════════════

    Client (Streamlit)           Backend (FastAPI)
    ─────────────────────────    ──────────────────
           │                           │
           │  GET /chat/stream         │
           │  (with message)           │
           ├──────────────────────────>│
           │                           │
           │                    ┌──────v──────┐
           │                    │ RAG Engine  │
           │                    │ executes    │
           │                    │ query       │
           │                    └──────┬──────┘
           │                           │
           │                    ┌──────v──────────────┐
           │                    │ LLM with Streaming  │
           │                    │ (token by token)    │
           │                    └──────┬──────────────┘
           │                           │
           │  SSE: token #1            │
           │<──────────────────────────┤
           │  (delta message)          │
           │  SSE: token #2            │
           │<──────────────────────────┤
           │  SSE: token #3            │
           │<──────────────────────────┤
           │  ... (more tokens) ...    │
           │                           │
           │  SSE: [DONE]              │
           │<──────────────────────────┤
           │  (stream complete)        │
           │                           │

    Real-time UI Update:
    - Display tokens as they arrive
    - Smooth typing animation
    - Show sources as they appear
    - Citations in real-time
```

---

## 🔧 Component Overview

### **Week 1: Data Ingestion & Vectorization**

**Purpose:** Prepare course materials for retrieval

- **Document Parser** (`Week_1/document_parser.py`)
  - Load PDF documents using PyPDFLoader
  - Extract text with metadata preservation
  - Validate file integrity and encoding
  
- **Text Splitting**
  - RecursiveCharacterTextSplitter: 1000 char chunks, 200 char overlap
  - Maintains semantic boundaries between chunks
  - Filters empty/whitespace-only segments

- **Embedding Generation**
  - Converts text chunks into vector embeddings
  - Supports: Sentence Transformers, OpenAI embeddings
  - Batch processing for efficiency

- **Vector Storage** (`Week_1/vector_store.py`)
  - ChromaDB (local) or Pinecone (cloud)
  - Index: `ai_tutor_documents`
  - Stores embeddings + metadata (source, page, chunk_id)
  - Enables fast similarity search

---

### **Week 2: RAG Engine & Query Processing**

**Purpose:** Retrieve relevant context and generate responses

- **FastAPI Backend** (`Week_2/main.py`)
  - Uvicorn ASGI server for async processing
  - CORS middleware for frontend communication
  - Request validation with Pydantic models
  - Structured logging & error handling

- **Chat Routers** (`Week_2/api/chat_router.py`)
  - `POST /chat/complete` → Standard response (full text)
  - `GET /chat/stream` → Streaming response (token-by-token via SSE)
  - Both endpoints support conversation context

- **RAG Engine** (`Week_2/core/rag_engine.py`)
  1. **Query Embedding:** Convert user message to vector
  2. **Similarity Search:** Query vector store for top-K chunks
  3. **Context Assembly:** Combine retrieved chunks into context window
  4. **Prompt Construction:** Build system prompt + context + query
  5. **LLM Generation:** Stream/generate response via LLM
  6. **Citation Extraction:** Parse and format source references

- **Prompt Templates** (`Week_2/core/prompts.py`)
  - System instructions for RAG-compliant behavior
  - Context injection points
  - Citation format requirements
  - Few-shot examples for quality control

- **LLM Setup** (`Week_2/core/llm_setup.py`)
  - Support for Ollama (local) and OpenAI/Claude (cloud)
  - Temperature and max_tokens configuration
  - Token streaming callback handlers

---

### **Week 3: Conversational Memory & Quiz Engine**

**Purpose:** Maintain context across conversations and generate assessments

#### **Conversational Memory System**

- **Memory Manager** (`Week_3/core/memory_manager.py`)
  - Per-user/per-session conversation threads
  - Semantic similarity-based context retrieval
  - Intelligent context window management (token budgeting)
  - Summary generation for long conversations

- **Session Storage** (`Week_3/database/storage.py`)
  - Persist conversations with timestamps
  - Store user metadata and session info
  - Support for multiple concurrent sessions
  - Query history and search capabilities

- **Context Window Management**
  - Maintains conversation history within token limits
  - Ranks messages by relevance using embeddings
  - Selects most important historical messages
  - Balances history depth vs. current query focus

#### **Dynamic MCQ Quiz Engine**

- **Quiz Generator** (`Week_3/core/quiz_generator.py`)
  - Retrieves relevant course materials
  - Selects concepts based on difficulty level
  - Generates natural language questions using LLM
  - Validates answer correctness

- **Distractor Generation** (`Week_3/core/distractor_gen.py`)
  - Creates plausible but incorrect alternatives
  - Maintains semantic similarity to correct answer
  - Prevents obviously wrong options
  - Randomizes option order

- **Difficulty Levels**
  - **Easy:** Foundational concepts, recall-based
  - **Medium:** Application-level thinking
  - **Hard:** Synthesis and analysis

- **Performance Tracking** (`Week_3/core/performance_tracker.py`)
  - Records quiz attempts with scores
  - Identifies weak knowledge areas
  - Tracks improvement over time
  - Generates personalized recommendations

- **Quiz API Endpoints** (`Week_3/api/quiz_router.py`)
  - `POST /quiz/generate` → Create new quiz
  - `POST /quiz/submit` → Submit answers & get results
  - `GET /quiz/history` → Retrieve past quizzes
  - `GET /quiz/performance` → Analytics dashboard data

---

### **Week 4: Frontend UI & Real-Time Streaming**

**Purpose:** Provide interactive user interfaces with real-time updates

#### **Streamlit Frontend** (`Week_4/frontend/app.py`)

**Multipage Application:**

1. **Student Tutor** (`pages/student_tutor.py`)
   - Chat interface with real-time message display
   - Streaming token visualization
   - Message history with citations
   - Quiz interface with difficulty selection
   - Performance tracking dashboard

2. **Educator Dashboard** (`pages/educator_dashboard.py`)
   - PDF document upload & ingestion
   - Vector store management
   - Quiz creation & customization
   - Student analytics & insights
   - Content performance metrics

3. **Analytics Dashboard** (`pages/analytics.py`)
   - Student progress charts
   - Quiz performance analytics
   - Learning gap identification
   - Trend analysis & predictions
   - Exportable reports

#### **Token Streaming** (`Week_4/core/stream_handler.py`)

- **Server-Sent Events (SSE)**
  - Asynchronous generator yields tokens in real-time
  - Maintains HTTP connection for live updates
  - Fallback to polling if SSE unavailable

- **Frontend Integration**
  - Streamlit `st.write()` updates as tokens arrive
  - Loading animation during stream
  - Automatic scroll to latest message
  - Error handling & retry logic

---

## 💻 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Interactive web UI with multipage support |
| **Backend** | FastAPI + Uvicorn | Async REST API server |
| **LLM Framework** | LangChain | Orchestration, retrieval, chains |
| **Vector DB** | ChromaDB / Pinecone | Semantic search & embeddings storage |
| **Embeddings** | Sentence Transformers / OpenAI | Text vectorization |
| **PDF Processing** | PyPDFLoader | Document ingestion |
| **Text Splitting** | RecursiveCharacterTextSplitter | Semantic chunking |
| **LLM Engines** | Ollama / OpenAI / Claude | Text generation |
| **Data Storage** | SQLite / PostgreSQL | Conversation & quiz persistence |
| **Async** | asyncio | Concurrent request handling |
| **Language** | Python 3.8+ | Core language |

---

## ✨ Key Features

| Feature | Description | Week |
|---------|-------------|------|
| **RAG Pipeline** | Strict retrieval-augmented generation with source tracking | W1-W2 |
| **Hallucination-Free** | Responses grounded in course materials with citations | W2 |
| **Conversational Memory** | Context-aware responses with semantic history retrieval | W3 |
| **Token Streaming** | Real-time token-by-token response display via SSE | W4 |
| **Dynamic MCQ Quizzes** | Auto-generated quizzes from materials with explanations | W3 |
| **Multi-Role UI** | Separate student tutor and educator dashboard views | W4 |
| **Cloud Vector Store** | Scalable Pinecone integration for production deployments | W1 |
| **Performance Analytics** | Track learning progress and identify knowledge gaps | W3 |
| **Contextual Responses** | Leverage conversation history for relevant answers | W3 |
| **Configurable LLMs** | Support for local (Ollama) and cloud (OpenAI) models | W2 |
| **Environment Security** | Secure API key management via .env files | All |
| **RESTful API** | Well-documented endpoints for extensibility | W2-W3 |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **pip** or **conda** package manager
- **PDF documents** for course materials
- **API Keys** (depending on configuration):
  - Pinecone API key (optional, for cloud vector DB)
  - OpenAI API key (optional, for GPT models)
  - Ollama (optional, for local LLM)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/meet-0107/AI_Tutor_System.git
cd AI_Tutor_System
```

#### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings
```

**Example `.env` configuration:**

```env
# LLM Configuration
LLM_PROVIDER=ollama  # or openai
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral  # or your chosen model

# Vector Database
VECTOR_DB_TYPE=chroma  # or pinecone
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=gcp-starter
PINECONE_INDEX_NAME=ai_tutor_documents

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Frontend
STREAMLIT_PORT=8501

# API Server
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

#### 5. Prepare Data (Optional)

Place PDF documents in `data_samples/`:

```bash
mkdir -p data_samples
# Add your .pdf files here
```

#### 6. Run the Backend

```bash
cd Week_2
python main.py
# Server runs on http://localhost:8000
```

#### 7. Run the Frontend (New Terminal)

```bash
cd Week_4/frontend
streamlit run app.py
# Opens on http://localhost:8501
```

---

## 📖 Usage Guide

### For Students

1. **Chat with AI Tutor**
   - Ask questions about course materials
   - Receive answers with source citations
   - Continue multi-turn conversations
   - See response streaming in real-time

2. **Take Quizzes**
   - Select topic and difficulty level
   - Answer MCQ questions
   - View explanations with sources
   - Track quiz performance

3. **Monitor Progress**
   - View learning analytics
   - Identify weak areas
   - Track improvement over time

### For Educators

1. **Ingest Course Materials**
   - Upload PDF documents
   - Monitor ingestion status
   - View vector store statistics

2. **Manage Content**
   - Create custom quizzes
   - Review student progress
   - Export analytics reports

3. **Analytics Dashboard**
   - Class-level performance metrics
   - Individual student progress
   - Topic mastery analysis

---

## 🔄 API Endpoints

### Chat Endpoints

```
POST /chat/complete
├── Request: { "message": "string", "session_id": "string" }
└── Response: { "answer": "string", "sources": [...], "tokens": int }

GET /chat/stream
├── Query: ?message=...&session_id=...
└── Response: Server-Sent Events (token stream)
```

### Quiz Endpoints

```
POST /quiz/generate
├── Request: { "topic": "string", "difficulty": "easy|medium|hard", "count": int }
└── Response: { "questions": [...], "quiz_id": "string" }

POST /quiz/submit
├── Request: { "quiz_id": "string", "answers": [...] }
└── Response: { "score": float, "results": [...], "feedback": "string" }

GET /quiz/history
├── Query: ?session_id=...&limit=10
└── Response: [{ "quiz_id": "...", "score": ..., "timestamp": ... }]

GET /quiz/performance
├── Query: ?session_id=...
└── Response: { "avg_score": float, "weak_areas": [...], "mastered": [...] }
```

### Ingestion Endpoints

```
POST /ingest
├── Request: multipart/form-data (PDF file)
└── Response: { "status": "success", "chunks_added": int, "vector_ids": [...] }

GET /health
└── Response: { "status": "ok", "vector_db": "connected", "llm": "ready" }
```

---

## 📚 Project Workflow

```
Week 1: Data Pipeline
├── Parse PDFs → Split text → Generate embeddings → Store in vector DB
└── Outcome: Ready-to-query vector database

Week 2: RAG Engine
├── User query → Embed query → Search vectors → Retrieve context
├── Build prompt → Call LLM → Stream response → Add citations
└── Outcome: Functional chat API with streaming

Week 3: Memory & Quizzes
├── Session management → Conversation memory → Context-aware responses
├── Quiz generation → MCQ creation → Performance tracking
└── Outcome: Enhanced chat with memory + quiz system

Week 4: Frontend
├── Streamlit UI → Chat interface → Quiz interface → Analytics dashboard
├── Token streaming → Real-time display → Educator tools
└── Outcome: Complete production-ready system
```

---

## 🧪 Testing

### Unit Tests

```bash
pytest tests/unit/ -v
```

### Integration Tests

```bash
pytest tests/integration/ -v
```

### End-to-End Tests

```bash
pytest tests/e2e/ -v
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Vector DB connection fails | Check `.env` credentials and network connectivity |
| LLM not responding | Verify Ollama is running or OpenAI API key is valid |
| PDF ingestion errors | Ensure PDFs are valid and not corrupted |
| Slow vector search | Increase vector DB index resolution or use Pinecone |
| Streamlit connection refused | Check FastAPI backend is running on correct port |

---

## 📈 Performance Optimization

1. **Vector Search:** Use Pinecone for production (cloud-managed scalability)
2. **Batch Processing:** Process multiple PDFs simultaneously
3. **Caching:** Cache frequent queries and responses
4. **Async I/O:** Leverage FastAPI's async capabilities
5. **Model Selection:** Use smaller embeddings for speed vs. larger for accuracy

---

## 🤝 Contributing

Contributions welcome! Follow these steps:

1. **Fork** the repository
2. **Create feature branch:** `git checkout -b feature/your-feature`
3. **Commit changes:** `git commit -m "Add your feature"`
4. **Push to branch:** `git push origin feature/your-feature`
5. **Open Pull Request**

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🎓 Learning Resources

- [LangChain Documentation](https://langchain.readthedocs.io/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Streamlit Guide](https://docs.streamlit.io/)
- [RAG Systems Overview](https://arxiv.org/abs/2005.11401)
- [Pinecone Vector Database](https://docs.pinecone.io/)

---

## 👥 Authors

- **Meet Patel** ([meet-0107](https://github.com/meet-0107))

---

<div align="center">

### 🌟 If you find this project helpful, please consider starring it! ⭐

**Built with ❤️ for enhanced learning experiences**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>
