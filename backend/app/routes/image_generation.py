from app.book_cover import generate_book_cover
from app.routes.chat import router as chat_router
from pydantic import BaseModel, Field
from fastapi import HTTPException, Response


class ImageGenerationRequest(BaseModel):
    title: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=10)


@chat_router.post(
    "/book_cover",
    responses={200: {"content": {"image/png": {"schema": {"type": "string", "format": "binary"}}}}},
    summary="Generate a representative book cover (PNG) for a recommendation"
)
def book_cover_endpoint(req: ImageGenerationRequest):
    try:
        png_bytes, cache_key = generate_book_cover(req.title.strip(), req.summary.strip())
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f'inline; filename="{cache_key}.png"',
                "Cache-Control": "no-store",
                "X-Cover-Cache-Key": cache_key,
            },
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cover generation error: {e}")
