# document_loader.py
# Reads files and extracts text content

import os
from pypdf import PdfReader


def load_pdf(filepath):
    """
    Read a PDF — returns all text from every page.
    """
    reader = PdfReader(filepath)
    text = ""

    for i, page in enumerate(reader.pages):
        text += f"\n--- Page {i+1} ---\n" + (page.extract_text() or "")

    return text


def load_text(filepath):
    """
    Read a .txt or .md file.
    """
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_document(filepath):
    """
    Auto-detect file type and load it.
    Returns a dictionary or None.
    """
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == ".pdf":
        content = load_pdf(filepath)

    elif ext in [".txt", ".md"]:
        content = load_text(filepath)

    else:
        print(f"⚠️ Skipping unsupported: {ext}")
        return None

    return {
        "content": content,
        "filename": os.path.basename(filepath),
        "filepath": filepath,
        "type": ext,
        "chars": len(content)
    }


def load_folder(folder):
    """
    Load all supported files in a folder.
    """
    docs = []

    for name in os.listdir(folder):
        path = os.path.join(folder, name)

        if os.path.isfile(path):
            d = load_document(path)

            if d:
                docs.append(d)

    print(f"✅ Loaded {len(docs)} documents")
    return docs


# Test it when running this file directly
if __name__ == "__main__":

    with open("sample_note.txt", "w") as f:
        f.write("My notes on machine learning.\nKey insight: data quality matters most.")

    result = load_document("sample_note.txt")

    print(f"✅ Loaded '{result['filename']}' — {result['chars']} characters")
    print(f"Content: {result['content']}")