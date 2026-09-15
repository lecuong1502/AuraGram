import { useEffect } from "react";
import { useUiStore } from "@/store/uiStore";
import styles from "./Toast.module.css";

function ToastItem({ id, message, type }) {
    const removeToast = useUiStore((s) => s.removeToast);
    useEffect(() => {
        const t = setTimeout(() => removeToast(id), 3000);
        return () => clearTimeout(t);
    }, [id, removeToast]);

    return (
        <div className={`${styles.toast} ${styles[type]}`}>
            {message}
        </div>
    );
}

export default function ToastContainer() {
    const toasts = useUiStore((s) => s.toasts);
    return (
        <div className={styles.container}>
            {toasts.map((t) => <ToastItem key={t.id} {...t} />)}
        </div>
    );
}