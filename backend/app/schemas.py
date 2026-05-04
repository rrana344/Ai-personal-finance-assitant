from datetime import date as dt_date, datetime

from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    amount: float = Field(gt=0)
    category: str
    type: str = Field(pattern="^(income|expense)$")
    date: dt_date
    notes: str | None = None
    payment_method: str = "Card"
    status: str = "Cleared"


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: float | None = Field(default=None, gt=0)
    category: str | None = None
    type: str | None = Field(default=None, pattern="^(income|expense)$")
    date: dt_date | None = None
    notes: str | None = None
    payment_method: str | None = None
    status: str | None = None


class TransactionOut(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    category: str
    month: str = Field(pattern=r"^\d{4}-\d{2}$")
    limit_amount: float = Field(gt=0)


class BudgetOut(BudgetCreate):
    id: int
    spent: float = 0
    remaining: float = 0
    usage_percent: float = 0

    class Config:
        from_attributes = True


class GoalCreate(BaseModel):
    title: str
    target_amount: float = Field(gt=0)
    current_amount: float = Field(default=0, ge=0)
    deadline: dt_date | None = None


class GoalOut(GoalCreate):
    id: int
    progress_percent: float

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    level: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True
