import os
from pypdf import PdfReader
import chromadb
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection(
    "documents",
    metadata={"hnsw:space": "cosine"}
)

def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c.strip() for c in chunks if c.strip()]

def ingest_file(file_path: str, filename: str) -> int:
    print(f"  Extracting text from {filename}...")
    text = extract_text(file_path)
    print(f"  Chunking text...")
    chunks = chunk_text(text)
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk": i} for i in range(len(chunks))]
    collection.upsert(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )
    print(f"  Stored {len(chunks)} chunks from {filename}")
    return len(chunks)