🏗 Architecture
--------------------------------------------------------------------------------------------------------------------------------------------------------
Frontend (GitHub Pages)
`index.html` · Vanilla JS · CSS
↓ HTTP REST API
Backend (Render — FastAPI + Uvicorn)

| Endpoint | File | Role |
|----------|------|------|
| POST /upload | document_loader.py → chunker.py | Load & chunk document |
| POST /ask | rag_engine.py | Search + generate answer |
| POST /delete | vector_store.py | Remove document |
| GET /documents | vector_store.py | List session documents |

Data Layer
- ChromaDB — session-isolated vector storage
- OpenAI text-embedding-3-small — document embeddings
- OpenAI GPT-4o-mini — answer generation
--------------------------------------------------------------------------------------------------------------------------------------------------------

 🔄 How RAG Works

| Step | Component | Action |
|------|-----------|--------|
| 1 | document_loader.py | Extracts text from PDF, DOCX, TXT, MD |
| 2 | chunker.py | Splits text into 800-char chunks with 100-char overlap |
| 3 | vector_store.py | Embeds each chunk using text-embedding-3-small |
| 4 | ChromaDB | Stores embeddings in session-isolated collection |
| 5 | vector_store.py | Embeds question → semantic search → top 5 chunks |
| 6 | rag_engine.py | Builds context and sends to GPT-4o-mini |
| 7 | API response | Returns answer with cited sources to user |
--------------------------------------------------------------------------------------------------------------------------------------------------------

🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Vanilla JavaScript |
| Backend | Python, FastAPI, Uvicorn |
| AI Model | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector DB | ChromaDB |
| Document Parsing | pypdf, python-docx |
| Environment | python-dotenv |
| Frontend Hosting | GitHub Pages |
| Backend Hosting | Render |
```
---------------------------------------------------------------------------------------------------------------------------------------------------------

📁 Project Structure

desktop-eye/
├── main.py              # FastAPI app — all API endpoints
├── rag_engine.py        # RAG pipeline — ingest, ask, clear
├── vector_store.py      # ChromaDB operations — embed, search, delete
├── document_loader.py   # File parser — PDF, DOCX, TXT, MD
├── chunker.py           # Text chunking strategy
├── index.html           # Full frontend UI
├── requirements.txt     # Python dependencies
├── Procfile             # Render deployment config
└── .env                 # API keys (not committed)
---------------------------------------------------------------------------------------------------------------------------------------------------------

🌐 Deployment
ServicePurposeURLRenderBackend API hostinghttps://desktop-eye.onrender.comGitHub PagesFrontend hostinghttps://srijanpoudel.github.io/Desktop-Eye/
---------------------------------------------------------------------------------------------------------------------------------------------------------
👤 Author
Srijan Paudel
---------------------------------------------------------------------------------------------------------------------------------------------------------
GitHub: @SrijanPoudel
Email: srijan5434@gmail.com
---------------------------------------------------------------------------------------------------------------------------------------------------------

📄 License
© 2026 Srijan Paudel · Desktop Eye — All rights reserved
