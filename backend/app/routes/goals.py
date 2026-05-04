from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.demo import DEMO_USER_ID

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("", response_model=list[schemas.GoalOut])
def list_goals(db: Session = Depends(get_db)):
    goals = db.query(models.Goal).filter(models.Goal.user_id == DEMO_USER_ID).all()
    return [_goal_out(goal) for goal in goals]


@router.post("", response_model=schemas.GoalOut)
def create_goal(payload: schemas.GoalCreate, db: Session = Depends(get_db)):
    goal = models.Goal(user_id=DEMO_USER_ID, **payload.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return _goal_out(goal)


def _goal_out(goal: models.Goal) -> dict:
    progress = round(min(goal.current_amount / goal.target_amount * 100, 100), 1)
    return {
        "id": goal.id,
        "title": goal.title,
        "target_amount": goal.target_amount,
        "current_amount": goal.current_amount,
        "deadline": goal.deadline,
        "progress_percent": progress,
    }
