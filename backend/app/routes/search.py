from app.retriever import search_by_context
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter(prefix="/search", tags=["search"])


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Natural language query")
    k: int = Field(5, ge=1, le=20, description="Number of results")


class SearchHit(BaseModel):
    title: str
    snippet: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchHit]

@router.post("", response_model=SearchResponse, dependencies=[])
def search(req: SearchRequest):
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Query must not be empty.")
    hits = search_by_context(q, k=req.k)
    trimmed = [
        SearchHit(title=h["title"], snippet=trim(h["snippet"], 480), score=h["score"])
        for h in hits
    ]
    return SearchResponse(results=trimmed)


def trim(text: str, max_len: int = 480) -> str:
    if len(text) <= max_len:
        return text
    cut = text[:max_len]
    last_dot = cut.rfind(".")
    if last_dot > max_len * 0.6:
        return cut[:last_dot + 1] + " …"
    return cut.rstrip() + " …"
