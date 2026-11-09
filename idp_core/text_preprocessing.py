import re
import unicodedata


def clean_text(text):
    """
    Normalize Unicode and whitespace without discarding meaningful symbols.

    Preserve letters, diacritics, punctuation, currency, and formatting marks.
    Replace control characters with spaces. Paragraph boundaries
    are flattened for compatibility with the original function.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    text = unicodedata.normalize("NFC", text)
    text = "".join(
        " " if unicodedata.category(char) == "Cc" else char
        for char in text
    )
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into chunks for RAG processing
    with an overlap to ensure context is preserved between segments.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if type(chunk_size) is not int or type(overlap) is not int:
        raise TypeError("chunk_size and overlap must be integers")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must satisfy 0 <= overlap < chunk_size")

    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
    return chunks
