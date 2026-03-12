from rag_engine import ingest_document, ask

# Create a sample document
notes = """
# System Design Notes

## Sharding
Sharding splits a database across multiple servers. Each server (shard) holds a subset of the data.
Use sharding when a single database can't handle the load.
Benefits: horizontal scalability, better performance under load.

## Caching with Redis
Redis stores frequently accessed data in memory.
Retrieving from cache is 100x faster than from disk.
Cache invalidation is the hardest part — know when data is stale.
Use TTL (time-to-live) to auto-expire cached items.

## Key Takeaways
1. Always add caching before horizontal scaling
2. Measure first — never guess at bottlenecks
3. Design for failure — every server will eventually crash
"""

# Save the document to a file
with open("system_design.txt", "w", encoding="utf-8") as f:
    f.write(notes)

print("=" * 50)

# Ingest the document into the RAG system
ingest_document("system_design.txt")

print("\n" + "=" * 50)
print("QUESTION 1:")

# Ask first question
r = ask("What is sharding and when should I use it?")

print(f"\n{r['answer']}")
print(f"\n📄 Sources: {r['sources']}")

print("\n" + "=" * 50)
print("QUESTION 2 (follow-up — tests memory):")

# Ask follow-up question
r2 = ask("What did you just tell me about caching?")

print(f"\n{r2['answer']}")