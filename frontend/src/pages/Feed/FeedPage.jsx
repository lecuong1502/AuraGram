// frontend/src/pages/Feed/FeedPage.jsx
import { useEffect, useRef } from "react";
import { useFeed } from "@/hooks/usePosts";
import PostCard from "@/components/post/PostCard";
import CreatePostModal from "@/components/post/CreatePostModal";
import styles from "./FeedPage.module.css";

export default function FeedPage() {
    const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading } = useFeed();
    const sentinelRef = useRef(null);

    // Infinite scroll via IntersectionObserver
    useEffect(() => {
        if (!sentinelRef.current) return;
        const observer = new IntersectionObserver(
            ([entry]) => { if (entry.isIntersecting && hasNextPage) fetchNextPage(); },
            { threshold: 0.1 }
        );
        observer.observe(sentinelRef.current);
        return () => observer.disconnect();
    }, [fetchNextPage, hasNextPage]);

    const posts = data?.pages.flatMap((p) => p.posts) ?? [];

    return (
        <div className={styles.page}>
            {isLoading && <p className={styles.loading}>Loading feed...</p>}

            {!isLoading && posts.length === 0 && (
                <div className={styles.empty}>
                    <p>No posts yet.</p>
                    <p>Follow some people to see their posts here!</p>
                </div>
            )}

            {posts.map((post) => <PostCard key={post.id} post={post} />)}

            <div ref={sentinelRef} className={styles.sentinel} />
            {isFetchingNextPage && <p className={styles.loading}>Loading more...</p>}

            <CreatePostModal />
        </div>
    );
}