import { useEffect, useState } from "react";
import api from "../services/api";
import Button from "../components/Button";

export default function Goals() {
  const [goals, setGoals] = useState([]);
  const [form, setForm] = useState({ title: "", target_amount: "", current_amount: "", deadline: "" });
  const load = () => api.get("/goals").then((res) => setGoals(res.data));
  useEffect(() => { load(); }, []);

  const submit = async (event) => {
    event.preventDefault();
    await api.post("/goals", { ...form, target_amount: Number(form.target_amount), current_amount: Number(form.current_amount || 0), deadline: form.deadline || null });
    setForm({ title: "", target_amount: "", current_amount: "", deadline: "" });
    load();
  };

  return (
    <div className="grid gap-6">
      <form onSubmit={submit} className="grid gap-3 rounded-lg border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900 md:grid-cols-5">
        <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" placeholder="Goal title" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} required />
        <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" type="number" placeholder="Target" value={form.target_amount} onChange={(event) => setForm({ ...form, target_amount: event.target.value })} required />
        <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" type="number" placeholder="Saved" value={form.current_amount} onChange={(event) => setForm({ ...form, current_amount: event.target.value })} />
        <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" type="date" value={form.deadline} onChange={(event) => setForm({ ...form, deadline: event.target.value })} />
        <Button type="submit">Create Goal</Button>
      </form>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {goals.map((goal) => (
          <div key={goal.id} className="rounded-lg border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-slate-900">
            <h3 className="font-black">{goal.title}</h3>
            <div className="my-5 grid aspect-square max-h-40 place-items-center rounded-full border-[12px] border-mint text-3xl font-black">{goal.progress_percent}%</div>
            <p className="text-sm text-slate-500">Rs.{goal.current_amount} saved of Rs.{goal.target_amount}</p>
            <p className="text-sm text-slate-500">Deadline: {goal.deadline || "Flexible"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
