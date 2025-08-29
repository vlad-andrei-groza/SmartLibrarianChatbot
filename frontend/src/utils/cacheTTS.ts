class CacheTTS {
    private cache: Map<string, string>;
    private order: string[] = [];
    private maxEntries: number;

    constructor(maxEntries = 15) {
        this.cache = new Map();
        this.maxEntries = maxEntries;
    }

    get(key: string): string | null {
        const url = this.cache.get(key);
        if (!url) return null;

        this.order = this.order.filter(k => k !== key);
        this.order.push(key);
        return url;
    }

    set(key: string, url: string) {
        if (this.cache.has(key)) {
            const old = this.cache.get(key)!;
            if (old !== url) URL.revokeObjectURL(old);
            this.order = this.order.filter(k => k !== key);
        }
        this.cache.set(key, url);
        this.order.push(key);

        if (this.order.length > this.maxEntries) {
            const evictKey = this.order.shift()!;
            const evictUrl = this.cache.get(evictKey);
            if (evictUrl) URL.revokeObjectURL(evictUrl);
            this.cache.delete(evictKey);
        }
    }

    has(key: string): boolean {
        return this.cache.has(key);
    }

    revokeAll() {
        for (const url of this.cache.values()) URL.revokeObjectURL(url);
        this.cache.clear();
        this.order = [];
    }
}

export const cacheTTS = new CacheTTS(15);
export const ttsKey = (text: string, voice: string) => `${voice}->${text}`;


// clean up on tab close/refresh to avoid leaking blob URLs
if (typeof window !== "undefined") {
  window.addEventListener("beforeunload", () => cacheTTS.revokeAll());
}