import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection("documents")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query: str, n_results: int = 5) -> list[dict]:
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "score": round(1 - results["distances"][0][i], 3)
        })
    return chunks