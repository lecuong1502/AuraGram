import { NavLink } from "react-router-dom";
import { useMe } from "@/hooks/useAuth";
import Avatar from "@/components/common/Avatar";
import styles from "./Sidebar.module.css";


export default function Sidebar() {
    const { data: me } = useMe();
    if (!me) return null;

    return (
        <aside className={styles.sidebar}>
            <NavLink to="/" className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ""}`}>
                🏠 <span>Home</span>
            </NavLink>
            <NavLink to="/explore" className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ""}`}>
                🔍 <span>Explore</span>
            </NavLink>
            <NavLink to="/notifications" className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ""}`}>
                🔔 <span>Notifications</span>
            </NavLink>
            <NavLink to={`/${me.username}`} className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ""}`}>
                <Avatar src={me.avatar_url} username={me.username} size="sm" />
                <span>Profile</span>
            </NavLink>
        </aside>
    );
}