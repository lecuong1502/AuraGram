import { useState } from "react";
import styles from "./PostMedia.module.css";

export default function PostMedia({ media }) {
    const [index, setIndex] = useState(0);
    if (!media?.length) return null;

    return (
        <div className={styles.wrapper}>
            <img src={media[index].url} alt="" className={styles.img} />
            {media.length > 1 && (
                <>
                    <div className={styles.dots}>
                        {media.map((_, i) => (
                            <button
                                key={i}
                                className={`${styles.dot} ${i === index ? styles.active : ""}`}
                                onClick={() => setIndex(i)}
                            />
                        ))}
                    </div>
                    {index > 0 && (
                        <button className={`${styles.arrow} ${styles.prev}`} onClick={() => setIndex(index - 1)}>‹</button>
                    )}
                    {index < media.length - 1 && (
                        <button className={`${styles.arrow} ${styles.next}`} onClick={() => setIndex(index + 1)}>›</button>
                    )}
                </>
            )}
        </div>
    );
}