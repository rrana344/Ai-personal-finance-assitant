from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest, RandomForestRegressor

from app import models

ARTIFACT_PATH = Path(__file__).resolve().parents[1] / "ml_artifacts" / "finance_models.joblib"


def predict_next_month(transactions: list[models.Transaction]) -> dict:
    expenses = [t for t in transactions if t.type == "expense"]
    if not expenses:
        return {
            "predicted_expense": 0,
            "confidence": "low",
            "series": [],
            "future_savings_forecast": 0,
            "budget_forecast": [],
            "anomalies": [],
            "overspending_risk": "low",
            "trained_dataset_prediction": _predict_with_trained_dataset_model(transactions),
            "model_metrics": trained_model_metrics(),
        }

    rows = [{"month": t.date.strftime("%Y-%m"), "amount": t.amount} for t in expenses]
    df = pd.DataFrame(rows).groupby("month", as_index=False).sum().sort_values("month")
    df["index"] = range(len(df))
    income_by_month = pd.DataFrame(
        [{"month": t.date.strftime("%Y-%m"), "amount": t.amount} for t in transactions if t.type == "income"]
    )
    monthly_income = income_by_month.groupby("month", as_index=False).sum() if not income_by_month.empty else pd.DataFrame(columns=["month", "amount"])

    if len(df) < 3:
        predicted = round(float(df["amount"].mean()), 2)
        return {
            "predicted_expense": predicted,
            "confidence": "low",
            "series": df.rename(columns={"amount": "expense"}).to_dict("records"),
            "future_savings_forecast": _forecast_savings(monthly_income, predicted),
            "budget_forecast": _budget_forecast(expenses),
            "anomalies": _detect_anomalies(expenses),
            "overspending_risk": _overspending_risk(predicted, monthly_income),
            "trained_dataset_prediction": _predict_with_trained_dataset_model(transactions),
            "model_metrics": trained_model_metrics(),
        }

    linear = LinearRegression()
    forest = RandomForestRegressor(n_estimators=80, random_state=42)
    linear.fit(df[["index"]], df["amount"])
    forest.fit(df[["index"]], df["amount"])
    next_frame = pd.DataFrame({"index": [len(df)]})
    next_value = (linear.predict(next_frame)[0] + forest.predict(next_frame)[0]) / 2
    predicted = round(max(float(next_value), 0), 2)
    return {
        "predicted_expense": predicted,
        "confidence": "high" if len(df) >= 6 else "medium",
        "series": df.rename(columns={"amount": "expense"}).to_dict("records"),
        "future_savings_forecast": _forecast_savings(monthly_income, predicted),
        "budget_forecast": _budget_forecast(expenses),
        "anomalies": _detect_anomalies(expenses),
        "overspending_risk": _overspending_risk(predicted, monthly_income),
        "trained_dataset_prediction": _predict_with_trained_dataset_model(transactions),
        "model_metrics": trained_model_metrics(),
    }


def trained_model_metrics() -> dict | None:
    bundle = _load_bundle()
    return bundle.get("metrics") if bundle else None


def _predict_with_trained_dataset_model(transactions: list[models.Transaction]) -> dict | None:
    bundle = _load_bundle()
    if not bundle:
        return None
    row = _profile_from_transactions(transactions)
    frame = pd.DataFrame([row])
    predictions = {}
    for name, model in bundle["models"].items():
        try:
            if hasattr(model, "set_params"):
                model.set_params(**{"randomforestregressor__n_jobs": 1})
            value = model.predict(frame)[0]
        except Exception:
            continue
        if hasattr(value, "item"):
            value = value.item()
        predictions[name] = round(float(value), 2) if isinstance(value, (float, int)) else str(value)
    return predictions or None


def _load_bundle() -> dict | None:
    if not ARTIFACT_PATH.exists():
        return None
    return joblib.load(ARTIFACT_PATH)


def _forecast_savings(monthly_income: pd.DataFrame, predicted_expense: float) -> float:
    if monthly_income.empty:
        return round(max(predicted_expense * 0.2, 0), 2)
    expected_income = float(monthly_income["amount"].tail(3).mean())
    return round(expected_income - predicted_expense, 2)


def _budget_forecast(expenses: list[models.Transaction]) -> list[dict]:
    category_totals: dict[str, list[float]] = {}
    for txn in expenses:
        category_totals.setdefault(txn.category, []).append(txn.amount)
    return [
        {
            "category": category,
            "forecast": round(sum(values) / max(len(values), 1), 2),
            "risk": "high" if sum(values) / max(len(values), 1) > 5000 else "normal",
        }
        for category, values in sorted(category_totals.items())
    ]


def _detect_anomalies(expenses: list[models.Transaction]) -> list[dict]:
    if len(expenses) < 5:
        threshold = sum(t.amount for t in expenses) / max(len(expenses), 1) * 1.8
        return [_anomaly_row(txn, "rule") for txn in expenses if txn.amount > threshold]
    frame = pd.DataFrame({"amount": [txn.amount for txn in expenses]})
    model = IsolationForest(contamination=0.15, random_state=42)
    flags = model.fit_predict(frame)
    return [_anomaly_row(txn, "isolation_forest") for txn, flag in zip(expenses, flags) if flag == -1]


def _anomaly_row(txn: models.Transaction, model: str) -> dict:
    return {"id": txn.id, "date": str(txn.date), "category": txn.category, "amount": round(txn.amount, 2), "model": model}


def _overspending_risk(predicted_expense: float, monthly_income: pd.DataFrame) -> str:
    if monthly_income.empty:
        return "medium"
    expected_income = float(monthly_income["amount"].tail(3).mean())
    ratio = predicted_expense / expected_income if expected_income else 1
    return "high" if ratio > 0.85 else "medium" if ratio > 0.65 else "low"


def _profile_from_transactions(transactions: list[models.Transaction]) -> dict:
    income = sum(t.amount for t in transactions if t.type == "income")
    expense = sum(t.amount for t in transactions if t.type == "expense")
    top_category = "Groceries"
    expense_categories = {}
    for txn in transactions:
        if txn.type == "expense":
            expense_categories[txn.category] = expense_categories.get(txn.category, 0) + txn.amount
    if expense_categories:
        top_category = max(expense_categories.items(), key=lambda item: item[1])[0]

    monthly_income = income or max(expense * 1.25, 3000)
    savings = max(monthly_income - expense, 0)
    savings_rate = savings / monthly_income if monthly_income else 0
    return {
        "monthly_income": monthly_income,
        "savings_rate": savings_rate,
        "budget_goal": max(expense * 0.9, 1000),
        "financial_scenario": "normal",
        "credit_score": 720,
        "debt_to_income_ratio": 0.28,
        "loan_payment": 250,
        "investment_amount": max(savings * 0.25, 0),
        "subscription_services": 4,
        "emergency_fund": max(savings * 2, 500),
        "transaction_count": len(transactions) or 12,
        "fraud_flag": 0,
        "discretionary_spending": expense * 0.35,
        "essential_spending": expense * 0.65,
        "income_type": "Salary",
        "rent_or_mortgage": min(monthly_income * 0.32, 1800),
        "category": top_category,
        "cash_flow_status": "Positive" if monthly_income >= expense else "Negative",
    }
