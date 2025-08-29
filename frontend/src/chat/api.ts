import type { ChatRequest, ChatResponse } from "../utils/types";


const API_BASE = import.meta.env.VITE_CHAT_API_BASE;

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


export async function fetchTTSAudio(text: string, voice: string): Promise<string> {
    const response = await fetch(`${API_BASE}/chat/tts`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text, voice }),
    });

    if (!response.ok) {
        let detail = `Error when turning text to audio (${response.status})`;
        try {
            const j = await response.json();
            detail = j?.detail ?? detail;
        } catch {}
        throw new Error(detail);
    }

    const blob = await response.blob();
    const audio_url = URL.createObjectURL(blob);
    return audio_url;
}


export async function fetchBookCover(title: string, summary: string): Promise<string> {
    const response = await fetch(`${API_BASE}/chat/book_cover`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, summary }),
    });

    if (!response.ok) {
        let detail = `Error when fetching book cover (${response.status})`;
        try {
            const j = await response.json();
            detail = j?.detail ?? detail;
        } catch {}
        throw new Error(detail);
    }

    const blob = await response.blob();
    const cover_url = URL.createObjectURL(blob);
    return cover_url;
}