import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_engine import ingest_document, ask, clear_memory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)


class Question(BaseModel):
    text: str


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        path = f"uploads/{file.filename}"

        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        success = ingest_document(path)

        if success:
            return {"status": "ok", "message": f"{file.filename} uploaded"}
        else:
            return {"status": "error", "message": "Unsupported file type"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/ask")
async def ask_question(q: Question):
    try:
        return ask(q.text)
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "sources": []}

@app.post("/ask")
async def ask_question(q: Question):
    try:
        return ask(q.text)
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "sources": []}


@app.post("/clear")
async def clear():
    clear_memory()
    return {"status": "cleared"}


@app.get("/")
async def root():
    return {"status": "AI Assistant is running!"}