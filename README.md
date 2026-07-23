# HP Local RAG Assistant

A fully local Retrieval-Augmented Generation (RAG) assistant that answers questions from private technical documents without sending data to external APIs.

The system ingests technical documentation, converts it into semantic embeddings, stores them in a vector database, retrieves relevant information, and generates answers using a locally running LLM.

---

# Architecture

```
Documents (.txt / .md)
          |
          v
Document Loader
          |
          v
Text Chunking
          |
          v
Embedding Model
(sentence-transformers)
          |
          v
FAISS Vector Database
          |
          v
Semantic Retrieval
          |
          v
Context + User Question
          |
          v
Local LLM
(Ollama + Qwen2.5)
          |
          v
Answer + Sources
```

---

# Features

- Fully local AI inference
- No external API dependency
- Supports TXT and Markdown documents
- Semantic search using embeddings
- FAISS vector similarity search
- Local LLM generation with Ollama
- Source attribution
- Hallucination reduction through context-only prompting
- Developer debug mode with retrieval information

---

# Technology Stack

## Language

- Python 3.14

## AI Components

### Embedding Model

`sentence-transformers/all-MiniLM-L6-v2`

Converts text into 384-dimensional vectors representing semantic meaning.

### Vector Database

FAISS

Used for efficient similarity search over document embeddings.

### Large Language Model

Ollama + Qwen2.5:3B

Runs locally for private document question answering.

---

# Project Structure

```
hp-rag-chat/

├── app/
│
├── chat.py
├── ingest.py
├── chunker.py
├── embedder.py
├── retriever.py
├── vector_store.py
├── llm.py
└── config.py


├── documents/
│   ├── embedded_firmware.txt
│   ├── telemetry_systems.txt
│   ├── device_management.txt
│   └── quality_control.txt


├── vector_store/
│   ├── faiss.index
│   └── chunks.pkl


└── requirements.txt
```

---

# Installation

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama models:

```bash
ollama pull qwen2.5:3b
```

---

# Document Ingestion

Before asking questions, build the vector database:

```bash
python app/ingest.py
```

Example:

```
Loaded 5 document(s)

Created 6 chunk(s)

Created embeddings: (6,384)

Saved FAISS index
```

---

# Running the Assistant

Start chat:

```bash
python app/chat.py
```

Example:

Question:

```
How are firmware updates delivered?
```

Answer:

```
Firmware updates are delivered through validated release packages to improve functionality, fix defects, and add new capabilities.

Sources:
- embedded_firmware.txt
```

---

# Design Decisions

## Why RAG?

Large language models do not automatically know private company documentation.

RAG allows the model to retrieve relevant information from a private knowledge base before generating an answer.

---

## Why embeddings?

Keyword search depends on exact word matching.

Embeddings allow semantic matching.

Example:

Question:

"How do I update device software?"

Document:

"Firmware updates are delivered through validated release packages."

The system recognizes these concepts are related even though the words differ.

---

## Why local inference?

Running the LLM locally provides:

- Data privacy
- No external API dependency
- Offline capability
- Predictable costs

---

# Future Improvements

- Web interface
- Streaming responses
- Larger document collections
- Better ranking models
- Conversation memory
- Automated document updates

