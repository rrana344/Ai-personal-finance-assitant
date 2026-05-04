from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.services.analytics import build_analytics


async def answer_finance_question(db: Session, demo_user_id: int, message: str) -> str:
    analytics = build_analytics(db, demo_user_id)
    db.add(models.ChatMessage(user_id=demo_user_id, role="user", content=message))

    if settings.openai_api_key:
        answer = await _openai_answer(message, analytics)
    else:
        answer = _local_answer(message, analytics)

    db.add(models.ChatMessage(user_id=demo_user_id, role="assistant", content=answer))
    db.commit()
    return answer


async def _openai_answer(message: str, analytics: dict) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {
                "role": "system",
                "content": "You are a careful personal finance assistant. Give practical, concise, non-legal financial guidance.",
            },
            {"role": "user", "content": f"Finance snapshot: {analytics}\n\nQuestion: {message}"},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content or "I could not generate an answer."


def _local_answer(message: str, analytics: dict) -> str:
    text = message.lower()
    summary = analytics["summary"]
    categories = analytics["category_expenses"]
    top_category = max(categories, key=lambda item: item["value"], default=None)

    if "most" in text or "where" in text:
        if top_category:
            return f"You spent the most on {top_category['name']}: {top_category['value']:.2f}. That is the first category to review."
        return "I need a few expense transactions before I can identify your highest spending category."
    if "save" in text:
        return "A practical saving move: set a target transfer right after income arrives, then cap your largest variable category weekly."
    if "predict" in text or "next month" in text:
        latest = analytics["monthly_trend"][-3:]
        avg = sum(item["expense"] for item in latest) / len(latest) if latest else summary["total_expenses"]
        return f"Based on your recent trend, next month expenses may land near {avg:.2f}. Add more history for a stronger forecast."
    return (
        f"Your income is {summary['total_income']:.2f}, expenses are {summary['total_expenses']:.2f}, "
        f"and current savings are {summary['savings']:.2f}. Health score: {summary['health_score']}/100."
    )
