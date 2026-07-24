from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL


# Load embedding model once when the application starts
model = SentenceTransformer(EMBEDDING_MODEL)


def embed_documents(chunks):
    """
    Create embeddings for a list of chunk dictionaries.

    Each chunk is expected to have:
    {
        "text": "...",
        "source": "...",
        "chunk_id": 0
    }
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings