from ast import Dict, List

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import uuid
import os
import hashlib
from datetime import datetime
from typing import List, Dict

class DocumentMemory:
 
    def __init__(self, model_path: str = "./bge-small-en-v1.5"):
        self.model = SentenceTransformer(model_path)
        print(f"Loaded embedding model from {model_path}")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(BASE_DIR, "chroma_db")
        self.client = chromadb.PersistentClient(path=self.db_path)
 
        # Main collection: stores document chunks
        self.collection = self.client.get_or_create_collection(
            name="docs",
            embedding_function=None   # ← this line stops the auto-download
        )
        print(f"Initialized ChromaDB at {self.db_path}")
 
        # FIX: persist processed file hashes in a separate collection
        # so dedup survives server restarts
        self.file_registry = self.client.get_or_create_collection(
            name="file_registry",
            embedding_function=None
        ) 

        print("DocumentMemory initialized with 2 collections: 'docs' and 'file_registry'")
    # ─── CHUNKING ────────────────────────────────────────
 
    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 100,         # FIX: add overlap — prevents lost context at boundaries
    ) -> List[str]:
        """
        Sliding window chunker with overlap.
        overlap=100 means each chunk shares 100 chars with the previous one,
        so a sentence split across a boundary still appears in full in one chunk.
        """
        chunks = []
        start = 0
        print(f"Chunking text of length {len(text)} with chunk_size={chunk_size} and overlap={overlap}")
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end == len(text):
                break
            start += chunk_size - overlap  # slide with overlap
        print(f"Created {len(chunks)} chunks")
        return chunks
 
    # ─── INDEXING ────────────────────────────────────────
 
    def is_already_processed(self, file_hash: str) -> bool:
        """Check persistent registry — survives restarts."""
        try:
            result = self.file_registry.get(ids=[file_hash])
            return len(result["ids"]) > 0
        except Exception:
            return False
 
    def add_document(self, text: str, file_hash: str, file_name: str = "unknown"):
        # FIX: check persistent registry, not in-memory set
        if self.is_already_processed(file_hash):
            print(f"Already indexed: {file_name} — skipping")
            return
 
        chunks = self.chunk_text(text)
        if not chunks:
            print(f"Warning: no text extracted from {file_name}")
            return
        print(f"Encoding {len(chunks)} chunks from '{file_name}'...")
        embeddings = self.model.encode(chunks, show_progress_bar=False).tolist()
        print(f"Generated embeddings for {len(chunks)} chunks from '{file_name}'")
        ids = [str(uuid.uuid4()) for _ in chunks]
        timestamp = datetime.utcnow().isoformat()
 
        # POWER-UP: rich metadata for every chunk
        metadatas = [
            {
                "file_name": file_name,       # which file this came from
                "file_hash": file_hash,        # for audit / tracing
                "chunk_index": i,              # position within the document
                "total_chunks": len(chunks),
                "timestamp": timestamp,
            }
            for i, _ in enumerate(chunks)
        ]
        print(f"Indexing {len(chunks)} chunks from '{file_name}' with hash {file_hash[:8]}...")
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )
        print(f"Indexed {len(chunks)} chunks from '{file_name}' into 'docs' collection")
        # Register file as processed (persistent)
        self.file_registry.add(
            ids=[file_hash],
            embeddings=[[0.0]],   # ← required by ChromaDB, just a placeholder
            metadatas=[{"file_name": file_name, "timestamp": timestamp}],
        )
 
        print(f"Indexed {len(chunks)} chunks from '{file_name}'")
 
    # ─── RETRIEVAL ───────────────────────────────────────
 
    def query(self, query_text: str, k: int = 4) -> List[Dict]:
        """
        Returns chunks WITH their source metadata.
        POWER-UP: you can now cite which file/page the answer came from.
        """
        query_embedding = self.model.encode([query_text]).tolist()
 
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )
 
        chunks = []
        for i in range(len(results["documents"][0])):
            chunks.append({
                "text": results["documents"][0][i],
                "file_name": results["metadatas"][0][i].get("file_name", "unknown"),
                "chunk_index": results["metadatas"][0][i].get("chunk_index", "?"),
                "score": round(1 - results["distances"][0][i], 3),  # similarity score
            })
        return chunks
 
    def delete_document(self, file_hash: str):
        """Remove all chunks for a specific file (useful for re-indexing)."""
        results = self.collection.get(where={"file_hash": file_hash})
        if results["ids"]:
            self.collection.delete(ids=results["ids"])
        try:
            self.file_registry.delete(ids=[file_hash])
        except Exception:
            pass
        print(f"Deleted document with hash {file_hash[:8]}...")
 
    def list_files(self):
        data = self.file_registry.get(include=["metadatas"])
        return [
            {"file_name": meta.get("file_name"), "timestamp": meta.get("timestamp")}
            for meta in data["metadatas"]
        ]
 
    def count(self) -> int:
        return self.collection.count()
 
 
# ─────────────────────────────────────────────────────────
# CONTEXT BUILDER
# ─────────────────────────────────────────────────────────
 
def build_context(chunks: List[Dict]) -> str:
    """
    POWER-UP: include source citation in every chunk block.
    The LLM can now say 'According to report.pdf...'
    """
    parts = []
    for c in chunks:
        header = f"[Source: {c['file_name']} | chunk {c['chunk_index']} | score {c['score']}]"
        parts.append(f"{header}\n{c['text']}")
    return "\n\n---\n\n".join(parts)
 