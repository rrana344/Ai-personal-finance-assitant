import { useEffect, useState } from "react";
import api from "../services/api";
import { Panel } from "./Dashboard";

export default function Admin() {
  const [overview, setOverview] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/admin/overview").then((res) => setOverview(res.data)).catch(() => setError("Demo overview is unavailable right now."));
  }, []);

  if (error) return <Panel title="Admin Panel"><p className="text-coral">{error}</p></Panel>;

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {Object.entries(overview || {}).map(([key, value]) => (
        <div key={key} className="rounded-lg border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-slate-900">
          <p className="text-sm uppercase tracking-wide text-slate-500">{key.replace("_", " ")}</p>
          <p className="mt-3 text-2xl font-black">{value}</p>
        </div>
      ))}
    </div>
  );
}
