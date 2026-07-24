# HP Local RAG Assistant

A fully local **Retrieval-Augmented Generation (RAG)** assistant that answers questions from private technical documents without sending data to external APIs.

The application ingests local documents, converts them into semantic embeddings, stores them in a FAISS vector database, retrieves relevant context, and generates grounded answers using a locally running Large Language Model.

The system includes both:

* A command-line interface for development/testing
* A Streamlit web interface for interactive demonstration

---

# Architecture

```
                 Local Documents
                 (.txt / .md)
                       |
                       v
              Document Loader
                       |
                       v
                Text Chunking
                       |
                       v
        Sentence Transformer Embeddings
          (all-MiniLM-L6-v2, 384 dimensions)
                       |
                       v
              FAISS Vector Store
                       |
                       v
             Semantic Retrieval
              (Top-K Search)
                       |
                       v
        Retrieved Context + User Question
                       |
                       v
             Local LLM Inference
             (Ollama + Qwen2.5:3B)
                       |
                       v
             Grounded Answer
             + Retrieved Sources
```

---

# Features

* Fully local RAG pipeline
* No external LLM API dependency
* Supports `.txt` and `.md` technical documents
* Semantic document search using embeddings
* FAISS vector similarity retrieval
* Local LLM generation with Ollama
* Context-only prompting to reduce hallucinations
* Source attribution for generated answers
* Configurable Top-K retrieval
* Interactive Streamlit chat interface
* Document re-indexing from the UI
* Conversation history management
* Retrieval confidence display

---

# Technology Stack

## Programming Language

* Python 3.14

## Embedding Model

`sentence-transformers/all-MiniLM-L6-v2`

Purpose:

* Converts documents and user questions into semantic vector representations
* Produces 384-dimensional embeddings

## Vector Database

FAISS

Purpose:

* Stores document embeddings
* Performs efficient similarity search

## Large Language Model

Ollama + Qwen2.5:3B

Purpose:

* Generates answers using only retrieved document context
* Runs locally on the developer machine

## User Interface

Streamlit

Purpose:

* Interactive chat experience
* Displays answers, sources, retrieval information, and system statistics

---

# Project Structure

```
hp-rag-chat/

├── app/
│   ├── chat.py              # CLI chat interface
│   ├── ingest.py            # Document ingestion pipeline
│   ├── chunker.py           # Text splitting logic
│   ├── document_loader.py   # TXT/Markdown document loading
│   ├── embedder.py          # Embedding generation
│   ├── retriever.py         # FAISS similarity search
│   ├── vector_store.py      # FAISS index management
│   ├── llm.py               # Ollama LLM interface
│   ├── stats.py             # Vector store statistics
│   └── config.py            # Application configuration
│
├── documents/
│   ├── embedded_firmware.txt
│   ├── telemetry_systems.txt
│   ├── device_management.txt
│   └── quality_control.txt
│
├── vector_store/
│   ├── index.faiss
│   └── chunks.pkl
│
├── streamlit_app.py         # Web interface
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Mac/Linux

```bash
source .venv/bin/activate
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Install Ollama Model

Download the local LLM:

```bash
ollama pull qwen2.5:3b
```

Verify:

```bash
ollama list
```

---

# Document Ingestion

Before using the assistant, documents must be converted into embeddings.

Run:

```bash
python app/ingest.py
```

Example output:

```
Loaded 5 document(s)

Created 6 chunk(s)

Created embeddings: (6,384)

Saved FAISS index
```

This creates:

```
vector_store/
├── index.faiss
└── chunks.pkl
```

---

# Running the Application

## Option 1: Streamlit Web Interface (Recommended)

Start:

```bash
streamlit run streamlit_app.py
```

The interface provides:

* Chat-based question answering
* Retrieved source display
* Top-K retrieval control
* Knowledge base statistics
* Document refresh/re-indexing
* Conversation clearing

---

## Option 2: Command Line Interface

Run:

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
Firmware updates are delivered through validated release packages
to improve functionality, fix defects, and add new capabilities.

Sources:
- embedded_firmware.txt
```

---

# Adding New Documents

1. Add a new `.txt` or `.md` file into:

```
documents/
```

Example:

```
documents/new_manual.md
```

2. Rebuild the knowledge base:

```bash
python app/ingest.py
```

or use the **Refresh Knowledge Base** button in the Streamlit interface.

3. Ask questions about the new document.

---

# Design Decisions

## Why RAG?

Large language models do not automatically contain private company documentation.

RAG improves accuracy by retrieving relevant information from a private knowledge base before generating an answer.

---

## Why Embeddings Instead of Keyword Search?

Traditional keyword search requires exact word matching.

Embeddings allow semantic understanding.

Example:

Question:

```
How do I update device software?
```

Document:

```
Firmware updates are delivered through validated release packages.
```

The system can identify that these concepts are related even though the wording differs.

---

## Why FAISS?

FAISS provides:

* Fast vector similarity search
* Lightweight local deployment
* No external database dependency

It is well suited for small-to-medium private knowledge bases.

---

## Why Local LLM Inference?

Running inference locally provides:

* Data privacy
* No external API dependency
* Offline operation after model download
* Predictable operating costs

---

# Demo Scenarios

Recommended demonstration questions:

### Knowledge Retrieval

```
How are firmware updates delivered?
```

Expected:
Retrieves embedded firmware documentation.

---

### Multi-document Retrieval

```
How is telemetry data used?
```

Expected:
Retrieves telemetry and device management information.

---

### Hallucination Prevention

```
What programming language was used to create Facebook?
```

Expected:

```
I don't have enough information in the provided documents.
```

---

# Future Improvements

Possible enhancements:

* Streaming token responses
* Larger document collections
* Advanced reranking models
* Hybrid keyword + semantic retrieval
* Automated document monitoring
* Cloud deployment option
* User authentication
* Persistent conversation storage

---

# Summary

This project demonstrates an end-to-end local RAG pipeline:

**Documents → Chunking → Embeddings → FAISS Retrieval → Local LLM → Grounded Answer**

The system provides a practical example of building a private AI assistant capable of answering questions from custom technical documentation.
