#Loads embedding model, embeds chunks with it

from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

def load_model():
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model


def generate_embeddings(chunks, model):
    texts = [c["text"] for c in chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    return embeddings