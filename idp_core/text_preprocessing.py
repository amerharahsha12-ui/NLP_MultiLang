import re

def clean_text(text):
    """
    Clean extracted text:
    - Remove extra symbols while preserving Arabic, English, German letters, and numbers.
    - Normalize multiple spaces.
    """
    text = re.sub(r'[^\w\s\.\,\?\!\u0600-\u06FF]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into chunks for RAG processing 
    with an overlap to ensure context is preserved between segments.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
