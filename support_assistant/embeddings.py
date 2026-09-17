from pathlib import Path
import os
import chromadb
from sentence_transformers import SentenceTransformer

DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "zepto_support"

def load_documents():
    """Load all text documents from the docs directory."""
    documents_data = []
    for file in sorted(os.listdir(DOCS_DIR)):
        if file.endswith(".txt"):
            filepath = os.path.join(DOCS_DIR, file)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents_data.append({
                "id": file.replace(".txt", ""),
                "text": text,
                "source": file
            })
    print("Total Documents Loaded:", len(documents_data))
    return documents_data

def create_chunks(documents_data):
    """Create chunks for all documents."""
    chunk_size = 300
    chunks_data = []
    for doc in documents_data:
        text = doc["text"]
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            chunks_data.append({
                "id": f'{doc["id"]}_chunk_{i//chunk_size}',
                "text": chunk,
                "source": doc["source"]
            })

    print("Total Chunks Created:", len(chunks_data))
    return chunks_data

def create_embeddings(chunks_data):
    """Create embeddings for all chunks."""
    embedding_model  = SentenceTransformer(MODEL_NAME)
    texts = [chunk["text"] for chunk in chunks_data]
    embeddings_data = embedding_model.encode(
        texts,
        show_progress_bar=True
    )
    return embeddings_data

def store_embeddings(chunks, embeddings):
    """Store document chunks and embeddings in ChromaDB."""
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )
    collection_data = client.get_or_create_collection(
        name=COLLECTION_NAME,
         metadata={"hnsw:space": "cosine"}
    )
    for i, chunk in enumerate(chunks):
        collection_data.add(
            ids=[chunk["id"]],
            documents=[chunk["text"]],
            metadatas=[
                {
                    "chunk_id": chunk["id"],
                    "source": chunk["source"]
                }
            ],
            embeddings=[embeddings[i].tolist()]
        )
    print("All chunks stored successfully.")
    return collection_data

def verification(collection_data):
    """Verify if all chunks are stored in ChromaDB."""
    embedding_model  = SentenceTransformer(MODEL_NAME)
    query = "How long does a refund take?"
    query_embedding = embedding_model.encode([query])[0].tolist()
    results = collection_data.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    print(results["documents"])

if __name__ == '__main__':
    """Run the document embedding pipeline."""
    documents = load_documents()
    print(f"Documents loaded: {len(documents)}")
    chunks_info = create_chunks(documents)
    print(f"Chunks created: {len(chunks_info)}")
    embeddings_info = create_embeddings(chunks_info)
    print(f"Embeddings generated: {len(embeddings_info)}")
    collection = store_embeddings(
        chunks_info,
        embeddings_info
    )
    #Verify/Test results here
    #verification(collection)
    print(f"Collection: {collection.name}")
    print(f"Documents stored: {collection.count()}")
