import type { ChatRequest, ChatResponse } from "../utils/types";


const API_BASE = import.meta.env.CHAT_API_BASE || "http://localhost:8008";

export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
    });

    if (!response.ok) {
        let detail = "Something went wrong.";
        try {
            const j = await response.json();
            detail = j?.detail ?? detail;
        } 
        catch {}
        return {
            recommendation: "Unknown",
            summary: "",
            reason: detail,
            candidates: [],
        };
    }

    const data = (await response.json()) as ChatResponse;
    return data;
}
