from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "monthly_income",
    "savings_rate",
    "budget_goal",
    "credit_score",
    "debt_to_income_ratio",
    "loan_payment",
    "investment_amount",
    "subscription_services",
    "emergency_fund",
    "transaction_count",
    "fraud_flag",
    "discretionary_spending",
    "essential_spending",
    "rent_or_mortgage",
]

CATEGORICAL_FEATURES = [
    "financial_scenario",
    "income_type",
    "category",
    "cash_flow_status",
]

REGRESSION_TARGETS = [
    "monthly_expense_total",
    "actual_savings",
    "financial_advice_score",
]

CLASSIFICATION_TARGETS = [
    "financial_stress_level",
    "savings_goal_met",
]


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric, NUMERIC_FEATURES),
            ("cat", categorical, CATEGORICAL_FEATURES),
        ]
    )


def train(dataset_path: Path, output_dir: Path) -> dict:
    df = pd.read_csv(dataset_path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    required = NUMERIC_FEATURES + CATEGORICAL_FEATURES + REGRESSION_TARGETS + CLASSIFICATION_TARGETS
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    x = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    models = {}
    metrics = {}

    for target in REGRESSION_TARGETS:
        y = df[target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        model = Pipeline(
            steps=[
                ("preprocess", build_preprocessor()),
                ("model", RandomForestRegressor(n_estimators=180, random_state=42, n_jobs=-1)),
            ]
        )
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        models[target] = model
        metrics[target] = {
            "mae": round(float(mean_absolute_error(y_test, pred)), 3),
            "r2": round(float(r2_score(y_test, pred)), 3),
        }

    for target in CLASSIFICATION_TARGETS:
        y = df[target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
        model = Pipeline(
            steps=[
                ("preprocess", build_preprocessor()),
                ("model", RandomForestClassifier(n_estimators=180, random_state=42, n_jobs=-1, class_weight="balanced")),
            ]
        )
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        models[target] = model
        metrics[target] = {"accuracy": round(float(accuracy_score(y_test, pred)), 3)}

    profile = {
        "rows": int(len(df)),
        "date_min": str(df["date"].min().date()),
        "date_max": str(df["date"].max().date()),
        "categories": sorted(df["category"].dropna().unique().tolist()),
        "features": NUMERIC_FEATURES + CATEGORICAL_FEATURES,
        "targets": REGRESSION_TARGETS + CLASSIFICATION_TARGETS,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    bundle = {"models": models, "metrics": metrics, "profile": profile}
    artifact_path = output_dir / "finance_models.joblib"
    metrics_path = output_dir / "finance_model_metrics.json"
    joblib.dump(bundle, artifact_path)
    metrics_path.write_text(json.dumps({"profile": profile, "metrics": metrics}, indent=2), encoding="utf-8")
    return {"artifact_path": str(artifact_path), "metrics_path": str(metrics_path), "profile": profile, "metrics": metrics}


def main() -> None:
    parser = argparse.ArgumentParser(description="Train FinMate AI models from the personal finance tracker dataset.")
    parser.add_argument("--dataset", type=Path, default=Path("../data/personal_finance_tracker_dataset.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("../../backend/app/ml_artifacts"))
    args = parser.parse_args()
    result = train(args.dataset.resolve(), args.output_dir.resolve())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
