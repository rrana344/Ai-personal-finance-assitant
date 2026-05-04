from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.demo import DEMO_USER_ID

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("", response_model=list[schemas.BudgetOut])
def list_budgets(db: Session = Depends(get_db)):
    budgets = db.query(models.Budget).filter(models.Budget.user_id == DEMO_USER_ID).all()
    return [_with_usage(db, budget) for budget in budgets]


@router.post("", response_model=schemas.BudgetOut)
def create_budget(payload: schemas.BudgetCreate, db: Session = Depends(get_db)):
    budget = models.Budget(user_id=DEMO_USER_ID, **payload.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return _with_usage(db, budget)


def _with_usage(db: Session, budget: models.Budget) -> dict:
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == budget.user_id,
        models.Transaction.type == "expense",
        models.Transaction.category == budget.category,
    ).all()
    spent = sum(t.amount for t in transactions if t.date.strftime("%Y-%m") == budget.month)
    remaining = budget.limit_amount - spent
    return {
        "id": budget.id,
        "category": budget.category,
        "month": budget.month,
        "limit_amount": budget.limit_amount,
        "spent": round(spent, 2),
        "remaining": round(remaining, 2),
        "usage_percent": round(min(spent / budget.limit_amount * 100, 999), 1),
    }
