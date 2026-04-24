from rag.milvus_client import search_opening, init_knowledge_base, COLLECTION_NAME
from pymilvus import utility


def search_openings(query: str, top_k: int = 3) -> list[dict]:
    """Recherche vectorielle via Milvus."""
    try:
        if not utility.has_collection(COLLECTION_NAME):
            init_knowledge_base()
        
        collection = None
        if utility.has_collection(COLLECTION_NAME):
            from pymilvus import Collection
            collection = Collection(COLLECTION_NAME)
            collection.load()
        
        if collection:
            results = search_opening(query, collection, top_k=top_k)
            return results
        return []
    except Exception as e:
        return []
