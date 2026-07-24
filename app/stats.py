import faiss
import pickle

from app.config import INDEX_FILE, CHUNKS_FILE


def get_stats():

    try:

        index = faiss.read_index(
            str(INDEX_FILE)
        )

        with open(CHUNKS_FILE, "rb") as f:
            chunks = pickle.load(f)


        documents = sorted(
            set(
                chunk["source"]
                for chunk in chunks
            )
        )


        return {

            "documents": len(documents),

            "document_list": documents,

            "chunks": len(chunks),

            "vectors": index.ntotal

        }


    except Exception:

        return {

            "documents": 0,

            "document_list": [],

            "chunks": 0,

            "vectors": 0

        }