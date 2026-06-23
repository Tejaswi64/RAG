from retriever import search
from ollama import generate


def ask_question(question):

    results = search(question, n_results=3)

    context = "\n\n".join(
        results["documents"][0]
    )

    prompt = f"""
You are an AI assistant.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    return generate(prompt)