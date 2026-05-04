import { Menu, Moon, Sun, Wallet, X } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

const links = [
  ["Home", "/"],
  ["Dashboard", "/app"],
  ["Analytics", "/analytics"],
  ["AI Assistant", "/ai-assistant"],
  ["Budget Planner", "/budget-planner"],
  ["Reports", "/reports"],
  ["About", "/#about"],
  ["Contact", "/#contact"]
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const [dark, setDark] = useState(false);

  const toggleTheme = () => {
    document.documentElement.classList.toggle("dark");
    setDark((value) => !value);
  };

  return (
    <header className="sticky top-0 z-50 border-b border-white/30 bg-white/80 backdrop-blur-xl dark:border-white/10 dark:bg-slate-950/80">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2 text-lg font-black">
          <span className="grid h-9 w-9 place-items-center rounded-lg bg-ink text-white dark:bg-mint dark:text-ink">
            <Wallet size={20} />
          </span>
          FinMate AI
        </Link>
        <div className="hidden items-center gap-6 lg:flex">
          {links.map(([label, href]) => (
            <a key={label} href={href} className="text-sm font-medium text-slate-600 hover:text-ink dark:text-slate-300 dark:hover:text-white">
              {label}
            </a>
          ))}
        </div>
        <div className="hidden items-center gap-2 lg:flex">
          <button aria-label="Toggle theme" onClick={toggleTheme} className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-white/10">
            {dark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
        <button aria-label="Open menu" className="lg:hidden" onClick={() => setOpen(true)}>
          <Menu />
        </button>
      </nav>
      {open && (
        <div className="fixed inset-0 z-50 bg-white p-5 dark:bg-slate-950 lg:hidden">
          <div className="flex items-center justify-between">
            <span className="text-lg font-black">FinMate AI</span>
            <button aria-label="Close menu" onClick={() => setOpen(false)}>
              <X />
            </button>
          </div>
          <div className="mt-8 grid gap-4">
            {links.map(([label, href]) => (
              <a key={label} href={href} onClick={() => setOpen(false)} className="text-lg font-semibold">
                {label}
              </a>
            ))}
          </div>
        </div>
      )}
    </header>
  );
}
