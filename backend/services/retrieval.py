import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import json
from config import EMBEDDING_MODEL, FAISS_INDEX_PATH, METADATA_PATH, TOP_K
#Retrives index and metadata. Embedding model for query is the same as that one used to generate embeddings
# Embeds Query. Finds k closest vectors at index. L2 distance used. Appends corresponding metadata explicit
#information related to retrieved vectors. 

class Retriever:
    def __init__(self):

        print("Loading FAISS index...")

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        index_path = os.path.join(BASE_DIR, FAISS_INDEX_PATH)
        metadata_path = os.path.join(BASE_DIR, METADATA_PATH)

        self.index = faiss.read_index(index_path)

        print("Loading metadata...")
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        print("Loading embedding model...")
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed_query(self, query):
        return self.model.encode([query])

    def search(self, query, top_k=TOP_K):
        query_embedding = self.embed_query(query)

        distances, indices = self.index.search(
            np.array(query_embedding), top_k
        )

        results = []
        scores = []

        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue

            results.append(self.metadata[idx])
            scores.append(float(distances[0][i]))

        return results, scores