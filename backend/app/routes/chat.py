import json
from app.config import openai_client, OPENAI_MODEL, MODEL_MODERATION
from app.retriever import search_by_context
from app.tools.book_summaries_tool import SYSTEM_PROMPT, TOOLS, get_summary_by_title
from pydantic import BaseModel, Field
from typing import List
from fastapi import APIRouter, HTTPException


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3)
    k: int = Field(3, ge=1, le=10, description="Number of top results to retrieve (1-10)")


class CandidateBook(BaseModel):
    title: str
    snippet: str
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score between 0 and 1")


class ChatResponse(BaseModel):
    recommendation: str
    summary: str
    reason: str
    candidates: List[CandidateBook]


router = APIRouter(prefix="/chat", tags=["chat"])


def moderation_check(text: str):
    try:
        result = openai_client.moderations.create(
            model=MODEL_MODERATION,
            input=text
        )
        print("Moderation result:", result.results[0].flagged)
        return bool(result.results and result.results[0].flagged)
    except Exception:
        print("Moderation failed")
        return False


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message.strip()

    if moderation_check(user_message):
        raise HTTPException(status_code=400, detail="Your message appears to contain inappropriate language. Please rephrase.")

    candidates = search_by_context(user_message, k=request.k)
    if not candidates:
        raise HTTPException(status_code=404, detail="No candidates found for your request.")

    docs = "\n\n".join([f"### {c['title']}\n{c['snippet']}" for c in candidates])
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
        {"role": "system", "content": "Retrieved candidates:\n" + docs}
    ]

    first_response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.3
    )
    message = first_response.choices[0].message

    title = "Unknown"
    summary_text = ""
    reason = "Here is a recommendation."

    if message.tool_calls:
        tc = message.tool_calls[0]
        if tc.function.name == "get_summary_by_title":
            args = json.loads(tc.function.arguments)
            title = args.get("title", "Unknown")
            summary_text = get_summary_by_title(title)

            # Return tool result to the model for a natural final message
            messages.append({
                "role": "assistant",
                "tool_calls": [{
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": "get_summary_by_title", "arguments": tc.function.arguments}
                }]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": "get_summary_by_title",
                "content": summary_text
            })

            final = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.3
            )
            reason = final.choices[0].message.content
        else:
            reason = "I couldn't fetch the full summary for the recommended title."
    else:
        # Fallback: try to pick a retrieved title mentioned in the LLM text
        reason = message.content or reason
        for h in candidates:
            if h["title"] in reason:
                title = h["title"]
                summary_text = get_summary_by_title(title)
                break

    books = [CandidateBook(title=c["title"], snippet=c["snippet"], score=c["score"]) for c in candidates]

    return ChatResponse(
        recommendation=title,
        summary=summary_text,
        reason=reason,
        candidates=books
    )
