import { useEffect, useMemo, useRef, useState } from "react";
import { sendChatMessage } from "./api";
import type { ChatResponse } from "../utils/types";
import "./chat_styles.css";

type ChatTurn =
    | { id: string; role: "user"; text: string }
    | { id: string; role: "assistant"; data: ChatResponse };

function AssistantMessage({ data }: { data: ChatResponse }) {
    const { recommendation, summary, reason } = data;
    if (recommendation === "Unknown") {
        return (
            <div className="assistant-bubble">
                <div className="assistant-reason">{reason}</div>
            </div>
        );
    }
    return (
        <div className="assistant-bubble">
            <div className="assistant-title">{recommendation}</div>
            <div className="assistant-summary">{summary}</div>
            <div className="assistant-reason">{reason}</div>
        </div>
    );
}

export default function ChatComponent() {
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [turns, setTurns] = useState<ChatTurn[]>([]);
    const bottomRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
    }, [turns, loading]);

    const canSend = useMemo(() => input.trim().length > 2 && !loading, [input, loading]);

    async function onSubmit(e: React.FormEvent) {
        e.preventDefault();
        const message = input.trim();
        if (!message) return;

        setTurns((t) => [...t, { id: crypto.randomUUID(), role: "user", text: message }]);
        setInput("");
        setLoading(true);

        try {
            const data = await sendChatMessage({ message, k: 3 });
            setTurns((t) => [...t, { id: crypto.randomUUID(), role: "assistant", data }]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="chat-shell">
            <div className="chat-thread">
                {turns.map((t) =>
                    t.role === "user" ? (
                        <div key={t.id} className="row user-row">
                            <div className="user-bubble">{t.text}</div>
                        </div>
                    ) : (
                        <div key={t.id} className="row assistant-row">
                            <AssistantMessage data={t.data} />
                        </div>
                    )
                )}

                {loading && (
                    <div className="row assistant-row">
                        <div className="assistant-bubble">Thinking…</div>
                    </div>
                )}
                <div ref={bottomRef} />
            </div>

            {/* Composer sits at the very bottom of the page because of flex layout */}
            <form className="chat-composer" onSubmit={onSubmit}>
                <input
                    className="chat-input"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your request"
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            if (canSend) onSubmit(e);
                        }
                    }}
                />
                <button className="chat-send" type="submit" disabled={!canSend}>
                    {loading ? "…" : "Send"}
                </button>
            </form>
        </div>
    );
}
