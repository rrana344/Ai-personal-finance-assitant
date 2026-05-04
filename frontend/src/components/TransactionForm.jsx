import { useState } from "react";
import Button from "./Button";

const categories = ["Food", "Shopping", "Rent", "Bills", "Education", "Health", "Travel", "Entertainment"];

export default function TransactionForm({ onSubmit }) {
  const [form, setForm] = useState({
    amount: "",
    category: "Food",
    type: "expense",
    date: new Date().toISOString().slice(0, 10),
    notes: "",
    payment_method: "Card"
  });

  const update = (key, value) => setForm((current) => ({ ...current, [key]: value }));

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit({ ...form, amount: Number(form.amount) });
      }}
      className="grid gap-3 rounded-lg border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900 md:grid-cols-3"
    >
      <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" type="number" min="1" placeholder="Amount" value={form.amount} onChange={(event) => update("amount", event.target.value)} required />
      <select className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" value={form.category} onChange={(event) => update("category", event.target.value)}>
        {categories.map((category) => <option key={category}>{category}</option>)}
      </select>
      <select className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" value={form.type} onChange={(event) => update("type", event.target.value)}>
        <option value="expense">Expense</option>
        <option value="income">Income</option>
      </select>
      <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" type="date" value={form.date} onChange={(event) => update("date", event.target.value)} />
      <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" placeholder="Payment method" value={form.payment_method} onChange={(event) => update("payment_method", event.target.value)} />
      <input className="rounded-lg border p-2 dark:border-white/10 dark:bg-slate-950" placeholder="Notes" value={form.notes} onChange={(event) => update("notes", event.target.value)} />
      <Button className="md:col-span-3" type="submit">Add Transaction</Button>
    </form>
  );
}
