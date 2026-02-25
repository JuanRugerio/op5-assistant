import faiss
import json
import os
import numpy as np
from config import FAISS_INDEX_PATH, METADATA_PATH

#Taking into account the number of embeddings, builds faiss index. Writes index to path. Writes metadata
def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index


def save_faiss_index(index, path=FAISS_INDEX_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    faiss.write_index(index, path)


def save_metadata(chunks, path=METADATA_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)