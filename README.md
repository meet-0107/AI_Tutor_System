# AI_Tutor_System

This AI tutor transforms course materials into an interactive chat using a strict RAG (Retrieval-Augmented Generation) pipeline. Built with **FastAPI**, **LangChain**, **PineconeDB**, and **Streamlit**, it provides hallucination-free guidance, source citations, conversational memory, real-time token streaming, and dynamic MCQ quizzes for a personalized learning experience.

---

## 🗂️ Project Structure

```text
AI_Tutor_System/
├── Week_1/                      # Data Ingestion & Vector Database Setup
│   ├── document_parser.py       # PDF loading and intelligent text chunking
│   ├── vector_store.py          # ChromaDB/Pinecone integration & embeddings
│   ├── __init__.py
│   └── utils/                   # Helper utilities for data processing
│       ├── validators.py        # File validation & error handling
│       └── logger.py            # Logging configuration
├── Week_2/                      # RAG Engine & FastAPI Backend
│   ├── api/
│   │   ├── chat_router.py       # Chat endpoints (/chat/complete, /chat/stream)
│   │   ├── ingest_router.py     # Document ingestion endpoints (/ingest)
│   │   ├── health_router.py     # Health check endpoints (/health)
│   │   └── schemas.py           # Pydantic request/response models
│   ├── core/
│   │   ├── rag_engine.py        # RAG pipeline & retrieval logic
│   │   ├── prompts.py           # LLM prompt templates
│   │   ├── llm_setup.py         # LLM configuration (Ollama/OpenAI)
│   │   ├── retrievers.py        # Vector store retriever setup
│   │   └── citation_formatter.py # Source citation extraction
│   ├── middleware/
│   │   ├── cors.py              # CORS configuration
│   │   └── auth.py              # Optional authentication
│   ├── config.py                # Configuration management
│   ├── main.py                  # FastAPI application entry point
│   └── __init__.py
├── Week_3/                      # Conversational Memory & Quiz Engine
│   ├── api/
│   │   ├── quiz_router.py       # Quiz endpoints (/quiz/generate, /quiz/submit)
│   │   ├── memory_router.py     # Memory endpoints (/memory/history, etc.)
│   │   └── schemas.py           # Quiz & memory request/response models
│   ├── core/
│   │   ├── memory_manager.py    # Conversation memory & session handling
│   │   ├── context_window.py    # Token budgeting & context selection
│   │   ├── quiz_generator.py    # Dynamic MCQ generation logic
│   │   ├── distractor_gen.py    # Plausible distractors generation
│   │   ├── performance_tracker.py # Quiz analytics & metrics
│   │   └── question_validator.py # Question quality checks
│   ├── database/
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── storage.py           # Session & conversation persistence
│   │   └── connection.py        # Database connection management
│   └── __init__.py
├── Week_4/                      # Frontend & Real-Time Streaming
│   ├── frontend/
│   │   ├── app.py               # Streamlit multipage application
│   │   ├── pages/
│   │   │   ├── 1_student_tutor.py     # Student chat interface
│   │   │   ├── 2_educator_dashboard.py # Educator content & quiz management
│   │   │   └── 3_analytics.py         # Learning analytics dashboard
│   │   ├── components/
│   │   │   ├── chat_widget.py   # Reusable chat display component
│   │   │   ├── quiz_widget.py   # Quiz UI component
│   │   │   ├── metrics_widget.py # Analytics visualization
│   │   │   └── sidebar.py       # Navigation sidebar
│   │   ├── styles/
│   │   │   └── custom.css       # Custom CSS styling
│   │   └── config.py            # Frontend configuration
│   ├── core/
│   │   ├── stream_handler.py    # SSE & token streaming logic
│   │   ├── ui_helpers.py        # Frontend utility functions
│   │   ├── api_client.py        # FastAPI client wrapper
│   │   └── state_manager.py     # Streamlit session state management
│   └── __init__.py
├── tests/
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── e2e/                     # End-to-end tests
├── data_samples/                # Sample documents for testing
├── logs/                        # Application logs
├── .env                         # Environment variables (API keys, models)
├── .env.example                 # Example environment configuration
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Docker orchestration (optional)
├── Dockerfile                   # Container image (optional)
├── pyproject.toml               # Python project metadata
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
        │  ✓ Metadata extraction              │
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
    │  ✓ Error handling & recovery             │
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
    │  Step 7: Validate & quality check        │
    └──────────────┬───────────────────────────┘
                   │
         ┌─────────┼─────────┬──────────────┐
         │         │         │              │
         v         v         v              v
    ┌────────────────────┐ ┌──────────────────┐ ┌────────────────────┐
    │ Embedding Model    │ │ Vector Retriever │ │ LLM Engine         │
    ├────────────────────┤ ├──────────────────┤ ├────────────────────┤
    │ ✓ Sentence         │ │ ✓ ChromaDB/      │ │ ✓ Ollama/OpenAI    │
    │   Transformers     │ │   Pinecone       │ │ ✓ LangChain LCEL   │
    │ ✓ Query encoding   │ │ ✓ Similarity     │ │ ✓ Token streaming  │
    │ ✓ Batch processing │ │   search         │ │ ✓ Temperature ctrl │
    │ ✓ Caching          │ │ ✓ Top-K ranking  │ │ ✓ Max tokens limit │
    │                    │ │ ✓ Metadata       │ │                    │
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
                     │  ✓ Guardrails & fallbacks │
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
                     │  ✓ Confidence scoring     │
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
    │  ✓ Generate summaries for long chats       │
    └──────────────┬─────────────────────────────┘
                   │
         ┌─────────┼──────────┬────────────────┐
         │         │          │                │
         v         v          v                v
    ┌────────────┐┌────────────┐ ┌──────────────┐ ┌─────────────────┐
    │ Session DB ││ Message    │ │ Embedding    │ │ Performance     │
    │ Storage    ││ Store      │ │ Similarity   │ │ Metrics         │
    ├────────────┤├────────────┤ ├──────────────┤ ├─────────────────┤
    │ ✓ User ID  ││ ✓ Chat ID  │ │ ✓ Query      │ │ ✓ Quiz scores   │
    │ ✓ Session  ││ ✓ Messages │ │   embeddings │ │ ✓ Concepts      │
    │   ID       ││ ✓ Timestamp│ │ ✓ Response   │ │   mastered      │
    │ ✓ Metadata ││ ✓ Role     │ │   embeddings │ │ ✓ Weak areas    │
    │ ✓ Thread   ││ ✓ Content  │ │ ✓ Similarity │ │ ✓ Learning path │
    │   ID       ││ ✓ Embed ID │ │   scores     │ │                 │
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
           │ ✓ Dynamic summarization
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
    │  ✓ Concept extraction & selection        │
    │  ✓ Question generation strategy          │
    │  ✓ Answer validation & uniqueness check  │
    └──────────────┬───────────────────────────┘
                   │
         ┌─────────┼────────┬──────────┬─────────────┐
         │         │        │          │             │
         v         v        v          v             v
    ┌────────────┐┌────────────┐ ┌───────────┐ ┌─────────────┐ ┌──────────┐
    │ Concept    ││ Question   │ │ Distractors
    │ Selection  ││ Crafting   │ │ Generation│ │ Validation  │ │ Ranking  │
    ├────────────┤├────────────┤ ├───────────┤ ├─────────────┤ ├──────────┤
    │ ✓ Extract  ││ ✓ LLM-based│ │ ✓ Generate│ │ ✓ Check Ans │ │ ✓ Score  │
    │   key      ││   Q generat│ │   wrong   │ │   validity  │ │  plausib │
    │   topics   ││ ✓ Include  │ │ ✓ Similar │ │ ✓ Grammar   │ │ ✓ Order  │
    │ ✓ Difficulty ││   context  │ │   to      │ │   check     │ │   options│
    │   selection ││ ✓ Grammar  │ │   correct │ │ ✓ Format    │ │ ✓ Shuffle│
    │ ✓ Sample   ││   check    │ │ ✓ Randomiz│ │   valid     │ │ ✓ Variety│
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
             │ ✓ Comparative analysis  │
             └─────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════════╗
║              WEEK 4: FRONTEND UI & REAL-TIME STREAMING                         ║
╚════════════════════════════════════════════════════════════════════════════════╝

    STREAMLIT FRONTEND ARCHITECTURE:
    ════════════════════════════════

    ┌──────────────────────────────────────────────────┐
    │    Streamlit Multipage Application               │
    │    (Week_4/frontend/app.py)                      │
    │                                                  │
    │    └─ Navigation Sidebar (pages-based routing)  │
    └──────────────────┬───────────────────────────────┘
                       │
         ┌─────────────┼─────────────┬──────────────┐
         │             │             │              │
         v             v             v              v
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Student      │ │ Educator     │ │ Analytics    │
    │ Tutor        │ │ Dashboard    │ │ Dashboard    │
    │ (1_student_  │ │ (2_educator_ │ │ (3_analytics │
    │ tutor.py)    │ │ dashboard.py)│ │ .py)         │
    ├──────────────┤ ├──────────────┤ ├──────────────┤
    │ ✓ Chat UI    │ │ ✓ PDF        │ │ ✓ Progress   │
    │ ✓ Message    │ │   upload     │ │   charts     │
    │   display    │ │ ✓ Ingestion  │ │ ✓ Quiz stats │
    │ ✓ Streaming  │ │   status     │ │ ✓ Weak areas │
    │   responses  │ │ ✓ Quiz       │ │ ✓ Comparative
    │ ✓ Quiz page  │ │   generation │ │   analysis   │
    │ ✓ History    │ │ ✓ Quiz mgmt  │ │ ✓ Export     │
    │ ✓ Settings   │ │ ✓ Vector DB  │ │   reports    │
    │ ✓ Filters    │ │   stats      │ │ ✓ Trends     │
    │ ✓ Sidebar    │ │ ✓ Search     │ │ ✓ Predictions
    │   navigation │ │ ✓ Settings   │ │              │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
            ┌───────────────v───────────────┐
            │  Streamlit Session State      │
            │  Management                   │
            ├───────────────────────────────┤
            │  ✓ User authentication        │
            │  ✓ Session persistence        │
            │  ✓ Global config & settings   │
            │  ✓ Cache management           │
            │  ✓ Error states               │
            └───────────────┬───────────────┘
                            │
                            v
                ┌───────────────────────────┐
                │  HTTP Client Request      │
                │  (FastAPI Endpoints)      │
                └───────────┬───────────────┘
                            │
        ┌───────────────────┼───────────────────────┐
        │                   │                       │
        v                   v                       v
    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
    │ Standard Chat    │ │ Stream Chat      │ │ Quiz/Memory      │
    │ Endpoints        │ │ Endpoints        │ │ Endpoints        │
    │ /chat/complete   │ │ /chat/stream     │ │ /quiz/*          │
    │                  │ │                  │ │ /memory/*        │
    │ Response: JSON   │ │ Response: SSE    │ │ /ingest          │
    │ (Complete text)  │ │ (Token stream)   │ │                  │
    │                  │ │                  │ │ Response: JSON   │
    └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
             │                    │                    │
             │      ┌─────────────v──────────────┐     │
             │      │  Uvicorn Server            │     │
             │      │  (Async Event Loop)        │     │
             │      │  • Connection pooling      │     │
             │      │  • Request queuing         │     │
             │      │  • Error recovery          │     │
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
           │  SSE: metadata (sources)  │
           │<──────────────────────────┤
           │                           │
           │  SSE: [DONE]              │
           │<──────────────────────────┤
           │  (stream complete)        │
           │                           │

    Real-time UI Update:
    - Display tokens as they arrive
    - Smooth typing animation
    - Show sources dynamically
    - Citations in real-time
    - Error handling & retry logic
    - Connection timeout recovery


    DETAILED STREAMLIT FRONTEND COMPONENTS:
    ═══════════════════════════════════════

    Week_4/frontend/components/
    ├── chat_widget.py
    │   ├─ Render message history
    │   ├─ Display streaming responses
    │   ├─ Show source citations
    │   ├─ Handle message input
    │   └─ Auto-scroll to latest
    │
    ├── quiz_widget.py
    │   ├─ Display questions MCQ format
    │   ├─ Render answer options
    │   ├─ Show timer (if timed)
    │   ├─ Handle answer submission
    │   └─ Display instant feedback
    │
    ├── metrics_widget.py
    │   ├─ Performance charts (Plotly)
    │   ├─ Progress indicators
    │   ├─ Quiz statistics
    │   ├─ Knowledge gap heatmap
    │   └─ Trending analysis
    │
    └── sidebar.py
        ├─ Navigation menu
        ├─ User info display
        ├─ Settings panel
        ├─ Session history
        └─ Quick filters


    STATE MANAGEMENT ARCHITECTURE:
    ═════════════════════════════

    Streamlit Session State:
    ┌─────────────────────────────────────┐
    │ Global App State                    │
    ├─────────────────────────────────────┤
    │ • user_id: str                      │
    │ • session_id: str                   │
    │ • current_page: str                 │
    │ • api_client: APIClient             │
    │ • config: Config                    │
    │ • messages: List[Message]           │
    │ • current_quiz: Quiz | None         │
    │ • performance_cache: Dict           │
    │ • error_state: str | None           │
    └─────────────────────────────────────┘

    Local Component State (per page):
    ┌─────────────────────────────────────┐
    │ Student Tutor State                 │
    ├─────────────────────────────────────┤
    │ • input_text: str                   │
    │ • is_streaming: bool                │
    │ • current_response: str             │
    │ • selected_difficulty: str          │
    │ • show_history: bool                │
    │ • chat_filter: str                  │
    └─────────────────────────────────────┘
```

---

## 🔧 Component Overview

### **Week 1: Data Ingestion & Vectorization**

**Purpose:** Prepare course materials for retrieval

- **Document Parser** (`Week_1/document_parser.py`)
  - Load PDF documents using PyPDFLoader
  - Extract text with metadata preservation (filename, page number, date)
  - Validate file integrity and encoding
  - Handle various PDF formats and encoding issues
  
- **Text Splitting**
  - RecursiveCharacterTextSplitter: 1000 char chunks, 200 char overlap
  - Maintains semantic boundaries between chunks
  - Filters empty/whitespace-only segments
  - Preserves context across chunk boundaries

- **Embedding Generation**
  - Converts text chunks into vector embeddings
  - Supports: Sentence Transformers, OpenAI embeddings
  - Batch processing for efficiency
  - Retry logic for failed embeddings

- **Vector Storage** (`Week_1/vector_store.py`)
  - ChromaDB (local) or Pinecone (cloud)
  - Index: `ai_tutor_documents`
  - Stores embeddings + metadata (source, page, chunk_id)
  - Enables fast similarity search with filtering

---

### **Week 2: RAG Engine & Query Processing**

**Purpose:** Retrieve relevant context and generate responses

- **FastAPI Backend** (`Week_2/main.py`)
  - Uvicorn ASGI server for async processing
  - CORS middleware for frontend communication
  - Request validation with Pydantic models
  - Structured logging & error handling
  - Health checks and graceful shutdown

- **Chat Routers** (`Week_2/api/chat_router.py`)
  - `POST /chat/complete` → Standard response (full text)
  - `GET /chat/stream` → Streaming response (token-by-token via SSE)
  - Both endpoints support conversation context
  - Request rate limiting and validation

- **RAG Engine** (`Week_2/core/rag_engine.py`)
  1. **Query Embedding:** Convert user message to vector
  2. **Similarity Search:** Query vector store for top-K chunks
  3. **Context Assembly:** Combine retrieved chunks into context window
  4. **Prompt Construction:** Build system prompt + context + query
  5. **LLM Generation:** Stream/generate response via LLM
  6. **Citation Extraction:** Parse and format source references
  7. **Quality Validation:** Check response coherence and accuracy

- **Prompt Templates** (`Week_2/core/prompts.py`)
  - System instructions for RAG-compliant behavior
  - Context injection points
  - Citation format requirements
  - Few-shot examples for quality control
  - Guardrails to prevent hallucinations

- **LLM Setup** (`Week_2/core/llm_setup.py`)
  - Support for Ollama (local) and OpenAI/Claude (cloud)
  - Temperature and max_tokens configuration
  - Token streaming callback handlers
  - Model-specific prompt formatting

---

### **Week 3: Conversational Memory & Quiz Engine**

**Purpose:** Maintain context across conversations and generate assessments

#### **Conversational Memory System**

- **Memory Manager** (`Week_3/core/memory_manager.py`)
  - Per-user/per-session conversation threads
  - Semantic similarity-based context retrieval
  - Intelligent context window management (token budgeting)
  - Summary generation for long conversations
  - Automatic cleanup of old sessions

- **Session Storage** (`Week_3/database/storage.py`)
  - Persist conversations with timestamps
  - Store user metadata and session info
  - Support for multiple concurrent sessions
  - Query history and search capabilities
  - Export conversation history

- **Context Window Management**
  - Maintains conversation history within token limits
  - Ranks messages by relevance using embeddings
  - Selects most important historical messages
  - Balances history depth vs. current query focus
  - Handles context overflow gracefully

#### **Dynamic MCQ Quiz Engine**

- **Quiz Generator** (`Week_3/core/quiz_generator.py`)
  - Retrieves relevant course materials
  - Selects concepts based on difficulty level
  - Generates natural language questions using LLM
  - Validates answer correctness and uniqueness

- **Distractor Generation** (`Week_3/core/distractor_gen.py`)
  - Creates plausible but incorrect alternatives
  - Maintains semantic similarity to correct answer
  - Prevents obviously wrong options
  - Randomizes option order for fairness

- **Difficulty Levels**
  - **Easy:** Foundational concepts, recall-based
  - **Medium:** Application-level thinking
  - **Hard:** Synthesis and analysis

- **Performance Tracking** (`Week_3/core/performance_tracker.py`)
  - Records quiz attempts with scores
  - Identifies weak knowledge areas
  - Tracks improvement over time
  - Generates personalized recommendations
  - Comparative analysis with class averages

- **Quiz API Endpoints** (`Week_3/api/quiz_router.py`)
  - `POST /quiz/generate` → Create new quiz
  - `POST /quiz/submit` → Submit answers & get results
  - `GET /quiz/history` → Retrieve past quizzes
  - `GET /quiz/performance` → Analytics dashboard data

---

### **Week 4: Frontend UI & Real-Time Streaming**

**Purpose:** Provide interactive user interfaces with real-time updates

#### **Streamlit Frontend Architecture** (`Week_4/frontend/app.py`)

**Multipage Application Structure:**

```
app.py (Entry point)
├── pages/
│   ├── 1_student_tutor.py
│   │   ├── Session state initialization
│   │   ├── Chat history display
│   │   ├── Message input handling
│   │   ├── Streaming response rendering
│   │   ├── Quiz interface
│   │   └── Performance dashboard
│   │
│   ├── 2_educator_dashboard.py
│   │   ├── PDF upload widget
│   │   ├── Ingestion status monitor
│   │   ├── Vector store statistics
│   │   ├── Quiz management interface
│   │   ├── Student analytics overview
│   │   └── Content performance metrics
│   │
│   └── 3_analytics.py
│       ├── Student progress visualization
│       ├── Quiz performance analytics
│       ├── Learning gap heatmap
│       ├── Trend analysis charts
│       ├── Comparative analysis
│       └── Report export functionality
│
├── components/ (Reusable UI elements)
│   ├── chat_widget.py
│   │   ├── Message history rendering
│   │   ├── Streaming token display
│   │   ├── Source citation formatting
│   │   └── Auto-scroll management
│   │
│   ├── quiz_widget.py
│   │   ├── MCQ question display
│   │   ├── Answer option rendering
│   │   ├── Timer functionality
│   │   └── Instant feedback display
│   │
│   ├── metrics_widget.py
│   │   ├── Progress charts (Plotly)
│   │   ├── Performance indicators
│   │   ├── Knowledge gap visualization
│   │   └── Trend analysis
│   │
│   └── sidebar.py
│       ├── Navigation menu
│       ├── User profile section
│       ├── Settings panel
│       └── Quick filters
│
├── core/
│   ├── stream_handler.py (SSE management)
│   ├── api_client.py (FastAPI wrapper)
│   ├── state_manager.py (Session state)
│   └── ui_helpers.py (Utility functions)
│
└── config.py (Frontend configuration)
```

**Key Features:**

1. **Student Tutor** (`pages/1_student_tutor.py`)
   - Real-time chat interface with message history
   - Streaming token visualization with typing animation
   - Source citations displayed inline with messages
   - Dynamic quiz creation with difficulty selection
   - Performance metrics and learning progress tracking
   - Search/filter for message history

2. **Educator Dashboard** (`pages/2_educator_dashboard.py`)
   - Drag-and-drop PDF document upload
   - Real-time ingestion progress monitoring
   - Vector store statistics and index management
   - Quiz creation and customization interface
   - Student progress overview and analytics
   - Content performance metrics per document

3. **Analytics Dashboard** (`pages/3_analytics.py`)
   - Student progress charts with trend analysis
   - Quiz performance analytics (avg score, completion rate)
   - Learning gap identification heatmap
   - Topic mastery visualization
   - Comparative analysis (student vs. class average)
   - Exportable performance reports (CSV, PDF)

#### **Token Streaming System** (`Week_4/core/stream_handler.py`)

- **Server-Sent Events (SSE)**
  - Asynchronous generator yields tokens in real-time
  - Maintains HTTP connection for live updates
  - Fallback to polling if SSE unavailable
  - Connection timeout and retry logic

- **Frontend Integration**
  - Streamlit `st.write()` updates as tokens arrive
  - Loading animation during stream
  - Automatic scroll to latest message
  - Error handling & retry logic
  - Graceful degradation for unsupported browsers

#### **State Management** (`Week_4/core/state_manager.py`)

- **Session State Persistence**
  - User authentication and session management
  - Chat history and quiz history caching
  - UI preferences and settings storage
  - Performance metrics caching
  - Error recovery and fallback states

- **Component Communication**
  - Callback handlers for cross-component updates
  - Event-driven architecture
  - Centralized state updates
  - Cache invalidation strategies

#### **API Client** (`Week_4/core/api_client.py`)

- **REST API Integration**
  - Type-safe API calls with Pydantic models
  - Request/response validation
  - Error handling and retry logic
  - Connection pooling and keep-alive
  - Request timeout and cancellation support

---

## 💻 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.28+ | Interactive web UI with multipage support |
| **Backend** | FastAPI 0.104+ | Async REST API server |
| **ASGI Server** | Uvicorn | Async application server |
| **LLM Framework** | LangChain 0.1+ | Orchestration, retrieval, chains |
| **Vector DB** | ChromaDB / Pinecone | Semantic search & embeddings storage |
| **Embeddings** | Sentence Transformers / OpenAI | Text vectorization |
| **PDF Processing** | PyPDFLoader | Document ingestion |
| **Text Splitting** | RecursiveCharacterTextSplitter | Semantic chunking |
| **LLM Engines** | Ollama / OpenAI / Claude | Text generation |
| **Data Persistence** | SQLite / PostgreSQL | Conversation & quiz storage |
| **Async Runtime** | asyncio | Concurrent request handling |
| **Visualization** | Plotly / Altair | Data visualization & charts |
| **Data Validation** | Pydantic 2.0+ | Request/response validation |
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
| **Real-time UI Updates** | Server-Sent Events for live data streaming | W4 |
| **Export Analytics** | Generate and export performance reports | W4 |
| **Multi-session Support** | Handle multiple concurrent user sessions | W3-W4 |
| **Error Recovery** | Graceful error handling and fallback mechanisms | All |

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

# Logging
LOG_LEVEL=INFO
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
# API docs: http://localhost:8000/docs
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
   - Compare with peers (if enabled)

### For Educators

1. **Ingest Course Materials**
   - Upload PDF documents
   - Monitor ingestion status
   - View vector store statistics
   - Manage document versions

2. **Manage Content**
   - Create custom quizzes
   - Review student progress
   - Export analytics reports
   - Update course materials

3. **Analytics Dashboard**
   - Class-level performance metrics
   - Individual student progress
   - Topic mastery analysis
   - Identify struggling students

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
| SSE streaming not working | Verify browser supports EventSource API; check CORS settings |
| Out of memory errors | Reduce chunk size or batch size for embeddings |

---

## 📈 Performance Optimization

1. **Vector Search:** Use Pinecone for production (cloud-managed scalability)
2. **Batch Processing:** Process multiple PDFs simultaneously
3. **Caching:** Cache frequent queries and responses
4. **Async I/O:** Leverage FastAPI's async capabilities
5. **Model Selection:** Use smaller embeddings for speed vs. larger for accuracy
6. **Connection Pooling:** Reuse database connections
7. **Token Streaming:** Use streaming responses instead of waiting for full completion
8. **CDN:** Serve static assets from CDN in production

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
- [Server-Sent Events Guide](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Async Python Guide](https://docs.python.org/3/library/asyncio.html)

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
![LangChain](https://img.shields.io/badge/LangChain-0.1%2B-orange?logo=langchain)

</div>
