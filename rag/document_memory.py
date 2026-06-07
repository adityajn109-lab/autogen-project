from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import uuid
import os
from datetime import datetime


class DocumentMemory:

    def __init__(self):
        self.model = SentenceTransformer("./bge-small-en-v1.5")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(BASE_DIR, "chroma_db")

        # print("✅ Chroma DB Path:", self.db_path)

        self.client = chromadb.PersistentClient(
           path=self.db_path
        )
        self.processed_files = set()
        self.collection = self.client.get_or_create_collection(name="docs")

    # ✅ Chunking
    def chunk_text(self, text, chunk_size=500):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # ✅ Add document (WITH persistence + metadata)
    def add_document(self, text, file_id):
        
        # ✅ Skip if already processed
        if file_id in self.processed_files:
            print("File already processed 🚫")
            return

        chunks = self.chunk_text(text)

        embeddings = self.model.encode(chunks).tolist()
        ids = [str(uuid.uuid4()) for _ in chunks]

        metadatas = [
            {
                "timestamp": datetime.utcnow().isoformat()
            }
            for _ in chunks
        ]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

        # ✅ IMPORTANT: force save to disk
        print(f"✅ Stored {len(chunks)} chunks")

    # ✅ Query top-k chunks
    def query(self, query_text, k=3):
        query_embedding = self.model.encode([query_text]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k
        )

        return results["documents"][0]

    # ✅ Debug: show stored documents
    def show_all_docs(self):
        data = self.collection.get(include=["documents", "metadatas"])

        for doc, meta in zip(data["documents"], data["metadatas"]):
            print(meta["timestamp"], "→", doc[:80])

    # ✅ Debug: count
    def count(self):
        return self.collection.count()


def build_context(chunks):
    return "\n\n".join(chunks)