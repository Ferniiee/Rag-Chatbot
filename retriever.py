import chromadb
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection(
    "documents",
    metadata={"hnsw:space": "cosine"}
)

def retrieve(query: str, n_results: int = 5) -> list[dict]:
    results = collection.query(
        query_texts=[query],
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