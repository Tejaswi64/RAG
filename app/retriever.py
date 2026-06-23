import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

model = SentenceTransformer("all-MiniLM-L6-v2")

# Use absolute path to project root vectorstore
project_root = Path(__file__).parent.parent
vectorstore_path = project_root / "vectorstore"

client = chromadb.PersistentClient(path=str(vectorstore_path))
collection = client.get_collection("rag_docs")


def search(query, n_results=3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results