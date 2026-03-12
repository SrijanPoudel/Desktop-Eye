import os
from dotenv import load_dotenv
from openai import OpenAI
from document_loader import load_document
from chunker import chunk_text
from vector_store import add_chunks_to_db, search_documents, doc_count, clear_session

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sessions = {}

SYSTEM_PROMPT = """You are Desktop Eye, a friendly AI assistant created by Srijan Paudel.
- Warm, helpful, and conversational
- When NO documents uploaded: chat normally, answer general questions
- When documents uploaded: answer ONLY using document content, cite sources
- Name: Desktop Eye | Creator: Srijan Paudel | Powered by GPT-4o-mini + RAG
"""

def ingest_document(filepath, session_id="default"):
    doc = load_document(filepath)
    if not doc: return False
    chunks = chunk_text(doc["content"], doc["filename"])
    add_chunks_to_db(chunks, session_id)
    return True

def ask(question, session_id="default"):
    if session_id not in sessions:
        sessions[session_id] = []
    history = sessions[session_id]
    history.append({"role": "user", "content": question})

    if doc_count(session_id) == 0:
        resp = client.chat.completions.create(
            model="gpt-4o-mini", max_tokens=512,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history[-6:]
        )
        answer = resp.choices[0].message.content
        history.append({"role": "assistant", "content": answer})
        return {"answer": answer, "sources": []}

    chunks, metas = search_documents(question, session_id)
    context = "\n\n---\n\n".join(
        f"[Source {i+1}: {m['source']}]\n{c}"
        for i, (c, m) in enumerate(zip(chunks, metas))
    )
    full_system = SYSTEM_PROMPT + f"\n\nDOCUMENT EXCERPTS:\n{context}"
    resp = client.chat.completions.create(
        model="gpt-4o-mini", max_tokens=1024,
        messages=[{"role": "system", "content": full_system}] + history[-6:]
    )
    answer = resp.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    sources = list(set(m["source"] for m in metas))
    return {"answer": answer, "sources": sources}

def clear_memory(session_id="default"):
    if session_id in sessions:
        sessions[session_id] = []
    clear_session(session_id)
