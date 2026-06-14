\# RAG Chatbot



A full-stack retrieval-augmented generation (RAG) chatbot that lets you upload documents and ask natural language questions about them.



\## How it works

1\. Upload a PDF or TXT file through the web UI

2\. Documents are chunked, embedded, and stored in ChromaDB

3\. Questions are embedded and matched against stored chunks via semantic search

4\. Groq LLaMA 3.3 generates answers using only the retrieved context

5\. Answers are returned with source citations



\## Tech stack

\- \*\*LLM:\*\* Groq (LLaMA 3.3 70B)

\- \*\*Embeddings:\*\* Sentence Transformers (all-MiniLM-L6-v2)

\- \*\*Vector store:\*\* ChromaDB

\- \*\*Backend:\*\* Flask

\- \*\*Frontend:\*\* HTML/CSS/JavaScript



\## Setup

```bash

git clone https://github.com/Ferniiee/Rag-Chatbot

cd Rag-Chatbot

python -m venv venv

venv\\Scripts\\Activate.ps1

pip install flask chromadb groq pypdf python-dotenv sentence-transformers

```



Add a `.env` file:



GROQ\_API\_KEY=your\_key\_here



\## Usage

```bash

python app.py

```

Open \*\*http://localhost:5000\*\*, upload a document, and start chatting.

