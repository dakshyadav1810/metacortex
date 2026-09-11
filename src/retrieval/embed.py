# retrieval/embed.py
import json
from typing import List, Dict

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks(path: str) -> List[Dict]:
    chunks = []
    with open(path, "r") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def embed_chunks(chunks: List[Dict]):
    model = SentenceTransformer(MODEL_NAME)

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings, chunks


if __name__ == "__main__":
    chunks = load_chunks("data/chunks/chunks.jsonl")
    embeddings, metadata = embed_chunks(chunks)

    print("Embeddings shape:", embeddings.shape)
