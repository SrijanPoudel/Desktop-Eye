import os
from dotenv import load_dotenv
from openai import OpenAI
from document_loader import load_document
from chunker import chunk_text
from vector_store import add_chunks_to_db, search_documents, doc_count

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
history = []

SYSTEM_PROMPT = """You are Desktop Eye, a friendly and intelligent AI assistant created by Srijan Paudel.

Your personality:
- Warm, helpful, and conversational
- Professional but approachable
- You have a subtle "eye" theme — you "see" and "read" documents

When NO documents are uploaded:
- Chat normally and answer general questions
- If asked about documents, gently remind the user to upload one
- Introduce yourself if greeted

When documents ARE uploaded:
- Answer questions using ONLY the document content
- Always cite sources using [Source X]
- If the answer isn't in the document, say so honestly

About yourself:
- Name: Desktop Eye
- Created by: Srijan Paudel
- Purpose: Read and analyze documents using AI
- Powered by: GPT-4o-mini + RAG (Retrieval-Augmented Generation)
- Tech stack: Python, FastAPI, ChromaDB, OpenAI
"""

def ingest_document(filepath):
    print(f"\n📄 Processing: {filepath}")
    doc = load_document(filepath)
    if not doc:
        return False
    chunks = chunk_text(doc["content"], doc["filename"])
    print(f"✂️ {len(chunks)} chunks created, storing...")
    add_chunks_to_db(chunks)
    print(f"✅ Done — DB has {doc_count()} total chunks")
    return True

def ask(question):
    history.append({"role": "user", "content": question})

    if doc_count() == 0:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=512,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history[-6:]
        )
        answer = resp.choices[0].message.content
        history.append({"role": "assistant", "content": answer})
        return {"answer": answer, "sources": []}

    chunks, metas = search_documents(question)
    context = "\n\n---\n\n".join(
        f"[Source {i+1}: {m['source']}]\n{c}"
        for i, (c, m) in enumerate(zip(chunks, metas))
    )

    full_system = SYSTEM_PROMPT + f"\n\nDOCUMENT EXCERPTS:\n{context}"

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[{"role": "system", "content": full_system}] + history[-6:]
    )

    answer = resp.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    sources = list(set(m["source"] for m in metas))
    return {"answer": answer, "sources": sources}

def clear_memory():
    history.clear()
