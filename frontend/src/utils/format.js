export function formatCount(n) {
    if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
    if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
    return String(n);
}

export function formatRelativeTime(isoString) {
    const diff = (Date.now() - new Date(isoString)) / 1000;
    if (diff < 60) return `${Math.floor(diff)}s`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h`;
    if (diff < 604800) return `${Math.floor(diff / 86400)}d`;
    return new Date(isoString).toLocaleDateString();
}

export function extractHashtags(caption) {
    return [...caption.matchAll(/#(\w+)/g)].map((m) => m[1].toLowerCase());
}