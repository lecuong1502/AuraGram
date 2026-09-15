import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { useProfile, useFollow } from "@/hooks/useProfile";
import { useMe } from "@/hooks/useAuth";
import { postsApi } from "@/api/posts.api";
import Avatar from "@/components/common/Avatar";
import Button from "@/components/common/Button";
import { formatCount } from "@/utils/format";
import styles from "./ProfilePage.module.css";

export default function ProfilePage() {
    const { username } = useParams();
    const { data: me } = useMe();
    const { data: profile, isLoading } = useProfile(username);
    const follow = useFollow(profile?.id);

    const { data: postsData } = useQuery({
        queryKey: ["userPosts", username],
        queryFn: () => postsApi.getFeed(),
        enabled: !!profile,
    });

    const isMe = me?.username === username;

    if (isLoading) return <p className={styles.loading}>Loading...</p>;
    if (!profile) return <p className={styles.loading}>User not found.</p>;

    return (
        <div className={styles.page}>
            {/* Header */}
            <div className={styles.header}>
                <Avatar src={profile.avatar_url} username={profile.username} size="xl" />
                <div className={styles.info}>
                    <div className={styles.top}>
                        <h1 className={styles.username}>{profile.username}</h1>
                        {isMe ? (
                            <Link to="/settings">
                                <Button variant="secondary" size="sm">Edit profile</Button>
                            </Link>
                        ) : (
                            <Button
                                size="sm"
                                variant={profile.is_following ? "secondary" : "primary"}
                                onClick={() => follow.mutate({ isFollowing: profile.is_following })}
                                loading={follow.isPending}
                            >
                                {profile.is_following ? "Following" : "Follow"}
                            </Button>
                        )}
                    </div>

                    <div className={styles.stats}>
                        <span><strong>{formatCount(profile.post_count)}</strong> posts</span>
                        <span><strong>{formatCount(profile.follower_count)}</strong> followers</span>
                        <span><strong>{formatCount(profile.following_count)}</strong> following</span>
                    </div>

                    {profile.full_name && <p className={styles.fullName}>{profile.full_name}</p>}
                    {profile.bio && <p className={styles.bio}>{profile.bio}</p>}
                </div>
            </div>

            {/* Photo grid */}
            <div className={styles.grid}>
                {postsData?.pages?.[0]?.posts?.map((post) => (
                    <Link key={post.id} to={`/p/${post.id}`} className={styles.gridItem}>
                        <img src={post.media[0]?.url} alt="" className={styles.gridImg} />
                        <div className={styles.overlay}>
                            <span>❤️ {formatCount(post.like_count)}</span>
                            <span>💬 {formatCount(post.comment_count)}</span>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}