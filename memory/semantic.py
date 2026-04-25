import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pathlib import Path

CHROMA_PATH = Path.home() / ".local" / "share" / "lyra" / "chroma"
COLLECTION_NAME = "lyra_memory"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3

_embedding_fn = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)


def _collection():
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_embedding_fn,
    )


def store_exchange(session_id: str, user_text: str, assistant_text: str, timestamp: float) -> None:
    """Embed and persist one conversation turn for future retrieval."""
    col = _collection()
    col.add(
        ids=[f"{session_id}_{timestamp}"],
        documents=[f"User: {user_text}\nAssistant: {assistant_text}"],
        metadatas=[{"session_id": session_id, "timestamp": timestamp}],
    )


def retrieve_relevant(query: str, top_k: int = TOP_K) -> list[str]:
    """Return the top_k past exchanges most semantically similar to query."""
    col = _collection()
    count = col.count()
    if count == 0:
        return []
    results = col.query(
        query_texts=[query],
        n_results=min(top_k, count),
    )
    return results["documents"][0] if results["documents"] else []
