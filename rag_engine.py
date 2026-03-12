# rag_engine.py
# Uses OpenAI for EVERYTHING (no Claude key needed!)

import os
from dotenv import load_dotenv
from openai import OpenAI

from document_loader import load_document, load_folder
from chunker import chunk_text
from vector_store import add_chunks_to_db, search_documents, doc_count

# Load environment variables from .env
load_dotenv()

# ONE client for embeddings and answers
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Conversation memory
history = []


def ingest_document(filepath):
    """
    Load a file, chunk it, and store it in the vector database.
    """
    print(f"\n📄 Processing: {filepath}")

    doc = load_document(filepath)
    if not doc:
        return False

    # Split document into chunks
    chunks = chunk_text(doc["content"], doc["filename"])

    print(f"✂️ {len(chunks)} chunks created, storing...")

    # Store chunks in vector DB
    add_chunks_to_db(chunks)

    print(f"✅ Done — DB has {doc_count()} total chunks")

    return True


def ask(question):
    """
    Ask a question and get a cited answer using GPT-4o-mini.
    """

    if doc_count() == 0:
        return {
            "answer": "❌ No documents loaded yet! Add files first.",
            "sources": []
        }

    # Search vector DB for relevant chunks
    chunks, metas = search_documents(question)

    # Build context for the LLM
    context = "\n\n---\n\n".join(
        f"[Source {i+1}: {m['source']}]\n{c}"
        for i, (c, m) in enumerate(zip(chunks, metas))
    )

    # Add question to conversation memory
    history.append({"role": "user", "content": question})

    # System prompt
    system_msg = {
        "role": "system",
        "content": f"""
You are a personal knowledge assistant.

Answer ONLY using the provided document excerpts.
Always cite sources using [Source X].

If the answer is not in the excerpts, say so honestly.

DOCUMENT EXCERPTS:
{context}
"""
    }

    # Call OpenAI model
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[system_msg] + history[-6:]
    )

    answer = resp.choices[0].message.content

    # Save assistant reply to memory
    history.append({"role": "assistant", "content": answer})

    # Collect unique source files
    sources = list(set(m["source"] for m in metas))

    return {
        "answer": answer,
        "sources": sources
    }


def clear_memory():
    """
    Clear conversation history.
    """
    history.clear()