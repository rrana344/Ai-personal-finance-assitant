import { ArrowRight, BarChart3, Bot, Camera, Check, Flag, LineChart, PiggyBank, ReceiptText, ShieldCheck, Sparkles, WalletCards } from "lucide-react";
import { Link } from "react-router-dom";
import Button from "../components/Button";
import Navbar from "../components/Navbar";

const features = [
  ["Expense Tracking", ReceiptText, "Log income and expenses with searchable categories and payment methods."],
  ["AI Chatbot", Bot, "Ask natural language questions about spending, savings, and forecasts."],
  ["Budget Planner", WalletCards, "Set monthly limits and spot overspending before it snowballs."],
  ["Expense Prediction", LineChart, "Forecast next-month expenses with lightweight ML models."],
  ["OCR Receipt Scanner", Camera, "Upload bills and extract draft transaction details."],
  ["Smart Analytics", BarChart3, "See category, monthly, and savings trends in one dashboard."],
  ["Goal Tracking", Flag, "Track emergency funds, gadgets, vacations, and big purchases."],
  ["Financial Reports", ShieldCheck, "Export clean CSV reports and prepare monthly reviews."]
];

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 text-ink dark:bg-slate-950 dark:text-white">
      <Navbar />
      <section className="fin-grid relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(49,196,141,0.24),transparent_32%),radial-gradient(circle_at_85%_10%,rgba(249,115,91,0.18),transparent_28%)]" />
        <div className="relative mx-auto grid max-w-7xl gap-10 px-4 py-20 lg:grid-cols-[1.05fr_0.95fr] lg:py-28">
          <div className="max-w-3xl">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-white/80 px-3 py-2 text-sm font-bold shadow-sm dark:bg-white/10">
              <Sparkles size={16} className="text-coral" /> AI-powered personal finance
            </div>
            <h1 className="text-4xl font-black leading-tight md:text-6xl">Take Control of Your Financial Future with AI</h1>
            <p className="mt-6 max-w-2xl text-lg text-slate-600 dark:text-slate-300">
              Track spending, build budgets, forecast expenses, scan receipts, and get personal finance insights from a smart assistant built for everyday money decisions.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link to="/app"><Button className="px-6 py-3">Open Dashboard <ArrowRight size={18} /></Button></Link>
              <Link to="/app/transactions"><Button variant="ghost" className="px-6 py-3">Start Tracking</Button></Link>
              <Link to="/app/chat"><Button variant="accent" className="px-6 py-3">Try AI Assistant</Button></Link>
              <a href="#features"><Button variant="ghost" className="px-6 py-3">Explore Features</Button></a>
            </div>
          </div>
          <div className="relative min-h-[420px]">
            <div className="glass float-card absolute left-0 top-4 w-72 rounded-lg p-5 shadow-glow">
              <p className="text-sm font-semibold text-slate-500 dark:text-slate-300">Monthly savings</p>
              <p className="mt-2 text-4xl font-black">Rs.42,800</p>
              <div className="mt-5 h-2 rounded-full bg-slate-200"><div className="h-2 w-4/5 rounded-full bg-mint" /></div>
            </div>
            <div className="glass float-card absolute right-0 top-28 w-72 rounded-lg p-5 shadow-glow [animation-delay:1.4s]">
              <p className="text-sm font-semibold">AI insight</p>
              <p className="mt-3 text-slate-600 dark:text-slate-300">Food spend is 18% above your normal trend. Set a weekly cap of Rs.3,000.</p>
            </div>
            <div className="glass float-card absolute bottom-4 left-10 right-8 rounded-lg p-5 shadow-glow [animation-delay:2.3s]">
              <div className="flex items-center justify-between">
                <span className="font-bold">Financial Health</span>
                <span className="text-2xl font-black text-mint">86</span>
              </div>
              <div className="mt-4 grid grid-cols-8 items-end gap-2">
                {[42, 70, 52, 80, 64, 92, 76, 88].map((height, index) => (
                  <span key={index} className="rounded-t bg-aqua" style={{ height }} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="mx-auto max-w-7xl px-4 py-16">
        <div className="mb-6 rounded-lg border border-mint/30 bg-mint/15 px-4 py-3 text-sm font-bold text-emerald-800 dark:text-mint">
          Demo Mode Enabled - No Login Required
        </div>
        <div className="mb-9 max-w-2xl">
          <h2 className="text-3xl font-black">Everything your money needs in one workspace</h2>
          <p className="mt-3 text-slate-600 dark:text-slate-300">Production-ready modules for a modern finance management platform.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {features.map(([title, Icon, text]) => (
            <div key={title} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-lg dark:border-white/10 dark:bg-slate-900">
              <Icon className="mb-4 text-aqua" />
              <h3 className="font-black">{title}</h3>
              <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{text}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-ink py-14 text-white dark:bg-slate-900">
        <div className="mx-auto grid max-w-7xl gap-4 px-4 md:grid-cols-4">
          {["25K Users Managed", "Rs.18Cr Money Tracked", "91% AI Accuracy", "Rs.2.4Cr Savings Generated"].map((metric) => (
            <div key={metric} className="rounded-lg bg-white/10 p-5 text-center">
              <p className="text-3xl font-black">{metric.split(" ")[0]}</p>
              <p className="mt-1 text-sm text-slate-300">{metric.substring(metric.indexOf(" ") + 1)}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="about" className="mx-auto max-w-7xl px-4 py-16">
        <h2 className="text-3xl font-black">How it works</h2>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {["Add Transactions", "AI Analyzes Data", "Get Insights & Predictions"].map((step, index) => (
            <div key={step} className="rounded-lg border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-slate-900">
              <span className="grid h-10 w-10 place-items-center rounded-lg bg-gold font-black text-ink">{index + 1}</span>
              <h3 className="mt-5 text-xl font-black">{step}</h3>
              <p className="mt-2 text-slate-600 dark:text-slate-300">Connect daily money activity to practical next steps without spreadsheet fatigue.</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16">
        <h2 className="text-3xl font-black">Loved by focused money managers</h2>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {["It caught subscriptions I forgot about.", "The AI advice feels practical, not generic.", "Budget alerts helped me stay under plan."].map((review, index) => (
            <div key={review} className="rounded-lg border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-slate-900">
              <div className="mb-4 h-12 w-12 rounded-full bg-gradient-to-br from-mint to-aqua" />
              <p className="font-semibold">"{review}"</p>
              <p className="mt-3 text-gold">5/5 stars</p>
              <p className="text-sm text-slate-500">User {index + 1}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="pricing" className="mx-auto max-w-7xl px-4 py-16">
        <h2 className="text-3xl font-black">Pricing</h2>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[
            ["Free", "Rs.0", ["Transactions", "Basic dashboard", "CSV export"]],
            ["Pro", "Rs.499", ["AI chat", "Predictions", "OCR receipts"]],
            ["Enterprise", "Custom", ["Admin panel", "Usage monitoring", "Priority support"]]
          ].map(([plan, price, items]) => (
            <div key={plan} className="rounded-lg border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-slate-900">
              <h3 className="text-xl font-black">{plan}</h3>
              <p className="mt-4 text-3xl font-black">{price}</p>
              <div className="mt-5 grid gap-3">
                {items.map((item) => <p key={item} className="flex items-center gap-2 text-sm"><Check size={16} className="text-mint" /> {item}</p>)}
              </div>
              <Button className="mt-6 w-full" variant={plan === "Pro" ? "accent" : "primary"}>Choose Plan</Button>
            </div>
          ))}
        </div>
      </section>

      <footer id="contact" className="border-t border-slate-200 bg-white py-10 dark:border-white/10 dark:bg-slate-900">
        <div className="mx-auto grid max-w-7xl gap-6 px-4 md:grid-cols-4">
          <div>
            <h3 className="font-black">FinMate AI</h3>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Modern personal finance intelligence.</p>
          </div>
          <p className="text-sm">Quick links<br />Features / Pricing / Dashboard</p>
          <p className="text-sm">Contact<br />hello@finmate.ai</p>
          <form className="flex gap-2">
            <input className="min-w-0 flex-1 rounded-lg border px-3 py-2 dark:border-white/10 dark:bg-slate-950" placeholder="Email" />
            <Button>Join</Button>
          </form>
        </div>
      </footer>
    </div>
  );
}
