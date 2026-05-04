import { useEffect, useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { AlertTriangle, CreditCard, IndianRupee, PiggyBank, TrendingUp, Wallet } from "lucide-react";
import api from "../services/api";
import StatCard from "../components/StatCard";

const colors = ["#19a7ce", "#31c48d", "#f9735b", "#f5b841", "#7c3aed", "#ef4444", "#0f766e"];
const currency = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    let active = true;
    Promise.all([api.get("/analytics"), api.get("/predictions")])
      .then(([analytics, predictions]) => {
        if (!active) return;
        setData(analytics.data);
        setPrediction(predictions.data);
        setStatus("ready");
      })
      .catch(() => active && setStatus("error"));
    return () => {
      active = false;
    };
  }, []);

  const summary = data?.summary || {};
  const health = data?.health_score || {};
  const insightPreview = useMemo(() => (data?.insights || []).slice(0, 4), [data]);

  if (status === "loading") return <DashboardSkeleton />;
  if (status === "error") {
    return (
      <Panel title="Could not load finance dashboard">
        <p className="text-sm text-slate-500 dark:text-slate-400">Start the FastAPI backend on port 8001 and refresh the page.</p>
      </Panel>
    );
  }

  return (
    <div className="grid gap-6">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Total Balance" value={currency.format(summary.total_balance || 0)} icon={Wallet} tone="bg-aqua/15 text-aqua" />
        <StatCard title="Monthly Income" value={currency.format(summary.monthly_income || 0)} icon={IndianRupee} tone="bg-mint/15 text-emerald-600" />
        <StatCard title="Monthly Expenses" value={currency.format(summary.monthly_expenses || 0)} icon={CreditCard} tone="bg-coral/15 text-coral" />
        <StatCard title="Savings Ratio" value={`${summary.savings_ratio || 0}%`} icon={PiggyBank} tone="bg-gold/20 text-amber-700" />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
        <Panel title="Income, Expense, Savings Trend">
          <ResponsiveContainer width="100%" height={320}>
            <AreaChart data={data?.monthly_trend || []}>
              <defs>
                <linearGradient id="income" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="5%" stopColor="#31c48d" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#31c48d" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="expense" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="5%" stopColor="#f9735b" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#f9735b" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => currency.format(value)} />
              <Area type="monotone" dataKey="income" stroke="#31c48d" fill="url(#income)" strokeWidth={3} />
              <Area type="monotone" dataKey="expense" stroke="#f9735b" fill="url(#expense)" strokeWidth={3} />
              <Line type="monotone" dataKey="savings" stroke="#19a7ce" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title={`Financial Health: ${health.score || 0}/100`}>
          <div className="grid place-items-center gap-4">
            <div className="relative grid h-44 w-44 place-items-center rounded-full bg-slate-100 dark:bg-slate-950">
              <div className="absolute inset-3 rounded-full border-[14px] border-mint" style={{ clipPath: `inset(${100 - (health.score || 0)}% 0 0 0)` }} />
              <div className="text-center">
                <p className="text-5xl font-black">{health.score || 0}</p>
                <p className="text-sm font-semibold text-slate-500">{health.label || "Ready"}</p>
              </div>
            </div>
            <div className="grid w-full grid-cols-2 gap-3 text-sm">
              {Object.entries(health.factors || {}).map(([label, value]) => (
                <div key={label} className="rounded-lg bg-slate-50 p-3 dark:bg-slate-950">
                  <p className="capitalize text-slate-500">{label.replaceAll("_", " ")}</p>
                  <p className="font-black">{value}</p>
                </div>
              ))}
            </div>
          </div>
        </Panel>
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <Panel title="Category Analytics">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={data?.category_expenses || []} dataKey="value" nameKey="name" innerRadius={62} outerRadius={110} paddingAngle={2}>
                {(data?.category_expenses || []).map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}
              </Pie>
              <Tooltip formatter={(value) => currency.format(value)} />
            </PieChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="Budget Utilization">
          <div className="mb-4 flex items-center justify-between">
            <p className="text-sm text-slate-500">Overall utilization</p>
            <p className="text-2xl font-black">{summary.budget_utilization || 0}%</p>
          </div>
          <div className="grid gap-3">
            {(data?.budget_status || []).map((budget) => (
              <div key={budget.id}>
                <div className="mb-1 flex justify-between text-sm">
                  <span className="font-semibold">{budget.category}</span>
                  <span>{currency.format(budget.spent)} / {currency.format(budget.limit_amount)}</span>
                </div>
                <div className="h-3 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
                  <div className={budget.status === "exceeded" ? "h-full bg-coral" : budget.status === "watch" ? "h-full bg-gold" : "h-full bg-mint"} style={{ width: `${Math.min(budget.usage_percent, 100)}%` }} />
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </section>

      <section className="grid gap-6 xl:grid-cols-3">
        <Panel title="AI Insights">
          <div className="grid gap-3">
            {insightPreview.map((insight) => (
              <div key={insight.title} className="rounded-lg border border-slate-100 p-3 dark:border-white/10">
                <p className="font-black">{insight.title}</p>
                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{insight.message}</p>
              </div>
            ))}
          </div>
        </Panel>
        <Panel title="ML Predictions">
          <div className="grid gap-4">
            <Metric label="Predicted next month expense" value={currency.format(prediction?.predicted_expense || 0)} />
            <Metric label="Future savings forecast" value={currency.format(prediction?.future_savings_forecast || 0)} />
            <Metric label="Overspending risk" value={prediction?.overspending_risk || "low"} />
          </div>
        </Panel>
        <Panel title="Smart Alerts">
          <div className="grid gap-3">
            {(data?.alerts || []).map((alert) => (
              <div key={`${alert.title}-${alert.message}`} className="flex gap-3 rounded-lg bg-slate-50 p-3 text-sm dark:bg-slate-950">
                <AlertTriangle size={18} className={alert.level === "critical" ? "text-coral" : "text-gold"} />
                <div>
                  <p className="font-bold">{alert.title}</p>
                  <p className="text-slate-500 dark:text-slate-400">{alert.message}</p>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <Panel title="Income vs Expense">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data?.monthly_trend || []}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => currency.format(value)} />
              <Bar dataKey="income" fill="#31c48d" radius={[6, 6, 0, 0]} />
              <Bar dataKey="expense" fill="#f9735b" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Panel>
        <Panel title="Recent Transactions">
          <div className="overflow-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-slate-500"><tr><th className="py-2">Date</th><th>Category</th><th>Amount</th><th>Type</th><th>Status</th></tr></thead>
              <tbody>
                {(data?.recent_transactions || []).map((txn) => (
                  <tr key={txn.id} className="border-t border-slate-100 dark:border-white/10">
                    <td className="py-3">{txn.date}</td><td>{txn.category}</td><td>{currency.format(txn.amount)}</td><td className="capitalize">{txn.type}</td><td>{txn.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      </section>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-lg bg-slate-50 p-4 dark:bg-slate-950">
      <p className="text-sm text-slate-500 dark:text-slate-400">{label}</p>
      <p className="mt-1 flex items-center gap-2 text-2xl font-black capitalize"><TrendingUp size={18} className="text-mint" /> {value}</p>
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="grid gap-6">
      <div className="grid gap-4 md:grid-cols-4">
        {[1, 2, 3, 4].map((item) => <div key={item} className="h-32 animate-pulse rounded-lg bg-slate-200 dark:bg-slate-900" />)}
      </div>
      <div className="h-96 animate-pulse rounded-lg bg-slate-200 dark:bg-slate-900" />
    </div>
  );
}

export function Panel({ title, children }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm dark:border-white/10 dark:bg-slate-900">
      <h2 className="mb-4 text-lg font-black">{title}</h2>
      {children}
    </section>
  );
}
