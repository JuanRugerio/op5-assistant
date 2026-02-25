from ingestion.ingest import fetch_pdf
from ingestion.pdf_parser import parse_pdf
from ingestion.chunking import chunk_text
from ingestion.embedding import load_model, generate_embeddings
from ingestion.vector_store import build_faiss_index, save_faiss_index, save_metadata
from config import PDF_PATH

def run_pipeline():
    print("Step 1: Downloading PDF...")
    fetch_pdf()

    print("Step 2: Parsing PDF...")
    docs = parse_pdf(PDF_PATH)

    print(f"Parsed {len(docs)} pages")

    print("Step 3: Chunking...")
    chunks = chunk_text(docs)

    print(f"Generated {len(chunks)} chunks")

    print("Step 4: Embeddings...")
    model = load_model()
    embeddings = generate_embeddings(chunks, model)

    print("Step 5: Building FAISS index...")
    index = build_faiss_index(embeddings)

    print("Step 6: Saving index and metadata...")
    save_faiss_index(index)
    save_metadata(chunks)

    print("✅ Ingestion pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()