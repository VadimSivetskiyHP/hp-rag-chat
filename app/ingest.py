from document_loader import load_documents
from chunker import chunk_text
from embedder import embed_documents
from vector_store import create_vector_store


def main():

    documents = load_documents("documents")

    print(f"Loaded {len(documents)} document(s):")

    for doc in documents:
        print(f" - {doc['source']}")

    chunks = []

    for doc in documents:

        doc_chunks = chunk_text(doc["text"])

        for chunk_index, chunk in enumerate(doc_chunks):

            chunks.append({
                "text": chunk,
                "source": doc["source"],
                "chunk_id": chunk_index
            })

    print(f"Created {len(chunks)} chunk(s)")

    embeddings = embed_documents(chunks)

    print(f"Created embeddings: {embeddings.shape}")

    create_vector_store(
        embeddings,
        chunks
    )

    print("Ingestion complete")


if __name__ == "__main__":
    main()