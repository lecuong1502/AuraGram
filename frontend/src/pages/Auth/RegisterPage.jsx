// frontend/src/pages/Auth/RegisterPage.jsx
import { useState } from "react";
import { Link } from "react-router-dom";
import { useRegister } from "@/hooks/useAuth";
import Input from "@/components/common/Input";
import Button from "@/components/common/Button";
import { validateEmail, validateUsername, validatePassword } from "@/utils/validators";
import styles from "./Auth.module.css";

export default function RegisterPage() {
    const register = useRegister();
    const [form, setForm] = useState({ username: "", email: "", password: "", full_name: "" });
    const [errors, setErrors] = useState({});

    const validate = () => {
        const e = {};
        if (!validateUsername(form.username)) e.username = "3-30 chars: letters, numbers, . and _ only";
        if (!validateEmail(form.email)) e.email = "Invalid email address";
        if (!validatePassword(form.password)) e.password = "At least 8 characters";
        setErrors(e);
        return Object.keys(e).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validate()) return;
        try {
            await register.mutateAsync(form);
        } catch (err) {
            setErrors({ api: err.response?.data?.detail ?? "Registration failed" });
        }
    };

    const set = (field) => (e) => setForm({ ...form, [field]: e.target.value });

    return (
        <div className={styles.page}>
            <div className={styles.card}>
                <h1 className={styles.logo}>AuraGram</h1>
                <p className={styles.subtitle}>Sign up to see photos from your friends.</p>

                <form onSubmit={handleSubmit} className={styles.form}>
                    <Input label="Full name" placeholder="Your name" value={form.full_name} onChange={set("full_name")} />
                    <Input label="Username" placeholder="username" value={form.username} onChange={set("username")} error={errors.username} required />
                    <Input label="Email" type="email" placeholder="email@example.com" value={form.email} onChange={set("email")} error={errors.email} required />
                    <Input label="Password" type="password" placeholder="Password (min 8 chars)" value={form.password} onChange={set("password")} error={errors.password} required />
                    {errors.api && <p className={styles.error}>{errors.api}</p>}
                    <Button type="submit" fullWidth loading={register.isPending}>Create account</Button>
                </form>

                <p className={styles.footer}>
                    Already have an account? <Link to="/login">Log in</Link>
                </p>
            </div>
        </div>
    );
}