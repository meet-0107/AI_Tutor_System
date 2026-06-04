# AI_Tutor_System

This AI tutor transforms course materials into an interactive chat using a strict RAG pipeline. Built with FastAPI, LangChain, and Pinecone DB, it provides hallucination-free guidance, source citations, conversational memory, token streaming, and dynamic MCQ quizzes for a personalized learning experience.

## 🗂️ Project Structure

```text
AI_Tutor_System/
├── Week_1/                  # Data Ingestion & Vector Database
│   ├── document_parser.py   # PDF loading and text chunking
│   └── vector_store.py      # Pinecone DB setup and embedding generation
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

---

# System Architecture (Week 1, 2 & 3)

## Complete Data Flow & Integrated Pipeline

```text
┌────────────────────────────────────────────────────────────────────────────┐
│              WEEK 1, 2 & 3: COMPLETE AI TUTOR PIPELINE                 │
└────────────────────────────────────────────────────────────────────────────┘

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
          │  • Embedding Model               │
          │  • Add search prefixes           │
          │  • Filter empty chunks           │
          │  • Initialize Pinecone Vector DB │
          └──────────┬───────────────────────┘
                     │
                     v
          ┌──────────────────────────────────┐
          │   Pinecone Vector Database       │
          ├──────────────────────────────────┤
          │  • Cloud Vector Storage          │
          │  • Index: ai_tutor_syllabus      │
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
      │  • /quiz/* (Week_3 endpoints)        │
      └──────────┬───────────────────────────┘
                 │
                 v
      ┌──────────────────────────────────────┐
      │  RAG Engine Core (Week_2/core/)      │
      ├──────────────────────────────────────┤
      │ Step 1: Query Embedding              │
      │ Step 2: Vector Similarity Search     │
      │         (Pinecone Retrieval)         │
      │ Step 3: Retrieve Context Chunks      │
      │ Step 4: Prompt Construction          │
      │ Step 5: LLM Generation               │
      │ Step 6: Response + Citations         │
      └──────────┬───────────────────────────┘
                 │
                 ├────────────────────────────┬──────────────┐
                 │                            │              │
                 v                            v              v
      ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐
      │ LangChain            │  │ Pinecone             │  │ LLM Engine       │
      │ Integration          │  │ Retriever            │  │ (Configurable)   │
      ├──────────────────────┤  ├──────────────────────┤  ├──────────────────┤
      │ • Vector Retriever   │  │ • Get Query          │  │ • LLM Instance   │
      │ • Prompt Templates   │  │   Embeddings         │  │ • Prompt: Context│
      │ • LLM Chain          │  │ • Similarity Search  │  │ • Generate       │
      │   Integration        │  │ • Return Top K       │  │   Response       │
      │ • Streaming Support  │  │   Relevant Chunks    │  │ • Token Streaming│
      └──────────┬───────────┘  └──────────┬───────────┘  └──────────┬───────┘
                 │                         │                         │
                 └─────────────────────────┼─────────────────────────┘
                                           │
                               ┌───────────v───────────┐
                               │  Conversational       │
                               │  Memory System (W3)   │
                               └───────────┬───────────┘
                                           │
                     ┌─────────────────────┼────────────────────┐
                     │                     │                    │
                     v                     v                    v
          ┌────────────────────┐  ┌──────────────────┐  ┌─────────────────┐
          │ Message Store      │  │ Embeddings Sim.  │  │ Session DB      │
          ├────────────────────┤  ├──────────────────┤  ├─────────────────┤
          │ • User Query       │  │ • Query Embedds  │  │ • User ID       │
          │ • Bot Response     │  │ • Response Emb.  │  │ • Timestamp     │
          │ • Metadata         │  │ • Relevance Scr. │  │ • Thread ID     │
          │ • Timestamps       │  │ • Retrieval Score│  │ • Analytics     │
          └────────┬───────────┘  └────────┬─────────┘  └────────┬────────┘
                   │                       │                     │
                   └───────────────────────┼─────────────────────┘
                                           │
                               ┌───────────v──────────────┐
                               │ Enhanced Context Asm.    │
                               ├───────────────────────────┤
                               │ • Conv. Thread           │
                               │ • Retrieved Chunks       │
                               │ • Memory-Aug. Prompt     │
                               └───────────┬──────────────┘
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

                      DYNAMIC MCQ QUIZ ENGINE (WEEK 3)
                      ═════════════════════════════════

      ┌──────────────────────────────┐
      │  Quiz Trigger Request        │
      │  (from Frontend)             │
      └──────────┬────────────────────┘
                 │
                 v
      ┌──────────────────────────────────────────┐
      │  Week_3/core/quiz_generator.py           │
      ├──────────────────────────────────────────┤
      │  • Query Pinecone for Content            │
      │  • MCQ Generation Logic                  │
      │  • Answer Validation                     │
      │  • Difficulty Level Selection            │
      └──────────┬───────────────────────────────┘
                 │
                 ├──────────────┬──────────────┬──────────────┐
                 │              │              │              │
                 v              v              v              v
      ┌────────────────┐ ┌────────────────┐ ┌──────────────┐ ┌──────────────┐
      │ Concept Select │ │ Question Craft │ │ Distractors  │ │ Validation   │
      ├────────────────┤ ├────────────────┤ ├──────────────┤ ├──────────────┤
      │ • Extract Key  │ │ • LLM-based    │ │ • Generate   │ │ • Check Ans. │
      │   Topics       │ │   Generation   │ │   Wrong Opts │ │ • Scoring    │
      │ • Difficulty   │ │ • Context      │ │ • Plausible  │ │ • Analytics  │
      │   Based Select │ │   Inclusion    │ │   Answers    │ │              │
      │ • Sample Size  │ │ • Grammar      │ │ • Randomize  │ │              │
      │               │ │   Check        │ │   Order      │ │              │
      └────────┬───────┘ └────────┬───────┘ └────────┬─────┘ └────────┬─────┘
               │                 │                 │                 │
               └─────────────────┼─────────────────┼─────────────────┘
                                 │
                                 v
                   ┌───────────────────────────────┐
                   │  Quiz Assessment Output       │
                   ├───────────────────────────────┤
                   │  • Questions (4-5 options)    │
                   │  • Correct Answers            │
                   │  • Explanations w/ Citations  │
                   │  • Difficulty Level           │
                   │  • Estimated Time             │
                   └───────────┬───────────────────┘
                               │
                               v
                  ┌─────────────────────────────┐
                  │  Week_3/api/quiz_router.py  │
                  ├─────────────────────────────┤
                  │  • /quiz/generate            │
                  │  • /quiz/submit              │
                  │  • /quiz/history             │
                  │  • /quiz/performance         │
                  └───────────┬───────────────────┘
                              │
                              v
               ┌─────────────────────────────────┐
               │  Quiz Results & Analytics       │
               ├─────────────────────────────────┤
               │  • Score Calculation            │
               │  • Performance Metrics          │
               │  • Weakness Identification      │
               │  • Recommendations              │
               └─────────────────────────────────┘
```

## Component Overview

### Week 1: Data Ingestion & Vectorization
- **Document Parser:** Loads PDF documents and splits text into semantic chunks (1000 chars, 200 char overlap)
- **Embedding Generation:** Converts text chunks into vector embeddings using configurable models
- **Vector Storage:** Persists embeddings in Pinecone for efficient cloud-based retrieval and scalability

### Week 2: RAG Engine & Query Processing
- **Frontend:** Streamlit app for interactive UI (Student/Educator views, chat, quizzes)
- **Backend:** FastAPI with Uvicorn provides REST API for chat, ingestion, and quiz endpoints
- **RAG Engine:** Retrieves context chunks from Pinecone, constructs prompts, generates responses using LLM via LangChain
- **Vector Retriever:** Handles semantic similarity search across embedded documents
- **Token Streaming:** Real-time token streaming for improved user experience

### Week 3: Conversational Memory & Quiz Engine
- **Conversation Memory Manager:** Maintains per-user conversation threads with semantic context retrieval
- **Session Storage:** Persists conversations with timestamps and metadata for continuity across sessions
- **Context Window Management:** Intelligently selects important messages within token limits
- **Dynamic MCQ Quiz Generator:** Creates natural, contextual questions from course materials with multiple choice options
- **Distractor Generation:** Produces plausible but incorrect answer choices using LLM
- **Difficulty Levels:** Supports Easy, Medium, and Hard quiz variations
- **Performance Tracking:** Records quiz history and identifies learning gaps for personalized recommendations
- **API Endpoints:** /quiz/generate, /quiz/submit, /quiz/history, /quiz/performance

---

## TECH STACK

**Frontend:**
- Streamlit

**Backend:**
- FastAPI
- Uvicorn

**Framework:**
- LangChain (document loaders, retrievers, chains, integrations)

**Vector Database:**
- Pinecone DB (cloud vector storage with langchain-pinecone)

**Embeddings:**
- Configurable embedding model
- Sentence Transformers

**Memory & Persistence:**
- Session storage with conversation history
- Vector-based semantic similarity for context retrieval

**PDF Parsing:**
- PyPDFLoader (from LangChain)

**Text Splitting:**
- RecursiveCharacterTextSplitter (1000 char chunks with 200 char overlap)

**LLM Integration:**
- LangChain with Ollama/OpenAI support

## ✨ Key Features

✅ **RAG Pipeline** - Retrieval-Augmented Generation for accurate, sourced responses  
✅ **Hallucination-Free** - Strict adherence to course materials with source citations  
✅ **Conversational Memory** - Maintains context across multiple turns with semantic retrieval  
✅ **Token Streaming** - Real-time response streaming for better UX  
✅ **Dynamic MCQ Quizzes** - Auto-generated quizzes from course materials with explanations  
✅ **Multi-Role UI** - Separate views for students and educators  
✅ **Cloud Vector Store** - Scalable Pinecone DB for embedding storage and retrieval  
✅ **Performance Analytics** - Track learning progress and identify knowledge gaps  
✅ **Integrated Memory System** - Context-aware responses using conversation history  

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or conda
- PDF documents for course materials
- Pinecone API key (for vector database)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/meet-0107/AI_Tutor_System.git
cd AI_Tutor_System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Pinecone API key and other configuration
```

4. Run the backend:
```bash
cd Week_2
python main.py
```

5. Run the frontend (in another terminal):
```bash
cd Week_4/frontend
streamlit run app.py
```

## 📝 Usage

1. **Ingest Documents:** Upload PDF materials through the Educator view
2. **Chat:** Ask questions about the course material and get instant answers with citations
3. **Take Quizzes:** Generate and take dynamic MCQ quizzes to test your knowledge
4. **Track Progress:** Monitor learning progress and quiz performance with analytics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for enhanced learning experiences**
