import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI
from document_loader import load_document
from chunker import chunk_text
from vector_store import add_chunks_to_db, search_documents, doc_count, clear_session, delete_doc_from_db, list_docs

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sessions = {}

SYSTEM_PROMPT = """You are Desktop Eye, a friendly AI assistant created by Srijan Paudel.

PERSONALITY:
- Warm, helpful, and professional
- When NO documents uploaded: chat normally, answer general questions
- When documents uploaded: answer ONLY using document content and cite sources

FORMATTING RULES — always follow these:
- Use a short intro sentence to set context
- Use bullet points for lists, steps, or multiple items
- Use paragraphs for explanations and descriptions
- Add spacing between sections for readability
- Bold important terms or key points using **bold**
- End with a brief closing sentence or follow-up question
- Never dump raw text — always structure your response cleanly
- IMPORTANT: Multiple [Source] excerpts may come from the SAME document — they are chunks of the same file, not separate documents. Count unique filenames only when asked how many documents you have.

EXAM RESTRICTION:
- If the user explicitly says they are currently taking an exam, in an exam, or asks you to help them cheat in an exam — politely refuse.
- Do NOT restrict if they upload an exam paper or study material — that is normal studying.

IDENTITY:
- Name: Desktop Eye | Creator: Srijan Paudel | Powered by GPT-4o-mini + RAG
"""

def ingest_document(filepath, session_id="default"):
    doc = load_document(filepath)
    if not doc: return False
    chunks = chunk_text(doc["content"], doc["filename"])
    add_chunks_to_db(chunks, session_id)
    return True

def delete_document(filename, session_id="default"):
    return delete_doc_from_db(filename, session_id)

def list_documents(session_id="default"):
    return list_docs(session_id)

def generate_quiz(session_id="default", num_questions=5):
    """Generate MCQ quiz from uploaded documents"""
    if doc_count(session_id) == 0:
        return {"error": "No documents uploaded. Please upload a document first to generate a quiz."}

    # Get all chunks from the session
    from vector_store import search_documents
    chunks, metas = search_documents("main concepts key points important information", session_id, top_k=8)

    if not chunks:
        return {"error": "Could not retrieve document content for quiz generation."}

    context = "\n\n---\n\n".join(
        f"[Source: {m['source']}]\n{c}"
        for c, m in zip(chunks, metas)
    )

    quiz_prompt = f"""Based on the following document content, generate exactly {num_questions} multiple choice questions.

DOCUMENT CONTENT:
{context}

STRICT RULES:
- Each question must have exactly 4 options labeled A, B, C, D
- Only one option is correct
- Questions must be based ONLY on the document content
- Make questions varied — definitions, facts, concepts
- Return ONLY valid JSON, no extra text, no markdown

Return this exact JSON format:
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": {{
        "A": "First option",
        "B": "Second option", 
        "C": "Third option",
        "D": "Fourth option"
      }},
      "correct": "A",
      "explanation": "Brief explanation why A is correct"
    }}
  ]
}}"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=2000,
        messages=[{"role": "user", "content": quiz_prompt}],
        temperature=0.7
    )

    raw = resp.choices[0].message.content.strip()

    # Clean up any markdown code blocks if present
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'^```\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    try:
        quiz_data = json.loads(raw)
        return {"quiz": quiz_data["questions"]}
    except json.JSONDecodeError:
        return {"error": "Could not generate quiz. Please try again."}


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
