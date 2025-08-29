import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

# Global configuration variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "books")
BOOKS_FILE = os.getenv("BOOK_SUMMARIES_FILE", "data/book_summaries.txt")
OPENAI_MODEL = "gpt-4o-mini"
MODEL_MODERATION = "omni-moderation-latest"
TTS_MODEL = "gpt-4o-mini-tts"
IMAGE_GENERATION_MODEL = "dall-e-3"
openai_client = OpenAI(api_key=OPENAI_API_KEY)