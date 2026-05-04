import { useEffect, useState } from "react";
import { Download, Upload } from "lucide-react";
import api from "../services/api";
import Button from "../components/Button";
import { Panel } from "./Dashboard";

export default function Reports() {
  const [prediction, setPrediction] = useState(null);
  const [receipt, setReceipt] = useState(null);

  useEffect(() => {
    api.get("/predictions").then((res) => setPrediction(res.data));
  }, []);

  const upload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    const { data } = await api.post("/uploads/receipt", formData);
    setReceipt(data);
  };

  const downloadReport = async (format) => {
    const response = await api.get(`/reports/monthly.${format}`, { responseType: "blob" });
    const url = URL.createObjectURL(response.data);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `finmate-report.${format === "xlsx" ? "xls" : format}`;
    anchor.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Panel title="Report Generation">
        <p className="mb-4 text-sm text-slate-500">Export your transaction history for monthly, yearly, and category reviews.</p>
        <div className="flex flex-wrap gap-3">
          <Button onClick={() => downloadReport("csv")}><Download size={18} /> CSV</Button>
          <Button onClick={() => downloadReport("xlsx")} variant="accent"><Download size={18} /> Excel</Button>
          <Button onClick={() => downloadReport("pdf")} variant="ghost"><Download size={18} /> PDF</Button>
        </div>
      </Panel>
      <Panel title="Expense Prediction">
        <p className="text-4xl font-black">Rs.{prediction?.predicted_expense || 0}</p>
        <p className="mt-2 text-sm text-slate-500">Predicted next-month spending / confidence {prediction?.confidence || "low"}</p>
        <div className="mt-4 grid gap-2 rounded-lg bg-slate-50 p-4 text-sm dark:bg-slate-950">
          <p>Future savings forecast: Rs.{prediction?.future_savings_forecast || 0}</p>
          <p>Overspending risk: {prediction?.overspending_risk || "low"}</p>
          <p>Anomalies detected: {prediction?.anomalies?.length || 0}</p>
        </div>
        {prediction?.trained_dataset_prediction && (
          <div className="mt-4 grid gap-2 rounded-lg bg-slate-50 p-4 text-sm dark:bg-slate-950">
            <p className="font-bold">Dataset-trained model output</p>
            <p>Monthly expense: Rs.{prediction.trained_dataset_prediction.monthly_expense_total}</p>
            <p>Actual savings: Rs.{prediction.trained_dataset_prediction.actual_savings}</p>
            <p>Advice score: {prediction.trained_dataset_prediction.financial_advice_score}</p>
            <p>Stress level: {prediction.trained_dataset_prediction.financial_stress_level}</p>
            <p>Savings goal met: {String(prediction.trained_dataset_prediction.savings_goal_met)}</p>
          </div>
        )}
      </Panel>
      <Panel title="OCR Receipt Scanner">
        <label className="inline-flex cursor-pointer items-center gap-2 rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white dark:bg-white dark:text-ink">
          <Upload size={18} /> Upload Receipt
          <input type="file" accept="image/*,.pdf" onChange={upload} className="hidden" />
        </label>
        {receipt && (
          <div className="mt-4 rounded-lg bg-slate-50 p-4 text-sm dark:bg-slate-950">
            <p>Detected amount: Rs.{receipt.amount || "Needs review"}</p>
            <p>Detected category: {receipt.category}</p>
            {receipt.transaction && <p>Transaction created: #{receipt.transaction.id} ({receipt.transaction.status})</p>}
          </div>
        )}
      </Panel>
      <Panel title="Recommendations">
        <p className="text-sm text-slate-500">PDF, CSV, Excel, OCR, anomaly detection, and forecast outputs are generated from backend service boundaries.</p>
      </Panel>
    </div>
  );
}
