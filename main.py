import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rag_engine import ingest_document, ask, clear_memory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "AI Assistant is running!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    success = ingest_document(path)
    return {"success": success, "filename": file.filename}

@app.post("/ask")
def ask_question(q: Question):
    result = ask(q.question)
    return result

@app.post("/clear")
def clear():
    clear_memory()
    return {"cleared": True}
