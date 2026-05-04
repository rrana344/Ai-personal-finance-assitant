from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    return {
        "mode": "Public Demo",
        "transactions": db.query(models.Transaction).count(),
        "chat_messages": db.query(models.ChatMessage).count(),
        "reports": "CSV export enabled",
    }
