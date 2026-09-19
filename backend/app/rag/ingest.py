from backend.app.rag.vectorstore import get_vector_store
from backend.app.rag.knowledge_data import KNOWLEDGE_DOCUMENTS

def ingest_fitness_knowledge(force: bool = False):
    """
    Ingest curated fitness knowledge documents into ChromaDB.
    If already ingested and not force, skips ingestion.
    """
    collection = get_vector_store()
    current_count = collection.count()

    if current_count > 0 and not force:
        print(f"[RAG Ingest] ChromaDB already contains {current_count} documents. Skipping ingestion.")
        return current_count

    print(f"[RAG Ingest] Ingesting {len(KNOWLEDGE_DOCUMENTS)} fitness knowledge documents...")

    # If force, delete existing
    if force and current_count > 0:
        existing_ids = collection.get()["ids"]
        if existing_ids:
            collection.delete(ids=existing_ids)

    ids = []
    documents = []
    metadatas = []

    for item in KNOWLEDGE_DOCUMENTS:
        doc_id = item["id"]
        title = item["title"]
        category = item["category"]
        tags = ", ".join(item.get("tags", []))
        content = item["content"].strip()

        # Combine title, category, and content for rich semantic indexing
        full_text = f"Title: {title}\nCategory: {category}\nKeywords: {tags}\n\n{content}"

        ids.append(doc_id)
        documents.append(full_text)
        metadatas.append({
            "title": title,
            "category": category,
            "tags": tags
        })

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    new_count = collection.count()
    print(f"[RAG Ingest] Successfully indexed {new_count} documents in ChromaDB.")
    return new_count

if __name__ == "__main__":
    ingest_fitness_knowledge(force=True)
