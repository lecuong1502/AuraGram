import { useState } from "react";
import { Link } from "react-router-dom";
import { useToggleLike } from "@/hooks/usePosts";
import { useMe } from "@/hooks/useAuth";
import Avatar from "@/components/common/Avatar";
import PostMedia from "./PostMedia";
import CommentList from "@/components/comment/CommentList";
import { formatCount, formatRelativeTime } from "@/utils/format";
import styles from "./PostCard.module.css";


export default function PostCard({ post }) {
    const { data: me } = useMe();
    const toggleLike = useToggleLike(post.id);
    const [showComments, setShowComments] = useState(false);

    return (
        <article className={styles.card}>
            {/* Header */}
            <div className={styles.header}>
                <Link to={`/${post.author?.username}`} className={styles.author}>
                    <Avatar src={post.author?.avatar_url} username={post.author?.username} size="sm" />
                    <span className={styles.username}>{post.author?.username}</span>
                </Link>
                <span className={styles.time}>{formatRelativeTime(post.created_at)}</span>
            </div>

            {/* Media */}
            <PostMedia media={post.media} />

            {/* Actions */}
            <div className={styles.actions}>
                <button
                    className={`${styles.likeBtn} ${post.liked ? styles.liked : ""}`}
                    onClick={() => toggleLike.mutate()}
                >
                    {post.liked ? "❤️" : "🤍"} {formatCount(post.like_count)}
                </button>
                <button className={styles.commentBtn} onClick={() => setShowComments((s) => !s)}>
                    💬 {formatCount(post.comment_count)}
                </button>
                <Link to={`/p/${post.id}`} className={styles.shareBtn}>↗</Link>
            </div>

            {/* Caption */}
            {post.caption && (
                <p className={styles.caption}>
                    <Link to={`/${post.author?.username}`} className={styles.captionAuthor}>
                        {post.author?.username}
                    </Link>{" "}
                    {post.caption}
                </p>
            )}

            {/* Hashtags */}
            {post.hashtags?.length > 0 && (
                <div className={styles.hashtags}>
                    {post.hashtags.map((tag) => (
                        <span key={tag} className={styles.tag}>#{tag}</span>
                    ))}
                </div>
            )}

            {/* Comments */}
            {showComments && <CommentList postId={post.id} />}
        </article>
    );
}