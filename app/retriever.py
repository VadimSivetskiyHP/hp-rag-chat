import faiss
import pickle
import numpy as np

from embedder import embed_documents
from config import INDEX_FILE, CHUNKS_FILE


def load_vector_store():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    with open(CHUNKS_FILE, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def search(query, top_k=3, similarity_threshold=0.45):

    index, chunks = load_vector_store()

    # Convert question into embedding
    query_embedding = embed_documents(
        [
            {
                "text": query
            }
        ]
    )

    # Convert to float32
    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    # Normalize query vector
    faiss.normalize_L2(
        query_embedding
    )

    # Search FAISS
    similarities, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for similarity, idx in zip(
        similarities[0],
        indices[0]
    ):

        if idx == -1:
            continue

        if similarity < similarity_threshold:
            continue

        result = chunks[idx].copy()

        result["similarity"] = float(
            similarity
        )

        results.append(result)

    return results