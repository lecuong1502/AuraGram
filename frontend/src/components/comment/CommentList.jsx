// frontend/src/components/comment/CommentList.jsx
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { commentsApi } from "@/api/comments.api";
import { useMe } from "@/hooks/useAuth";
import Avatar from "@/components/common/Avatar";
import { formatRelativeTime } from "@/utils/format";
import styles from "./CommentList.module.css";

export default function CommentList({ postId }) {
    const { data: me } = useMe();
    const queryClient = useQueryClient();
    const [text, setText] = useState("");

    const { data: comments = [], isLoading } = useQuery({
        queryKey: ["comments", postId],
        queryFn: () => commentsApi.list(postId),
    });

    const addComment = useMutation({
        mutationFn: () => commentsApi.add(postId, text),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["comments", postId] });
            setText("");
        },
    });

    return (
        <div className={styles.wrapper}>
            {isLoading ? (
                <p className={styles.loading}>Loading comments...</p>
            ) : (
                comments.map((c) => (
                    <div key={c.id} className={styles.comment}>
                        <Avatar src={c.author?.avatar_url} username={c.author?.username} size="sm" />
                        <div className={styles.content}>
                            <span className={styles.username}>{c.author?.username}</span>
                            <span className={styles.text}>{c.content}</span>
                            <span className={styles.time}>{formatRelativeTime(c.created_at)}</span>
                            {c.replies?.map((r) => (
                                <div key={r.id} className={styles.reply}>
                                    <span className={styles.username}>{r.author?.username}</span>
                                    <span className={styles.text}>{r.content}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                ))
            )}

            {me && (
                <div className={styles.input}>
                    <input
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Add a comment..."
                        onKeyDown={(e) => e.key === "Enter" && text.trim() && addComment.mutate()}
                    />
                    <button
                        onClick={() => addComment.mutate()}
                        disabled={!text.trim() || addComment.isPending}
                    >
                        Post
                    </button>
                </div>
            )}
        </div>
    );
}