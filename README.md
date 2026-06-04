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

# System Architecture (Week 1 & Week 2)

## Complete Data Flow & RAG Pipeline

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                    WEEK 1 & 2: COMPLETE AI TUTOR PIPELINE                │
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
         │  • Initialize ChromaDB Vector DB │
         └──────────┬───────────────────────┘
                    │
                    v
         ┌──────────────────────────────────┐
         │   ChromaDB Vector Database       │
         ├──────────────────────────────────┤
         │  • Local Vector Storage          │
         │  • Collection: ai_tutor_syllabus │
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
                ├────────────────────────────┬──────────────┐
                │                            │              │
                v                            v              v
     ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐
     │ LangChain            │  │ ChromaDB             │  │ LLM Engine       │
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

## Component Overview

- **Frontend:** Streamlit app for interactive UI (Student/Educator views, chat, quizzes)
- **Backend:** FastAPI with Uvicorn provides REST API for chat, ingestion, and quiz endpoints
- **RAG Engine:** Retrieves context chunks from ChromaDB, constructs prompts, generates responses using LLM via LangChain
- **Vector Database:** ChromaDB stores embedded document vectors and handles semantic search
- **Data Ingestion:** Parses PDF documents, splits text into chunks, computes embeddings, and persists in ChromaDB
- **Conversational Memory:** Maintains conversation history for context-aware responses
- **Token Streaming:** Real-time token streaming for improved user experience
- **Dynamic Quizzes:** MCQ quiz generation based on course materials

## TECH STACK

**Frontend:**
- Streamlit

**Backend:**
- FastAPI
- Uvicorn

**Framework:**
- LangChain (document loaders, retrievers, chains, integrations)

**Vector Database:**
- ChromaDB (local vector storage)

**Embeddings:**
- Configurable embedding model

**PDF Parsing:**
- PyPDFLoader (from LangChain)

**Text Splitting:**
- RecursiveCharacterTextSplitter (1000 char chunks with 200 char overlap)

## ✨ Key Features

✅ **RAG Pipeline** - Retrieval-Augmented Generation for accurate, sourced responses  
✅ **Hallucination-Free** - Strict adherence to course materials with source citations  
✅ **Conversational Memory** - Maintains context across multiple turns  
✅ **Token Streaming** - Real-time response streaming for better UX  
✅ **Dynamic MCQ Quizzes** - Auto-generated quizzes from course materials  
✅ **Multi-Role UI** - Separate views for students and educators  
✅ **Local Vector Store** - Privacy-preserving ChromaDB for embedding storage  

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or conda
- PDF documents for course materials

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
# Edit .env with your configuration
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
4. **Track Progress:** Monitor learning progress and quiz performance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for enhanced learning experiences**
