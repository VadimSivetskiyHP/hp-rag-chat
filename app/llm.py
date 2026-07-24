import requests

from app.config import LLM_MODEL


OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_answer(context, question):

    prompt = f"""
You are a professional AI assistant for answering questions from a private technical knowledge base.

Your job is to provide accurate answers using ONLY the information provided in the context.

Rules:
- Do not use outside knowledge.
- Do not make assumptions.
- If the context does not contain enough information, respond:
  "I don't have enough information in the provided documents."
- Keep answers concise and technically accurate.
- Explain concepts clearly when needed.

Retrieved Context:
------------------
{context}
------------------

User Question:
{question}

Answer:
"""


    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )


    response.raise_for_status()


    return response.json()["response"].strip()