import os
from openai import OpenAI
import chromadb

DB_PATH = "/data/knowledge_db" if os.path.exists("/data") else "./knowledge_db"
chroma = chromadb.PersistentClient(path=DB_PATH)

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_collection(session_id="default"):
    return chroma.get_or_create_collection(f"session_{session_id}")

def get_embedding(text):
    client = get_client()
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text.replace("\n", " "))
    return res.data[0].embedding

def add_chunks_to_db(chunks, session_id="default"):
    collection = get_collection(session_id)
    for c in chunks:
        try:
            existing = collection.get(ids=[c["id"]])
            if existing["ids"]: continue
        except: pass
        collection.add(
            documents=[c["content"]], embeddings=[get_embedding(c["content"])],
            metadatas=[{"source": c["source"], "chunk": c["chunk_index"]}],
            ids=[c["id"]])

def search_documents(question, session_id="default", top_k=5):
    collection = get_collection(session_id)
    n = min(top_k, collection.count())
    if n == 0: return [], []
    res = collection.query(query_embeddings=[get_embedding(question)], n_results=n)
    return res["documents"][0], res["metadatas"][0]

def doc_count(session_id="default"):
    return get_collection(session_id).count()

def clear_session(session_id="default"):
    try:
        chroma.delete_collection(f"session_{session_id}")
    except: pass
