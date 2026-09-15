import styles from "./Avatar.module.css";

export default function Avatar({ src, username, size = "md" }) {
    const initials = username?.[0]?.toUpperCase() ?? "?";
    return (
        <div className={`${styles.avatar} ${styles[size]}`}>
            {src
                ? <img src={src} alt={username} className={styles.img} />
                : <span className={styles.initials}>{initials}</span>
            }
        </div>
    );
}