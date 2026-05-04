from pathlib import Path
from datetime import date

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.demo import DEMO_USER_ID
from app.services.ocr import extract_receipt_data

router = APIRouter(prefix="/uploads", tags=["OCR"])
UPLOAD_DIR = Path("uploads")


@router.post("/receipt")
async def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    UPLOAD_DIR.mkdir(exist_ok=True)
    path = UPLOAD_DIR / f"demo-{DEMO_USER_ID}-{file.filename}"
    path.write_bytes(await file.read())
    data = extract_receipt_data(path)
    transaction = None
    if data.get("amount"):
        transaction = models.Transaction(
            user_id=DEMO_USER_ID,
            amount=float(data["amount"]),
            category=data.get("category") or "Bills",
            type="expense",
            date=date.today(),
            notes=f"OCR import from {file.filename}",
            payment_method="Receipt Upload",
            status="Needs Review",
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
    return {
        **data,
        "transaction": {
            "id": transaction.id,
            "amount": transaction.amount,
            "category": transaction.category,
            "date": transaction.date,
            "status": transaction.status,
        }
        if transaction
        else None,
    }
