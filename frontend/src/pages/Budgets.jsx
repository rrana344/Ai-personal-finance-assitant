import { useEffect, useState } from "react";
import api from "../services/api";
import Button from "../components/Button";

export default function Budgets() {
  const [budgets, setBudgets] = useState([]);
  const [form, setForm] = useState({ category: "Food", month: new Date().toISOString().slice(0, 7), limit_amount: "" });
  const load = () => api.get("/budgets").then((res) => setBudgets(res.data));
  useEffect(() => { load(); }, []);

  const submit = async (event) => {
    event.preventDefault();
    await api.post("/budgets", { ...form, limit_amount: Number(form.limit_amount) });
    setForm({ ...form, limit_amount: "" });
    load();
  };

  return (
    <div className="grid gap-6">
      <form onSubmit={submit} className="grid gap-3 rounded-lg border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900 md:grid-cols-4">
        <select className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" value={form.category} onChange={(event) => setForm({ ...form, category: event.target.value })}>
          {["Food", "Shopping", "Rent", "Bills", "Education", "Health", "Travel", "Entertainment"].map((item) => <option key={item}>{item}</option>)}
        </select>
        <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" type="month" value={form.month} onChange={(event) => setForm({ ...form, month: event.target.value })} />
        <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" type="number" placeholder="Monthly limit" value={form.limit_amount} onChange={(event) => setForm({ ...form, limit_amount: event.target.value })} required />
        <Button type="submit">Set Budget</Button>
      </form>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {budgets.map((budget) => (
          <div key={budget.id} className="rounded-lg border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-slate-900">
            <div className="flex justify-between"><h3 className="font-black">{budget.category}</h3><span>{budget.month}</span></div>
            <p className="mt-3 text-sm text-slate-500">Rs.{budget.spent} of Rs.{budget.limit_amount}</p>
            <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
              <div className={`h-full ${budget.usage_percent > 100 ? "bg-coral" : "bg-mint"}`} style={{ width: `${Math.min(budget.usage_percent, 100)}%` }} />
            </div>
            <p className="mt-3 text-sm font-semibold">Remaining: Rs.{budget.remaining}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
