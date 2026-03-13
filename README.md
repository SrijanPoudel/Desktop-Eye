# 👁 Desktop Eye — AI Document Intelligence Assistant

> **Upload any document. Ask anything. Get cited answers instantly.**

## 🧠 What is Desktop Eye?

Desktop Eye is a full-stack AI-powered document assistant that uses **Retrieval-Augmented Generation (RAG)** to answer questions from uploaded documents with source citations and session privacy.

Unlike ChatGPT, Desktop Eye:
- 🔒 Keeps documents **private per session**
- 📄 Answers **only from your document** — no hallucinations  
- 🔍 Shows **exactly which source** every answer came from
- 🚀 Works with **PDF, DOCX, TXT, and MD** files

## ✨ Features
- Upload multiple documents per session
- Chat with documents using natural language
- Delete individual documents from session
- AI personality that chats normally without documents
- Session-isolated vector storage — no data leakage between users
- Animated Apple-style UI

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML, CSS, Vanilla JavaScript |
| **Backend** | Python, FastAPI, Uvicorn |
| **AI Model** | OpenAI GPT-4o-mini |
| **Embeddings** | OpenAI text-embedding-3-small |
| **Vector DB** | ChromaDB |
| **Document Parsing** | pypdf, python-docx |
| **Environment** | python-dotenv |
| **Frontend Hosting** | GitHub Pages |
| **Backend Hosting** | Render |

## 🔄 How RAG Works
```
User uploads document
        │
        ▼
document_loader.py → Extracts text from PDF/DOCX/TXT/MD
        │
        ▼
chunker.py → Splits into 800-char chunks, 100-char overlap
        │
        ▼
vector_store.py → Embeds chunks using text-embedding-3-small
        │
        ▼
ChromaDB → Stores in session-isolated collection
        │
        ▼
User asks question → semantic search → top 5 chunks
        │
        ▼
GPT-4o-mini → Generates cited answer from context
```

## 📁 Project Structure
```
desktop-eye/
├── main.py              # FastAPI app — all API endpoints
├── rag_engine.py        # RAG pipeline — ingest, ask, clear
├── vector_store.py      # ChromaDB — embed, search, delete
├── document_loader.py   # File parser — PDF, DOCX, TXT, MD
├── chunker.py           # Text chunking strategy
├── index.html           # Full frontend UI
├── requirements.txt     # Python dependencies
└── Procfile             # Render deployment config
```

## 🚀 Run Locally
```bash
git clone https://github.com/SrijanPoudel/Desktop-Eye.git
cd Desktop-Eye
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key-here" > .env
uvicorn main:app --reload
```

Then open index.html in your browser.

## 🌐 Live Demo

- **App:** https://srijanpoudel.github.io/Desktop-Eye/
- **API:** https://desktop-eye.onrender.com

## 👤 Author

**Srijan Paudel** — [@SrijanPoudel](https://github.com/SrijanPoudel)

© 2026 Srijan Paudel · Desktop Eye — All rights reserved
