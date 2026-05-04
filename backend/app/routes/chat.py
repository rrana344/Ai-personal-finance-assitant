import asyncio

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.demo import DEMO_USER_ID
from app.services.ai_chat import answer_finance_question

router = APIRouter(prefix="/chat", tags=["AI Chat"])


@router.post("", response_model=schemas.ChatResponse)
async def chat(payload: schemas.ChatRequest, db: Session = Depends(get_db)):
    answer = await answer_finance_question(db, DEMO_USER_ID, payload.message)
    return {"answer": answer}


@router.get("/history")
def chat_history(db: Session = Depends(get_db)):
    messages = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == DEMO_USER_ID)
        .order_by(models.ChatMessage.created_at.asc())
        .limit(30)
        .all()
    )
    return [{"role": item.role, "content": item.content, "created_at": item.created_at} for item in messages]


@router.post("/stream")
async def chat_stream(payload: schemas.ChatRequest, db: Session = Depends(get_db)):
    answer = await answer_finance_question(db, DEMO_USER_ID, payload.message)

    async def chunks():
        for word in answer.split(" "):
            yield f"{word} "
            await asyncio.sleep(0.015)

    return StreamingResponse(chunks(), media_type="text/plain")
