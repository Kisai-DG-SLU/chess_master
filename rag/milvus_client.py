from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from typing import list


COLLECTION_NAME = "chess_openings"
DIMENSION = 768


def get_embedding(text: str) -> list[float]:
    """Generate embedding for text using a simple hash-based approach.
    In production, use OpenAI embeddings or similar.
    """
    import hashlib
    import struct
    
    hash_bytes = hashlib.sha256(text.encode()).digest()
    seed = struct.unpack('<Q', hash_bytes[:8])[0]
    
    import random
    random.seed(seed)
    return [random.random() * 2 - 1 for _ in range(DIMENSION)]


def create_collection():
    """Create Milvus collection for chess openings."""
    connections.connect(host="localhost", port="19530")
    
    if utility.has_collection(COLLECTION_NAME):
        utility.drop_collection(COLLECTION_NAME)
    
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="opening_name", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="moves", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=4096),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
    ]
    
    schema = CollectionSchema(fields=fields, description="Chess openings knowledge base")
    collection = Collection(name=COLLECTION_NAME, schema=schema)
    
    index_params = {
        "metric_type": "IP",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    
    return collection


def ingest_opening(name: str, moves: str, description: str, collection: Collection):
    """Ingest a chess opening into the vector database."""
    embedding = get_embedding(f"{name} {moves} {description}")
    
    entities = [
        [name],
        [moves],
        [description],
        [embedding]
    ]
    
    collection.insert(entities)
    collection.flush()


def search_opening(query: str, collection: Collection, top_k: int = 5) -> list[dict]:
    """Search for similar openings in the knowledge base."""
    query_embedding = get_embedding(query)
    
    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
    
    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["opening_name", "moves", "description"]
    )
    
    return [
        {
            "opening_name": hit.entity.get("opening_name"),
            "moves": hit.entity.get("moves"),
            "description": hit.entity.get("description"),
            "score": hit.distance
        }
        for hit in results[0]
    ]


def init_knowledge_base():
    """Initialize the knowledge base with sample openings."""
    collection = create_collection()
    
    openings = [
        ("Ruy Lopez", "1.e4 e5 2.Nf3 Nc6 3.Bb5", 
         "Classical opening dating to 1561. One of the most popular and theoretically important openings. A favourite of many world champions."),
        ("Sicilian Defense", "1.e4 c5",
         "The most popular response to 1.e4. Leads to sharp, tactical positions. Many variations including Open, Closed, and Siciilian Defense."),
        ("Queen's Gambit", "1.d4 d5 2.c4",
         "One of the oldest and most respected openings. White sacrifices a pawn for better development and central control."),
        ("King's Indian Defense", "1.d4 Nf6 2.c4 g6",
         "Hypermodern opening where Black allows White to occupy the center before attacking it. Popular among aggressive players."),
        ("French Defense", "1.e4 e6",
         "Solid defensive opening. Leads to varied positions with pawn structures unique to this opening."),
        ("Caro-Kann Defense", "1.e4 c6",
         "Solid response to 1.e4. Less sharper than the Sicilian but leads to reliable positions."),
        ("London System", "1.d4 Nf6 2.Bf4",
         "Reliable system that can be played against almost any Black setup. Popular at all levels."),
        ("Reti Opening", "1.Nf3 d5 2.c4",
         "Hypermodern opening that controls the center with pieces rather than pawns.")
    ]
    
    for name, moves, desc in openings:
        ingest_opening(name, moves, desc, collection)
    
    collection.load()
    return collection


if __name__ == "__main__":
    print("Initializing chess knowledge base...")
    collection = init_knowledge_base()
    print(f"Collection '{COLLECTION_NAME}' created with {collection.num_entities} entities")
    
    print("\nSearching for 'aggressive tactical opening'...")
    results = search_opening("aggressive tactical opening", collection)
    for r in results:
        print(f"  - {r['opening_name']}: {r['moves']} (score: {r['score']:.3f})")
