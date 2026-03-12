import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from rag_engine import ingest_document, ask, clear_memory

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Question(BaseModel):
    question: str
    session_id: Optional[str] = "default"

@app.get("/")
def root():
    return {"status": "AI Assistant is running!"}

@app.get("/session")
def new_session():
    return {"session_id": str(uuid.uuid4())}

@app.post("/upload")
async def upload(file: UploadFile = File(...), x_session_id: Optional[str] = Header(None)):
    session_id = x_session_id or "default"
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    success = ingest_document(path, session_id)
    return {"success": success, "filename": file.filename}

@app.post("/ask")
def ask_question(q: Question):
    result = ask(q.question, q.session_id or "default")
    return result

@app.post("/clear")
def clear(q: Optional[Question] = None):
    session_id = q.session_id if q else "default"
    clear_memory(session_id)
    return {"cleared": True}
