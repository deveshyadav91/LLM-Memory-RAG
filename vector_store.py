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

    memories = []

    for file in os.listdir(MEMORY_DIR):

        if not file.endswith(".md"):
            continue

        path = os.path.join(MEMORY_DIR, file)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if line.startswith("-"):
                memory = line[1:].strip()

                if memory and memory.lower() != "no memory found.":
                    memories.append({
                        "file": file,
                        "content": memory
                    })

    if not memories:
        print("No memories found.")
        return

    documents = [
        memory["content"]
        for memory in memories
    ]

    embeddings = model.encode(
        documents,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    index = faiss.IndexFlatIP(
        embeddings.shape[1]
    )

    index.add(embeddings)

    faiss.write_index(
        index,
        os.path.join(
            INDEX_DIR,
            "memory.index"
        )
    )

    with open(
        os.path.join(
            INDEX_DIR,
            "memories.pkl"
        ),
        "wb"
    ) as f:

        pickle.dump(
            memories,
            f
        )

    print(
        f"FAISS index created with "
        f"{len(memories)} memories."
    )


def search_memory(query, top_k=3):

    index = faiss.read_index(
        os.path.join(
            INDEX_DIR,
            "memory.index"
        )
    )

    with open(
        os.path.join(
            INDEX_DIR,
            "memories.pkl"
        ),
        "rb"
    ) as f:

        memories = pickle.load(f)

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(memories))
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx < 0 or idx >= len(memories):
            continue

        memory = memories[idx]

        results.append({
            "file": memory["file"],
            "distance": float(1.0 - score),
            "score": float(score),
            "content": memory["content"]
        })

    return results


if __name__ == "__main__":

    results = search_memory(
        "What is my name?"
    )

    for result in results:

        print("\nFILE:", result["file"])
        print(
            "SCORE:",
            result["score"]
        )
        print(
            "DISTANCE:",
            result["distance"]
        )
        print(
            "MEMORY:",
            result["content"]
        )