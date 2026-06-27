import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_DIR = "faiss"
MEMORY_DIR = "memories"

model = SentenceTransformer(
    "./models/all-MiniLM-L6-v2",
    local_files_only=True
)

index = faiss.read_index(os.path.join(INDEX_DIR, "memory.index"))

with open(os.path.join(INDEX_DIR, "files.pkl"), "rb") as f:
    filenames = pickle.load(f)


def retrieve(query, k=5, threshold=1.2):

    query_embedding = model.encode([query]).astype("float32")

    distances, indices = index.search(query_embedding, k)

    memories = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        # Ignore unrelated memories
        if distance > threshold:
            continue

        filename = filenames[idx]

        with open(
            os.path.join(MEMORY_DIR, filename),
            "r",
            encoding="utf-8"
        ) as f:

            memories.append(f.read())

    return memories