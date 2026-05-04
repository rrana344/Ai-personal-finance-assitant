from collections import defaultdict
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app import models


def user_transactions(db: Session, user_id: int) -> list[models.Transaction]:
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.date.desc()).all()


def build_analytics(db: Session, user_id: int) -> dict:
    transactions = user_transactions(db, user_id)
    budgets = db.query(models.Budget).filter(models.Budget.user_id == user_id).all()
    today = date.today()
    current_month = today.strftime("%Y-%m")
    previous_month = _shift_month(today, -1)

    income = sum(t.amount for t in transactions if t.type == "income")
    expenses = sum(t.amount for t in transactions if t.type == "expense")
    savings = income - expenses

    by_category: dict[str, float] = defaultdict(float)
    monthly: dict[str, dict[str, float]] = defaultdict(lambda: {"income": 0, "expense": 0})
    current_category: dict[str, float] = defaultdict(float)
    previous_category: dict[str, float] = defaultdict(float)
    for txn in transactions:
        month = txn.date.strftime("%Y-%m")
        monthly[month][txn.type] += txn.amount
        if txn.type == "expense":
            by_category[txn.category] += txn.amount
            if month == current_month:
                current_category[txn.category] += txn.amount
            if month == previous_month:
                previous_category[txn.category] += txn.amount

    savings_ratio = (savings / income * 100) if income else 0
    current_income = monthly[current_month]["income"]
    current_expenses = monthly[current_month]["expense"]
    previous_expenses = monthly[previous_month]["expense"]
    monthly_comparison = _percent_change(current_expenses, previous_expenses)
    budget_rows = budget_status(transactions, budgets, current_month)
    budget_utilization = _budget_utilization(budget_rows)
    health = health_score(savings_ratio, income, expenses, budget_rows, transactions)
    insights = generate_insights(income, expenses, current_category, previous_category, budget_rows, monthly_comparison)

    return {
        "summary": {
            "total_balance": round(savings, 2),
            "total_income": round(income, 2),
            "total_expenses": round(expenses, 2),
            "monthly_income": round(current_income, 2),
            "monthly_expenses": round(current_expenses, 2),
            "savings": round(savings, 2),
            "savings_ratio": round(savings_ratio, 1),
            "budget_left": round(sum(item["remaining"] for item in budget_rows), 2),
            "budget_utilization": budget_utilization,
            "health_score": health["score"],
            "highest_expense_category": _top_category(by_category),
            "monthly_comparison": monthly_comparison,
        },
        "category_expenses": [{"name": k, "value": round(v, 2)} for k, v in sorted(by_category.items())],
        "monthly_trend": [
            {
                "month": month,
                "income": round(values["income"], 2),
                "expense": round(values["expense"], 2),
                "savings": round(values["income"] - values["expense"], 2),
            }
            for month, values in sorted(monthly.items())
        ],
        "recent_transactions": [_transaction_summary(txn) for txn in transactions[:8]],
        "budget_status": budget_rows,
        "insights": insights,
        "recommendations": recommendations(income, expenses, by_category, budget_rows),
        "health_score": health,
        "alerts": smart_alerts(insights, budget_rows, savings_ratio),
    }


def recommendations(income: float, expenses: float, by_category: dict[str, float], budgets: list[dict] | None = None) -> list[str]:
    tips = []
    if income and expenses / income > 0.8:
        tips.append("Your expenses are above 80% of income. Try moving one variable category into a weekly cap.")
    if by_category:
        category, amount = max(by_category.items(), key=lambda item: item[1])
        tips.append(f"{category} is your highest spend category at Rs.{amount:,.0f}. Review recurring purchases there first.")
    exceeded = [budget for budget in budgets or [] if budget["remaining"] < 0]
    if exceeded:
        budget = exceeded[0]
        tips.append(f"Warning: {budget['category']} budget exceeded by {abs(budget['remaining']) / budget['limit_amount'] * 100:.0f}%.")
    if income > expenses:
        tips.append("You are saving this period. Automating part of the surplus can help protect it.")
    return tips or ["Add transactions to unlock personalized recommendations."]


def _transaction_summary(txn: models.Transaction) -> dict:
    return {
        "id": txn.id,
        "date": txn.date,
        "category": txn.category,
        "amount": txn.amount,
        "type": txn.type,
        "status": txn.status,
        "notes": txn.notes,
        "payment_method": txn.payment_method,
    }


def budget_status(transactions: list[models.Transaction], budgets: list[models.Budget], month: str | None = None) -> list[dict]:
    selected_month = month or date.today().strftime("%Y-%m")
    rows = []
    for budget in budgets:
        spent = sum(
            txn.amount
            for txn in transactions
            if txn.type == "expense" and txn.category == budget.category and txn.date.strftime("%Y-%m") == budget.month
        )
        remaining = budget.limit_amount - spent
        usage = (spent / budget.limit_amount * 100) if budget.limit_amount else 0
        rows.append(
            {
                "id": budget.id,
                "category": budget.category,
                "month": budget.month,
                "limit_amount": round(budget.limit_amount, 2),
                "spent": round(spent, 2),
                "remaining": round(remaining, 2),
                "usage_percent": round(usage, 1),
                "status": "exceeded" if remaining < 0 else "watch" if usage >= 80 else "healthy",
                "is_current_month": budget.month == selected_month,
            }
        )
    return rows


def generate_insights(
    income: float,
    expenses: float,
    current_category: dict[str, float],
    previous_category: dict[str, float],
    budgets: list[dict],
    monthly_comparison: float,
) -> list[dict]:
    insights = []
    for category, amount in sorted(current_category.items(), key=lambda item: item[1], reverse=True):
        previous = previous_category.get(category, 0)
        change = amount - previous
        if previous and abs(change) >= 500:
            direction = "increased" if change > 0 else "decreased"
            insights.append(
                {
                    "title": f"{category} spend {direction}",
                    "message": f"{category} expenses {direction} by Rs.{abs(change):,.0f} this month.",
                    "impact": "warning" if change > 0 else "positive",
                }
            )
    if monthly_comparison > 10:
        insights.append(
            {
                "title": "Monthly expenses are rising",
                "message": f"You spent {monthly_comparison:.0f}% more than last month.",
                "impact": "warning",
            }
        )
    if income and income > expenses:
        insights.append(
            {
                "title": "Savings rate improved",
                "message": f"You can route up to Rs.{max((income - expenses) * 0.25, 0):,.0f} into goals without stressing cash flow.",
                "impact": "positive",
            }
        )
    for budget in budgets:
        if budget["status"] == "exceeded":
            insights.append(
                {
                    "title": f"{budget['category']} budget exceeded",
                    "message": f"Warning: {budget['category']} budget exceeded by {abs(budget['remaining']) / budget['limit_amount'] * 100:.0f}%.",
                    "impact": "critical",
                }
            )
    return insights[:6] or [{"title": "Healthy demo baseline", "message": "Demo data is loaded and ready for finance analysis.", "impact": "positive"}]


def health_score(savings_ratio: float, income: float, expenses: float, budgets: list[dict], transactions: list[models.Transaction]) -> dict:
    expense_ratio = (expenses / income * 100) if income else 100
    budget_penalty = sum(12 for budget in budgets if budget["status"] == "exceeded")
    consistency = _spending_consistency(transactions)
    emergency_score = min(max((income - expenses) / max(expenses / 3, 1) * 20, 0), 20)
    score = 35 + min(savings_ratio, 35) + (100 - min(expense_ratio, 100)) * 0.18 + consistency * 0.12 + emergency_score - budget_penalty
    score = max(0, min(100, round(score)))
    return {
        "score": score,
        "label": "Excellent" if score >= 85 else "Strong" if score >= 70 else "Needs attention" if score >= 50 else "At risk",
        "factors": {
            "savings_rate": round(savings_ratio, 1),
            "expense_ratio": round(expense_ratio, 1),
            "spending_consistency": round(consistency, 1),
            "budget_discipline": max(0, 100 - budget_penalty * 5),
        },
    }


def smart_alerts(insights: list[dict], budgets: list[dict], savings_ratio: float) -> list[dict]:
    alerts = []
    if savings_ratio < 15:
        alerts.append({"title": "Low savings", "message": "Savings ratio is below 15%. Review discretionary spending.", "level": "warning"})
    for budget in budgets:
        if budget["status"] in {"watch", "exceeded"}:
            alerts.append({"title": f"{budget['category']} budget {budget['status']}", "message": f"{budget['usage_percent']}% used.", "level": "critical" if budget["status"] == "exceeded" else "warning"})
    for insight in insights:
        if insight["impact"] in {"warning", "critical"}:
            alerts.append({"title": insight["title"], "message": insight["message"], "level": insight["impact"]})
    return alerts[:5]


def _budget_utilization(budgets: list[dict]) -> float:
    current = [budget for budget in budgets if budget["is_current_month"]]
    if not current:
        return 0
    total_limit = sum(budget["limit_amount"] for budget in current)
    total_spent = sum(budget["spent"] for budget in current)
    return round((total_spent / total_limit * 100) if total_limit else 0, 1)


def _top_category(values: dict[str, float]) -> str | None:
    return max(values.items(), key=lambda item: item[1])[0] if values else None


def _shift_month(day: date, months: int) -> str:
    month = day.month - 1 + months
    year = day.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1).strftime("%Y-%m")


def _percent_change(current: float, previous: float) -> float:
    if not previous:
        return 0
    return round((current - previous) / previous * 100, 1)


def _spending_consistency(transactions: list[models.Transaction]) -> float:
    month_totals: dict[str, float] = defaultdict(float)
    for txn in transactions:
        if txn.type == "expense":
            month_totals[txn.date.strftime("%Y-%m")] += txn.amount
    values = list(month_totals.values())
    if len(values) < 2:
        return 75
    average = sum(values) / len(values)
    variance = sum(abs(value - average) for value in values) / len(values)
    return max(0, min(100, 100 - (variance / average * 100 if average else 0)))
