import os
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

MEMORY_DIR = "memories"
INDEX_DIR = "faiss"

os.makedirs(INDEX_DIR, exist_ok=True)

model = SentenceTransformer(
    "./models/all-MiniLM-L6-v2",
    local_files_only=True
)


def build_index():

    documents = []
    filenames = []

    for file in os.listdir(MEMORY_DIR):

        if not file.endswith(".md"):
            continue

        path = os.path.join(MEMORY_DIR, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append(text)
        filenames.append(file)

    embeddings = model.encode(documents)

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    faiss.write_index(index, os.path.join(INDEX_DIR, "memory.index"))

    with open(os.path.join(INDEX_DIR, "files.pkl"), "wb") as f:
        pickle.dump(filenames, f)

    print("FAISS index created.")