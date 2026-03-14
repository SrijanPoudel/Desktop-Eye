import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from rag_engine import ingest_document, ask, clear_memory, delete_document, list_documents, generate_quiz

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Question(BaseModel):
    question: str
    session_id: Optional[str] = "default"

class DeleteDoc(BaseModel):
    filename: str
    session_id: Optional[str] = "default"

class QuizRequest(BaseModel):
    session_id: Optional[str] = "default"
    num_questions: Optional[int] = 5

@app.get("/")
def root():
    return {"status": "AI Assistant is running!"}

@app.get("/session")
def new_session():
    return {"session_id": str(uuid.uuid4())}

@app.get("/documents")
def get_documents(x_session_id: Optional[str] = Header(None)):
    session_id = x_session_id or "default"
    return {"documents": list_documents(session_id)}

@app.post("/upload")
async def upload(file: UploadFile = File(...), x_session_id: Optional[str] = Header(None)):
    session_id = x_session_id or "default"
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    success = ingest_document(path, session_id)
    return {"success": success, "filename": file.filename}

@app.post("/delete")
def delete_doc(body: DeleteDoc):
    success = delete_document(body.filename, body.session_id or "default")
    return {"success": success}

@app.post("/ask")
def ask_question(q: Question):
    result = ask(q.question, q.session_id or "default")
    return result

@app.post("/quiz")
def generate_quiz_endpoint(body: QuizRequest):
    result = generate_quiz(body.session_id or "default", body.num_questions or 5)
    return result

@app.post("/clear")
def clear(q: Optional[Question] = None):
    session_id = (q.session_id if q.session_id else "default") if q else "default"
    clear_memory(session_id)
    return {"cleared": True}

@app.post("/admin-reset")
def admin_reset():
    import chromadb
    DB_PATH = "/data/knowledge_db" if __import__('os').path.exists("/data") else "./knowledge_db"
    client = chromadb.PersistentClient(path=DB_PATH)
    for col in client.list_collections():
        client.delete_collection(col.name)
    return {"reset": True}
