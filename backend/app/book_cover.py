import base64
import hashlib
from pathlib import Path
from typing import Tuple

from app.config import IMAGE_GENERATION_MODEL, openai_client

COVER_CACHE_DIR = Path("generated_book_images").resolve()
COVER_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _hash_key(*parts: str) -> str:
    """Create a short hash key from multiple string parts."""
    h = hashlib.sha256()
    for p in parts:
        h.update((p or "").encode("utf-8"))
        h.update(b"|")
    return h.hexdigest()[:32]


def build_book_cover_prompt(title: str, summary: str) -> str:
    """Build a prompt for generating a book cover image."""
    prompt = (
        f"Create a captivating book cover for the following book.\n"
        f"Title: {title}\n"
        f"Summary: {summary}\n"
        f"The cover should be visually appealing and reflect the essence of the book."
        f"Do not imitate or recreate any existing copyrighted book cover.\n"
        "No logos or trademarks."
    )
    return prompt


def generate_book_cover(title: str, summary: str) -> Tuple[bytes, str]:
    if not title or not summary:
        raise ValueError("Both title and summary must be provided.")

    prompt = build_book_cover_prompt(title, summary)
    cache_key = _hash_key(title, summary, IMAGE_GENERATION_MODEL)
    cache_path = COVER_CACHE_DIR / f"{cache_key}.png"

    if cache_path.exists():
        return cache_path.read_bytes(), cache_key

    response = openai_client.images.generate(
        model=IMAGE_GENERATION_MODEL,
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )

    b64 = response.data[0].b64_json
    png_bytes = base64.b64decode(b64)

    if not (len(png_bytes) > 8 and png_bytes[:8] == b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Image generation failed: invalid PNG payload.")

    cache_path.write_bytes(png_bytes)
    return png_bytes, cache_key

