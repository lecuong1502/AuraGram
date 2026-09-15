import styles from "./Button.module.css";
 
export default function Button({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  fullWidth = false,
  ...props
}) {
    return (
        <button
            className={[
                styles.btn,
                styles[variant],
                styles[size],
                fullWidth ? styles.fullWidth : "",
                loading ? styles.loading : "",
            ].join(" ")}
            disabled={loading || props.disabled}
            {...props}
        >
            {loading ? <span className={styles.spinner} /> : children}
        </button>
    )
}