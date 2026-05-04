from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.demo import DEMO_USER_ID
from app.services.analytics import build_analytics, user_transactions
from app.services.prediction import predict_next_month

router = APIRouter(tags=["Analytics"])


@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    return build_analytics(db, DEMO_USER_ID)


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return build_analytics(db, DEMO_USER_ID)["summary"]


@router.get("/dashboard/trends")
def dashboard_trends(db: Session = Depends(get_db)):
    return build_analytics(db, DEMO_USER_ID)["monthly_trend"]


@router.get("/dashboard/categories")
def dashboard_categories(db: Session = Depends(get_db)):
    return build_analytics(db, DEMO_USER_ID)["category_expenses"]


@router.get("/dashboard/insights")
def dashboard_insights(db: Session = Depends(get_db)):
    analytics_data = build_analytics(db, DEMO_USER_ID)
    return {"insights": analytics_data["insights"], "alerts": analytics_data["alerts"], "recommendations": analytics_data["recommendations"]}


@router.get("/dashboard/health-score")
def dashboard_health_score(db: Session = Depends(get_db)):
    return build_analytics(db, DEMO_USER_ID)["health_score"]


@router.get("/predictions")
def predictions(db: Session = Depends(get_db)):
    return predict_next_month(user_transactions(db, DEMO_USER_ID))
