from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.database import SessionLocal
from app.demo import seed_demo_data
from app.routes import admin, analytics, budgets, chat, goals, reports, transactions, uploads

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_demo_data(db)

app = FastAPI(title=settings.app_name, version="1.0.0", swagger_ui_oauth2_redirect_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for api_prefix in ("", "/api"):
    app.include_router(transactions.router, prefix=api_prefix)
    app.include_router(analytics.router, prefix=api_prefix)
    app.include_router(budgets.router, prefix=api_prefix)
    app.include_router(goals.router, prefix=api_prefix)
    app.include_router(chat.router, prefix=api_prefix)
    app.include_router(reports.router, prefix=api_prefix)
    app.include_router(uploads.router, prefix=api_prefix)
    app.include_router(admin.router, prefix=api_prefix)


@app.get("/")
def root():
    return {"name": settings.app_name, "status": "ready"}
