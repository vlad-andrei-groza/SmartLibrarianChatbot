from uuid import uuid5
import chromadb
from dotenv import load_dotenv
import os
from openai import OpenAI
import uuid


# Configuration for ChromaDB
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
BOOKS_FILE = os.getenv("BOOK_SUMMARIES_FILE", "data/book_summaries.txt")

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
    Create embeddings for the input text using OpenAI's embedding model
    :param input_text: the text to be embedded
    :return: the list of embeddings
    """
    embedding_response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=input_text,
    )
    return [d.embedding for d in embedding_response.data]


def load_book_summaries():
    items = parse_book_summaries(BOOKS_FILE)
    if not items:
        print(f"No book summaries parsed from {BOOKS_FILE}.")
        return

    global collection
    if collection.count():
        chroma.delete_collection("books")
        collection = chroma_client.get_or_create_collection(
            name="books",
            metadata={"hnsw:space": "cosine"}
        )

    ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, it['title'])) for it in items]
    texts = [it['summary'] for it in items]
    metadatas = [{"title": it['title']} for it in items]

    embeddings = create_embeddings(texts)
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Loaded {len(items)} book summaries into ChromaDB collection 'books'.")

if __name__ == "__main__":
    # load_book_summaries()

    print(OpenAI().models.list())
