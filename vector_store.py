import os
from openai import OpenAI
import chromadb

chroma = chromadb.PersistentClient(path="./knowledge_db")
collection = chroma.get_or_create_collection("my_documents")

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    client = get_client()
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text.replace("\n", " "))
    return res.data[0].embedding

def add_chunks_to_db(chunks):
    for c in chunks:
        try:
            existing = collection.get(ids=[c["id"]])
            if existing["ids"]: continue
        except: pass
        print(f"  Embedding chunk {c['chunk_index']} from {c['source']}")
        collection.add(
            documents=[c["content"]], embeddings=[get_embedding(c["content"])],
            metadatas=[{"source": c["source"], "chunk": c["chunk_index"]}],
            ids=[c["id"]])

def search_documents(question, top_k=5):
    n = min(top_k, collection.count())
    if n == 0: return [], []
    res = collection.query(query_embeddings=[get_embedding(question)], n_results=n)
    return res["documents"][0], res["metadatas"][0]

def doc_count(): return collection.count()
