import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import ToastContainer from "@/components/common/Toast";
import styles from "./MainLayout.module.css";

export default function MainLayout() {
    return (
        <div className={styles.layout}>
            <Navbar />
            <div className={styles.body}>
                <Sidebar />
                <main className={styles.main}>
                    <Outlet />
                </main>
            </div>
            <ToastContainer />
        </div>
    );
}