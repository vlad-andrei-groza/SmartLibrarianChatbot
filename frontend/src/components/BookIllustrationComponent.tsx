import { useEffect, useState } from "react";
import { fetchBookCover } from "../chat/api";
import "./book_styles.css";


export default function BookIllustration({ title, summary }: { title: string; summary: string }) {
    const [imageUrl, setImageUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleClick() {
        if (imageUrl) return;

        setLoading(true);
        setError(null);
        try {
            const url = await fetchBookCover(title, summary);
            setImageUrl(url);
        } catch (error) {
            setError("Failed to generate book illustration");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        return () => {
            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }
        }
    }, [imageUrl]);

    return (
        <div className="cover-container">
            {!imageUrl && (
                <button className="cover-button" onClick={handleClick} disabled={loading}>
                    {loading ? "Generating…" : "View book illustration"}
                </button>
            )}
            {error && <div className="cover-error">{error}</div>}
            {imageUrl && <img className="cover-image" src={imageUrl} alt={`Illustration for ${title}`} />}
        </div>
    )
}
