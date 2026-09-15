// frontend/src/components/layout/Navbar.jsx
import { Link, useNavigate } from "react-router-dom";
import { useMe, useLogout } from "@/hooks/useAuth";
import { useUiStore } from "@/store/uiStore";
import Avatar from "@/components/common/Avatar";
import styles from "./Navbar.module.css";

export default function Navbar() {
    const { data: me } = useMe();
    const logout = useLogout();
    const navigate = useNavigate();
    const openUploadModal = useUiStore((s) => s.openUploadModal);

    return (
        <header className={styles.navbar}>
            <Link to="/" className={styles.logo}>AuraGram</Link>

            <nav className={styles.actions}>
                <button className={styles.uploadBtn} onClick={openUploadModal} title="New post">＋</button>
                <Link to="/notifications" className={styles.iconBtn} title="Notifications">🔔</Link>
                {me && (
                    <Link to={`/${me.username}`} className={styles.profile}>
                        <Avatar src={me.avatar_url} username={me.username} size="sm" />
                    </Link>
                )}
                <button className={styles.iconBtn} onClick={() => logout.mutate()} title="Logout">
                    ↩
                </button>
            </nav>
        </header>
    );
}