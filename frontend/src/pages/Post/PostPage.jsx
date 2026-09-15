import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { postsApi } from "@/api/posts.api";
import { useToggleLike } from "@/hooks/usePosts";
import PostMedia from "@/components/post/PostMedia";
import CommentList from "@/components/comment/CommentList";
import Avatar from "@/components/common/Avatar";
import { formatCount, formatRelativeTime } from "@/utils/format";
import styles from "./PostPage.module.css";


export default function PostPage() {
    const { postId } = useParams();

    const { data: post, isLoading } = useQuery({
        queryKey: ["post", postId],
        queryFn: () => postsApi.getPost(postId),
    });

    const toggleLike = useToggleLike(postId);

    if (isLoading) return <p className={styles.loading}>Loading...</p>;
    if (!post) return <p className={styles.loading}>Post not found.</p>;

    return (
        <div className={styles.page}>
            <div className={styles.container}>
                {/* Left: media */}
                <div className={styles.media}>
                    <PostMedia media={post.media} />
                </div>

                {/* Right: details */}
                <div className={styles.details}>
                    <div className={styles.header}>
                        <Link to={`/${post.author?.username}`} className={styles.author}>
                            <Avatar src={post.author?.avatar_url} username={post.author?.username} size="sm" />
                            <span className={styles.username}>{post.author?.username}</span>
                        </Link>
                    </div>

                    {post.caption && (
                        <p className={styles.caption}>
                            <strong>{post.author?.username}</strong> {post.caption}
                        </p>
                    )}

                    <div className={styles.comments}>
                        <CommentList postId={post.id} />
                    </div>

                    <div className={styles.actions}>
                        <button
                            className={`${styles.likeBtn} ${post.liked ? styles.liked : ""}`}
                            onClick={() => toggleLike.mutate()}
                        >
                            {post.liked ? "❤️" : "🤍"} {formatCount(post.like_count)} likes
                        </button>
                        <span className={styles.time}>{formatRelativeTime(post.created_at)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}