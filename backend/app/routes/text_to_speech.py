from typing import Optional

from app.config import openai_client, TTS_MODEL
from app.routes.chat import router as chat_router
from pydantic import BaseModel, Field
from fastapi import HTTPException
from fastapi.responses import StreamingResponse


MAX_INPUT_CHARS = 1500


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to read out loud")
    voice: Optional[str] = Field(None, description="Voice to use for TTS (e.g., shimmer, alloy)")
    audio_format: Optional[str] = Field("mp3", description="Audio format (e.g., mp3, wav)")


@chat_router.post("/tts", responses={200: {"content": {"audio/mpeg": {}}}})
def text_to_speech_endpoint(request: TTSRequest):
    if len(request.text) > MAX_INPUT_CHARS:
        raise HTTPException(status_code=413, detail=f"Text too long (>{MAX_INPUT_CHARS} chars).")

    try:
        def audio_stream():
            with openai_client.audio.speech.with_streaming_response.create(
                    model=TTS_MODEL,
                    voice=request.voice,
                    input=request.text,
                    response_format="mp3",
                    instructions="Speak on a tone that is engaging and expressive."
            ) as response:
                for chunk in response.iter_bytes():
                    yield chunk

        return StreamingResponse(
            audio_stream(),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": 'inline; filename="speech.mp3"',
                "Cache-Control": "no-store",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TTS streaming error: {e}")
