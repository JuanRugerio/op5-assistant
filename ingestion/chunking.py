# ingestion/chunking.py

#Within each page, Splits text into paragraphs. Chunks are 3 paragraph lenght, they overlap therefore.

from ingestion.pdf_parser import parse_pdf
from config import WINDOWS_SIZE


def split_into_paragraphs(text):
    """
    Split text into paragraphs using double newlines or large breaks.
    """
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]


def chunk_text(documents, window_size=WINDOWS_SIZE):
    chunks = []

    for doc in documents:
        paragraphs = split_into_paragraphs(doc["text"])
        page = doc["page"]

        # Sliding window over paragraphs
        for i in range(len(paragraphs)):
            window = paragraphs[i:i + window_size]

            if not window:
                continue

            chunk_text = " ".join(window)

            chunks.append({
                "text": chunk_text,
                "page": page
            })

    return chunks