from pathlib import Path


# -------------------------
# Project directories
# -------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "documents"

VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"


# -------------------------
# Chunking
# -------------------------

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100


# -------------------------
# Models
# -------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "qwen2.5:3b"


# -------------------------
# Vector database files
# -------------------------

INDEX_FILE = VECTOR_STORE_DIR / "index.faiss"

CHUNKS_FILE = VECTOR_STORE_DIR / "chunks.pkl"

# Application settings
DEBUG_MODE = True