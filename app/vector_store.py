import os
import pickle
import faiss
import numpy as np

from config import (
    VECTOR_STORE_DIR,
    INDEX_FILE,
    CHUNKS_FILE
)


def create_vector_store(embeddings, chunks):

    # Create vector store folder if missing
    os.makedirs(
        VECTOR_STORE_DIR,
        exist_ok=True
    )


    # Convert embeddings to float32
    embeddings = np.array(
        embeddings,
        dtype="float32"
    )


    # Normalize vectors for cosine similarity
    faiss.normalize_L2(
        embeddings
    )


    # Embedding dimension
    dimension = embeddings.shape[1]


    # Inner product on normalized vectors = cosine similarity
    index = faiss.IndexFlatIP(
        dimension
    )


    # Add vectors
    index.add(
        embeddings
    )


    # Save FAISS index
    faiss.write_index(
        index,
        str(INDEX_FILE)
    )


    # Save metadata
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(
            chunks,
            f
        )


    print(
        f"Saved FAISS index with {index.ntotal} vectors"
    )