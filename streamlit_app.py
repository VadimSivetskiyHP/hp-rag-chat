import streamlit as st

from app.stats import get_stats
from app.retriever import search
from app.llm import generate_answer
from app.ingest import rebuild_index


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="HP Local Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)


# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("📚 HP Local Knowledge Assistant")

st.markdown("""
### Private document search powered by

- 🧠 **Ollama (Qwen2.5:3B)**
- 🔎 **FAISS Vector Search**
- 📄 **TXT & Markdown Documents**
- 🚫 **Runs Completely Offline**
""")


st.info(
    "This application demonstrates Retrieval-Augmented Generation (RAG) "
    "running completely offline using a local language model."
)

# ---------------------------------------------------
# RAG Architecture
# ---------------------------------------------------

with st.expander("🏗️ How the RAG Pipeline Works"):

    st.markdown(
        """
```mermaid
flowchart LR

    A[📄 Documents<br/>TXT + Markdown] --> B[✂️ Chunking]

    B --> C[🧠 Embeddings<br/>all-MiniLM-L6-v2]

    C --> D[(🔎 FAISS<br/>Vector Database)]

    Q[❓ User Question] --> E[Query Embedding]

    E --> D

    D --> F[Relevant Context]

    F --> G[🤖 Ollama<br/>Qwen2.5:3B]

    G --> H[✅ Grounded Answer]
    """)
# ---------------------------------------------------
# Load System Stats
# ---------------------------------------------------

stats = get_stats()


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.header("System Information")

    st.metric(
        "Documents",
        stats["documents"]
    )

    st.metric(
        "Chunks",
        stats["chunks"]
    )

    st.metric(
        "Vectors",
        stats["vectors"]
    )

    st.divider()

    st.subheader("📚 Indexed Documents")


    if stats["document_list"]:

        for doc in stats["document_list"]:

            st.write(
                f"📄 {doc}"
            )

    else:

        st.write(
            "No documents indexed"
        )

    st.write("### AI Stack")

    st.write(
        "**Embedding Model**  \n"
        "all-MiniLM-L6-v2"
    )

    st.write(
        "**Language Model**  \n"
        "Qwen2.5:3B (Ollama)"
    )

    st.write(
        "**Vector Database**  \n"
        "FAISS"
    )

    st.write(
        "**Supported Files**  \n"
        ".txt  \n"
        ".md"
    )

    st.divider()

    st.write("### Retrieval Settings")

    top_k = st.slider(
        "Number of retrieved chunks",
        min_value=1,
        max_value=5,
        value=3
    )
    st.divider()

    st.subheader("Knowledge Base")

    if st.button("🔄 Refresh Documents"):

        with st.spinner(
            "Rebuilding knowledge base..."
        ):

            rebuild_index()

        st.success(
            "Knowledge base refreshed!"
        )

        st.rerun()
        
    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# ---------------------------------------------------
# Chat History
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# Display previous conversation

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------
# User Input (Enter Key)
# ---------------------------------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)


if question:


    # Save user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)


    # ---------------------------------------------------
    # Retrieval
    # ---------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Searching knowledge base..."
        ):

            results = search(
            question,
            top_k=top_k
            )


        if not results:

            answer = (
                "I could not find relevant information "
                "in the knowledge base."
            )

            st.warning(answer)


        else:


            # Combine retrieved chunks

            context = "\n".join(
                result["text"]
                for result in results
            )


            # ---------------------------------------------------
            # LLM Generation
            # ---------------------------------------------------

            with st.spinner(
                "🤖 Generating answer..."
            ):

                answer = generate_answer(
                    context,
                    question
                )


            st.success(answer)



            # ---------------------------------------------------
            # Sources
            # ---------------------------------------------------

            with st.expander(
                "📄 Retrieved Sources"
            ):

                for i, result in enumerate(
                    results,
                    start=1
                ):

                    confidence = result["similarity"]


                    if confidence >= 0.80:
                        level = "🟢 High"

                    elif confidence >= 0.55:
                        level = "🟡 Medium"

                    else:
                        level = "🔴 Low"


                    st.markdown(
                        f"""
### Source {i}: {result['source']}

**Chunk ID:** {result['chunk_id']}  

**Confidence:** {level} ({confidence:.0%})

---

{result['text']}
"""
                    )


    # Save assistant response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )