def chunk_text(text, source_name, chunk_size=800, overlap=100):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current, idx = [], "", 0
    for para in paragraphs:
        if len(current) + len(para) < chunk_size:
            current += para + "\n\n"
        else:
            if current.strip():
                chunks.append({"content": current.strip(), "source": source_name,
                                "chunk_index": idx, "id": f"{source_name}_c{idx}"})
                idx += 1
            words = current.split()
            current = " ".join(words[-overlap:]) + "\n\n" + para + "\n\n"
    if current.strip():
        chunks.append({"content": current.strip(), "source": source_name,
                        "chunk_index": idx, "id": f"{source_name}_c{idx}"})
    return chunks

if __name__ == "__main__":
    sample = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    result = chunk_text(sample, "test.txt")
    print(f"✅ Created {len(result)} chunks from sample text")
