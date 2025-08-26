import { useState } from "react";
import type { ChatResponse } from "../utils/types";
import { sendChatMessage } from "./api";

function RecommendationView({ data }: { data: ChatResponse }) {
  if (data.recommendation === "Unknown") {
    return (
      <div style={{ backgroundColor: "#222222ff", border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
        <div style={{ whiteSpace: "pre-wrap" }}>{data.reason}</div>
      </div>
    );
  }

  return (
    <div style={{ backgroundColor: "#222222ff", border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
      <div style={{ fontWeight: 700, fontSize: 18 }}>{data.recommendation}</div>
      <div style={{ marginTop: 8, whiteSpace: "pre-wrap" }}>{data.summary}</div>
      <div style={{ marginTop: 12, fontStyle: "italic", color: "#c5c5c5ff" }}>
        {data.reason}
      </div>
    </div>
  );
}

export default function ChatComponent() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [resp, setResp] = useState<ChatResponse | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    const message = input.trim();
    if (!message) return;
    setLoading(true);
    setResp(null);
    try {
      const data = await sendChatMessage({ message, k: 3 });
      setResp(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ 
        maxWidth: 720, 
        margin: "32px auto", 
        padding: 16, 
        fontFamily: "system-ui, sans-serif", 
        display: "flex", 
        flexDirection: "column",
        alignContent: "center",
        }}
    >
      <h1 style={{ marginBottom: 8, color: "#222222ff" }}>Book Recommender 📚</h1>
      <p style={{ marginTop: 40, color: "#555" }}>
        Ask for a book by themes, e.g. “I want a book about magic and friendship” or “What do you recommend for someone who loves war stories?”.
      </p>

      <form onSubmit={onSubmit} style={{ display: "flex", gap: 8, margin: "20px 0" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your request..."
          style={{ flex: 1, padding: 10, border: "1px solid #ccc", borderRadius: 8 }}
        />
        <button type="submit" disabled={loading} style={{ padding: "10px 16px" }}>
          {loading ? "Thinking…" : "Send"}
        </button>
      </form>

      {resp && <RecommendationView data={resp} />}

      {!resp && !loading && (
        <div style={{ marginTop: 16, color: "#666" }}>
          Try: <em>“friendship and fantasy”</em>, <em>“war stories”</em>, <em>“post-apocalyptic hope”</em>
        </div>
      )}
    </div>
  );
}