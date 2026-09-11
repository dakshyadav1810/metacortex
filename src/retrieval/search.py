import pickle
import faiss
import numpy as np
import os

from sentence_transformers import SentenceTransformer


INDEX_PATH = "data/index/faiss.index"
META_PATH = "data/index/metadata.pkl"
MODEL_NAME = "all-MiniLM-L6-v2"


class VectorSearcher:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        
        # Check if index files exist
        if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
            print(f"Warning: Index files not found. Creating empty index.")
            self.index = None
            self.metadata = []
        else:
            self.index = faiss.read_index(INDEX_PATH)
            with open(META_PATH, "rb") as f:
                self.metadata = pickle.load(f)

    def search(self, query: str, top_k: int = 5):
        if self.index is None or len(self.metadata) == 0:
            print("Warning: No index available. Returning empty results.")
            return []
            
        query_vec = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue

            chunk = self.metadata[idx]
            results.append({
                "chunk_id": chunk["chunk_id"],
                "title": chunk["title"],
                "url": chunk["url"],
                "text": chunk["text"],
                "score": float(dist)
            })

        return results


if __name__ == "__main__":
    searcher = VectorSearcher()

    query = "governor of Azad Hall"
    results = searcher.search(query, top_k=3)

    for r in results:
        print("\n---")
        print(r["title"])
        print(r["url"])
        print(r["text"][:300])
