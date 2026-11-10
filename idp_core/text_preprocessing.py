import re
import unicodedata
def clean_text(text, preserve_newlines=False):
    """
    Clean multilingual text (Arabic, English, German).
    - Normalize Unicode using NFC.
    - Preserve letters, diacritics, punctuation,
      and important symbols.
    - Remove unwanted control characters.
    - Normalize whitespace.
    - Optionally preserve paragraph boundaries.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(preserve_newlines, bool):
        raise TypeError("preserve_newlines must be a boolean")
    # Unicode normalization
    text = unicodedata.normalize("NFC", text)
    # Handle selected invisible characters
    text = text.replace("\ufeff", "")
    text = text.replace("\u200b", " ")
    # Normalize different line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\u2028", "\n")
    text = text.replace("\u2029", "\n")
    # Replace unwanted control characters
    text = "".join(
        " " if unicodedata.category(char) == "Cc"
        and char not in "\n\t"
        else char
        for char in text
    )
    if preserve_newlines:
        # Normalize spaces without removing paragraphs
        text = re.sub(r"[^\S\n]+", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
    else:
        # Original behavior: flatten whitespace
        text = re.sub(r"\s+", " ", text)
    return text.strip()
def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into overlapping word-based chunks.

    - Validate inputs.
    - Preserve punctuation and paragraph formatting.
    - Avoid unnecessary duplicate chunks.
    - Return an empty list for empty input.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if type(chunk_size) is not int or type(overlap) is not int:
        raise TypeError(
            "chunk_size and overlap must be integers"
        )
    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero"
        )
    if not 0 <= overlap < chunk_size:
        raise ValueError(
            "overlap must satisfy 0 <= overlap < chunk_size"
        )
    # Find word positions to preserve formatting
    words = list(re.finditer(r"\S+", text))
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        end = min(start + chunk_size, len(words))
        chunk = text[
            words[start].start():words[end - 1].end()
        ]
        chunks.append(chunk)
        if end == len(words):
            break

    return chunks
