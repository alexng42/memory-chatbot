import chromadb
import os
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "D:\\chroma_db"
os.makedirs(CHROMA_DIR, exist_ok=True)

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=CHROMA_DIR)

# Create or load collection
collection = client.get_or_create_collection(name="conversations")

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# takes a message and converts it to a vector using embedded model
# stores in ChromaDB with metadata (role and date)
def store_message(message_id, text, role, date):
    embedding = model.encode(text).tolist()
    collection.add(
        ids=[message_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"role": role, "date": date}]
    )

# converts query into a vector, finds results most similar in ChromaDB and returns them w/ metadata
def search_messages(query, n_results=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results["documents"][0], results["metadatas"][0]