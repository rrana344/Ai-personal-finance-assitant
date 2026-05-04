import { BarChart3, Bot, Flag, Gauge, LayoutDashboard, Moon, ReceiptText, Shield, Sun, WalletCards } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";
import { useEffect, useState } from "react";

const nav = [
  ["Dashboard", "/", LayoutDashboard],
  ["Transactions", "/app/transactions", ReceiptText],
  ["Budgets", "/app/budgets", WalletCards],
  ["Goals", "/app/goals", Flag],
  ["AI Chat", "/app/chat", Bot],
  ["Reports", "/app/reports", BarChart3],
  ["Admin", "/app/admin", Shield]
];

export default function AppLayout() {
  const [dark, setDark] = useState(() => localStorage.getItem("theme") === "dark");

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 dark:text-white">
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 border-r border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900 lg:block">
        <div className="mb-8 flex items-center gap-2 text-xl font-black">
          <Gauge className="text-aqua" /> FinMate AI
        </div>
        <nav className="grid gap-2">
          {nav.map(([label, href, Icon]) => (
            <NavLink
              key={href}
              to={href}
              end={href === "/" || href === "/app"}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-semibold ${
                  isActive ? "bg-ink text-white dark:bg-mint dark:text-ink" : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-white/10"
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="absolute bottom-4 left-4 right-4 rounded-lg bg-mint/15 px-3 py-3 text-sm font-semibold text-emerald-800 dark:text-mint">
          Demo Mode Enabled - No Login Required
        </div>
      </aside>
      <main className="lg:pl-64">
        <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/85 px-4 py-3 backdrop-blur dark:border-white/10 dark:bg-slate-950/85 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500 dark:text-slate-400">Demo Mode Enabled - No Login Required</p>
              <h1 className="text-xl font-black">AI Finance Command Center</h1>
            </div>
            <button
              type="button"
              onClick={() => setDark((value) => !value)}
              className="grid h-10 w-10 place-items-center rounded-lg border border-slate-200 bg-white text-slate-700 shadow-sm dark:border-white/10 dark:bg-slate-900 dark:text-white"
              aria-label="Toggle color mode"
              title="Toggle color mode"
            >
              {dark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </header>
        <div className="p-4 lg:p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
