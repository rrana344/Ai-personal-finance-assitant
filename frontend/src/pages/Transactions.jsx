import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import api from "../services/api";
import TransactionForm from "../components/TransactionForm";

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [search, setSearch] = useState("");

  const load = () => api.get("/transactions", { params: { search } }).then((res) => setTransactions(res.data));

  useEffect(() => { load(); }, []);

  const add = async (payload) => {
    await api.post("/transactions", payload);
    load();
  };

  const remove = async (id) => {
    await api.delete(`/transactions/${id}`);
    load();
  };

  return (
    <div className="grid gap-6">
      <TransactionForm onSubmit={add} />
      <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-slate-900">
        <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <h2 className="text-xl font-black">Transactions</h2>
          <div className="flex gap-2">
            <input className="rounded-lg border px-3 py-2 dark:border-white/10 dark:bg-slate-950" placeholder="Search notes" value={search} onChange={(event) => setSearch(event.target.value)} />
            <button onClick={load} className="rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white dark:bg-white dark:text-ink">Filter</button>
          </div>
        </div>
        <div className="overflow-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-slate-500"><tr><th className="py-2">Date</th><th>Category</th><th>Amount</th><th>Type</th><th>Method</th><th></th></tr></thead>
            <tbody>
              {transactions.map((txn) => (
                <tr key={txn.id} className="border-t border-slate-100 dark:border-white/10">
                  <td className="py-3">{txn.date}</td><td>{txn.category}</td><td>Rs.{txn.amount}</td><td>{txn.type}</td><td>{txn.payment_method}</td>
                  <td><button aria-label="Delete transaction" onClick={() => remove(txn.id)} className="rounded-lg p-2 hover:bg-red-50 hover:text-red-600"><Trash2 size={17} /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
