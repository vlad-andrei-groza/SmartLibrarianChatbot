import chromadb
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
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
    for query in ["friendship and fantasy", "war story", "post-apocalyptic hope"]:
        print(f"\nQuery: {query}")
        for book in search_by_context(query, k=3):
            print(f"  -> {book['title']} (score={book['score']:.3f})")