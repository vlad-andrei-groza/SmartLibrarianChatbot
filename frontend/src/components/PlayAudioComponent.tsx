import { useEffect, useRef, useState } from "react";
import { fetchTTSAudio } from "../chat/api";
import { FaStop, FaSpinner } from "react-icons/fa";
import "./audio_button_styles.css";


export default function PlayAudioButton({ text, voice = "shimmer" }: { text: string; voice?: string }) {
    const [playing, setPlaying] = useState(false);
    const [loading, setLoading] = useState(false);
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const audioUrlRef = useRef<string | null>(null);

    async function handleClick() {
        if (playing && audioRef.current) {
            audioRef.current.pause();
            audioRef.current.currentTime = 0;
            setPlaying(false);
            return;
        }

        setLoading(true);
        try {
            const url = await fetchTTSAudio(text, voice);
            audioUrlRef.current = url;
            if (!audioRef.current) {
                audioRef.current = new Audio();
                audioRef.current.addEventListener("ended", () => setPlaying(false));
                audioRef.current.addEventListener("pause", () => setPlaying(false));
            }
             audioRef.current.src = url;
            await audioRef.current.play();
            setPlaying(true);
        } catch (error) {
            console.error("Error fetching TTS audio:", error);
            alert("Failed to fetch audio. Please try again later.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        return () => {
            if (audioUrlRef.current) {
                URL.revokeObjectURL(audioUrlRef.current);
                audioUrlRef.current = null;
            }
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current.src = "";
            }
        }
    }, [])

    return (
        <div className="audio-button-container">
            <button
            type="button"
            onClick={handleClick}
            disabled={loading}
            className="tts-button"
            title={playing ? "Stop" : "Listen"}
        >
            {loading ? (
                <FaSpinner className="icon spin" />
            ) : playing ? (
                <FaStop className="icon" />
            ) : (
                <span>🔊 Listen</span>
            )}
        </button>
        </div>
    );
}
