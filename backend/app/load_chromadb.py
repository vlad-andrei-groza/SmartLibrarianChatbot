import chromadb
from config import OPENAI_API_KEY, CHROMA_DIR, EMBEDDING_MODEL, BOOKS_FILE
from openai import OpenAI
import uuid


# openai and chromadb clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = chroma_client.get_or_create_collection(
    name="books",
    metadata={"hnsw:space": "cosine"}
)


def parse_book_summaries(file_path):
    """
    Parses the book summaries from the file in the format:
    ## Title: Title of the Book
    line
    line
    (blank line separates books)
    :param file_path: the path to the book summaries file
    :return: a list of dictionaries with book titles and summaries
    """
    with open (file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()

    docs = []

    books = [b.strip() for b in content.split('\n\n')]
    for book in books:
        lines = [ln.rstrip() for ln in book.splitlines() if ln.strip() != ""]
        if not lines or not lines[0].startswith("## Title:"):
            continue
        title = lines[0].replace("## Title:", "").strip()
        summary = " ".join(lines[1:]).strip()
        if not summary:
            continue
        docs.append({
            "title": title,
            "summary": f"Title: {title}\n{summary}"
        })

    return docs


def create_embeddings(input_text):
    """
    Uses OpenAI to create embeddings for a list of texts.
    :param input_text: list of strings
    :return: list of embeddings
    """
    response = openai_client.embeddings.create(
        input=input_text,
        model=EMBEDDING_MODEL
    )
    return [e.embedding for e in response.data]


def load_books_to_chromadb():
    docs = parse_book_summaries(BOOKS_FILE)
    summaries = [doc["summary"] for doc in docs]
    titles = [doc["title"] for doc in docs]
    ids = [str(uuid.uuid4()) for _ in docs]
    embeddings = create_embeddings(summaries)
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=summaries,
        metadatas=[{"title": t} for t in titles]
    )
    return ids


def get_retriever():
    """
    Returns a retriever object for semantic search.
    """
    return collection.as_retriever()

# If run as script, load books
if __name__ == "__main__":
    load_books_to_chromadb()
