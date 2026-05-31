from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import uuid


class DocumentMemory:

    def __init__(self):
        self.model = SentenceTransformer("./bge-small-en-v1.5")

        self.client = chromadb.Client(Settings(persist_directory="./chroma_db"))
        self.collection = self.client.get_or_create_collection(name="docs")

    # ✅ Chunking
    def chunk_text(self, text, chunk_size=500):
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])
        return chunks

    # ✅ Add document
    def add_document(self, text):
        chunks = self.chunk_text(text)

        embeddings = self.model.encode(chunks).tolist()
        ids = [str(uuid.uuid4()) for _ in chunks]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )

    # ✅ Query top-k chunks
    def query(self, query_text, k=3):
        query_embedding = self.model.encode([query_text]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k
        )

        return results["documents"][0]
    
def build_context(chunks):
        return "\n\n".join(chunks)