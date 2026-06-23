import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

model = SentenceTransformer("all-MiniLM-L6-v2")

# Use absolute path to project root vectorstore
project_root = Path(__file__).parent.parent.parent
vectorstore_path = project_root / "vectorstore"

chroma_client = chromadb.PersistentClient(path=str(vectorstore_path))
collection = chroma_client.get_or_create_collection(name="rag_docs")


def store_chunks(url, chunks):
    embeddings = model.encode(chunks).tolist()

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[f"{url}_{i}"]
        )

    print(f"Stored {len(chunks)} chunks for {url}")