import os, shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import ingest_document, ask, clear_memory

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

os.makedirs("uploads", exist_ok=True)

class Question(BaseModel):
    question: str

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    success = ingest_document(path)
    return {"status": "ok" if success else "error", "filename": file.filename}

@app.post("/ask")
async def ask_question(q: Question):
    result = ask(q.question)
    return result

@app.post("/clear")
async def clear():
    clear_memory()
    return {"status": "cleared"}

@app.get("/")
async def root():
    return {"status": "AI Assistant is running!"}
