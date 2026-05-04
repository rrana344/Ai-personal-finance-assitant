export default function Button({ children, className = "", variant = "primary", ...props }) {
  const styles = {
    primary: "bg-ink text-white hover:bg-slate-800 dark:bg-white dark:text-ink",
    accent: "bg-mint text-ink hover:bg-emerald-300",
    ghost: "bg-white/70 text-ink hover:bg-white dark:bg-white/10 dark:text-white"
  };
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition ${styles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
