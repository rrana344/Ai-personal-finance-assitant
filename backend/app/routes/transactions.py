from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.demo import DEMO_USER_ID

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=list[schemas.TransactionOut])
def list_transactions(
    search: str | None = None,
    category: str | None = None,
    type: str | None = Query(default=None, pattern="^(income|expense)$"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == DEMO_USER_ID)
    if search:
        query = query.filter(models.Transaction.notes.ilike(f"%{search}%"))
    if category:
        query = query.filter(models.Transaction.category == category)
    if type:
        query = query.filter(models.Transaction.type == type)
    return query.order_by(models.Transaction.date.desc()).all()


@router.post("", response_model=schemas.TransactionOut)
def create_transaction(
    payload: schemas.TransactionCreate,
    db: Session = Depends(get_db),
):
    txn = models.Transaction(user_id=DEMO_USER_ID, **payload.model_dump())
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


@router.put("/{transaction_id}", response_model=schemas.TransactionOut)
def update_transaction(
    transaction_id: int,
    payload: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
):
    txn = _get_transaction(db, transaction_id, DEMO_USER_ID)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(txn, key, value)
    db.commit()
    db.refresh(txn)
    return txn


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    txn = _get_transaction(db, transaction_id, DEMO_USER_ID)
    db.delete(txn)
    db.commit()
    return {"message": "Transaction deleted"}


def _get_transaction(db: Session, transaction_id: int, user_id: int) -> models.Transaction:
    txn = db.query(models.Transaction).filter(models.Transaction.id == transaction_id, models.Transaction.user_id == user_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn
