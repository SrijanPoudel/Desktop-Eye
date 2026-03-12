import os

def load_document(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    filename = os.path.basename(filepath)
    
    if ext == '.txt' or ext == '.md':
        with open(filepath, 'r', encoding='utf-8') as f:
            return {"content": f.read(), "filename": filename}
    
    elif ext == '.pdf':
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        text = "\n\n".join(page.extract_text() for page in reader.pages)
        return {"content": text, "filename": filename}
    
    elif ext == '.docx':
        from docx import Document
        doc = Document(filepath)
        text = "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return {"content": text, "filename": filename}
    
    else:
        print(f"❌ Unsupported file type: {ext}")
        return None

def load_folder(folderpath):
    docs = []
    for f in os.listdir(folderpath):
        filepath = os.path.join(folderpath, f)
        doc = load_document(filepath)
        if doc:
            docs.append(doc)
    return docs

if __name__ == "__main__":
    print("✅ document_loader.py is ready!")
