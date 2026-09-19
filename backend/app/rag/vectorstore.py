from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.app.config import settings

_chroma_client: Optional[chromadb.PersistentClient] = None
_collection = None

def get_chroma_client() -> chromadb.PersistentClient:
    """Singleton getter for ChromaDB persistent client"""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
    return _chroma_client

def get_vector_store():
    """Retrieve or create the fitness knowledge collection"""
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name="fitness_knowledge",
            metadata={"description": "Curated fitness, nutrition, and supplement knowledge base"}
        )
    return _collection

def query_knowledge_base(query: str, n_results: int = 3, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search ChromaDB for relevant fitness knowledge.
    Returns list of dicts with title, category, snippet, and relevance score.
    """
    collection = get_vector_store()
    
    # Check if collection is empty
    count = collection.count()
    if count == 0:
        return []

    # Adjust n_results if collection has fewer items
    fetch_count = min(n_results, count)

    where_filter = {"category": category} if category else None

    try:
        results = collection.query(
            query_texts=[query],
            n_results=fetch_count,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )

        formatted = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
            distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)

            for doc, meta, dist in zip(docs, metas, distances):
                score = round(1.0 - (dist / 2.0), 3) if dist is not None else 0.85
                formatted.append({
                    "title": meta.get("title", "Fitness Science Guide"),
                    "category": meta.get("category", "General"),
                    "snippet": doc,
                    "score": score
                })
        return formatted
    except Exception as e:
        print(f"[VectorStore] Error querying ChromaDB: {e}")
        return []
