import chromadb
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")


openai_client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name="books")


def embed(q: str):
    return openai_client.embeddings.create(model=EMBEDDING_MODEL, input=q).data[0].embedding


def search_by_context(query: str, k: int = 5):
    """Return top-k matches with titles + snippets by semantic similarity."""
    query_embed = embed(query)
    res = collection.query(query_embeddings=[query_embed], n_results=k)
    results = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        results.append({
            "title": meta.get("title"),
            "snippet": doc,
            "score": 1 - dist
        })

    # Sort best first (higher similarity)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


if __name__ == "__main__":
    # quick manual test
    for q in ["friendship and fantasy", "war story", "post-apocalyptic hope"]:
        print(f"\nQuery: {q}")
        for hit in search_by_context(q, k=3):
            print(f"  -> {hit['title']} (score={hit['score']:.3f})")
