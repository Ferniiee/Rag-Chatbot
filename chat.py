import os
from groq import Groq
from retriever import retrieve
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using only 
the provided context from uploaded documents. Always cite your sources by 
mentioning the document name. If the answer isn't in the context, say so clearly 
— do not make up information."""

def answer(question: str) -> dict:
    chunks = retrieve(question)
    if not chunks:
        return {
            "answer": "No documents have been uploaded yet. Please upload a document first.",
            "sources": []
        }
    context = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )
    prompt = f"""Context from uploaded documents:

{context}

Question: {question}

Answer based only on the context above:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return {
        "answer": response.choices[0].message.content,
        "sources": list(set(c["source"] for c in chunks))
    }