// frontend/src/pages/Auth/LoginPage.jsx
import { useState } from "react";
import { Link } from "react-router-dom";
import { useLogin } from "@/hooks/useAuth";
import Input from "@/components/common/Input";
import Button from "@/components/common/Button";
import styles from "./Auth.module.css";

export default function LoginPage() {
    const login = useLogin();
    const [form, setForm] = useState({ email: "", password: "" });
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            await login.mutateAsync(form);
        } catch (err) {
            setError(err.response?.data?.detail ?? "Login failed");
        }
    };

    return (
        <div className={styles.page}>
            <div className={styles.card}>
                <h1 className={styles.logo}>AuraGram</h1>
                <p className={styles.subtitle}>Sign in to see photos from your friends.</p>

                <form onSubmit={handleSubmit} className={styles.form}>
                    <Input
                        label="Email"
                        type="email"
                        placeholder="email@example.com"
                        value={form.email}
                        onChange={(e) => setForm({ ...form, email: e.target.value })}
                        required
                    />
                    <Input
                        label="Password"
                        type="password"
                        placeholder="Password"
                        value={form.password}
                        onChange={(e) => setForm({ ...form, password: e.target.value })}
                        required
                    />
                    {error && <p className={styles.error}>{error}</p>}
                    <Button type="submit" fullWidth loading={login.isPending}>
                        Log in
                    </Button>
                </form>

                <p className={styles.footer}>
                    Don't have an account? <Link to="/register">Sign up</Link>
                </p>
            </div>
        </div>
    );
}