import json
import os
import pickle

import faiss
import numpy as np

from src.retrieval.embed import load_chunks, embed_chunks


CHUNKS_PATH = "data/chunks/chunks.jsonl"
INDEX_DIR = "data/index"
INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
META_PATH = os.path.join(INDEX_DIR, "metadata.pkl")


def build_index(embeddings: np.ndarray):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def save_index(index, metadata):
    os.makedirs(INDEX_DIR, exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)


def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata


def run():
    chunks = load_chunks(CHUNKS_PATH)
    embeddings, metadata = embed_chunks(chunks)

    index = build_index(embeddings)
    save_index(index, metadata)

    print("Index built")
    print("Total vectors:", index.ntotal)


if __name__ == "__main__":
    run()
