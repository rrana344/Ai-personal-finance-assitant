from datetime import date

from sqlalchemy.orm import Session

from app import models

DEMO_USER_ID = 1


def seed_demo_data(db: Session) -> None:
    existing = db.query(models.Transaction).filter(models.Transaction.user_id == DEMO_USER_ID).first()
    if existing:
        _backfill_demo_history(db)
        return

    transactions = [
        models.Transaction(user_id=DEMO_USER_ID, amount=50000, category="Salary", type="income", date=date(2026, 5, 1), notes="Monthly salary", payment_method="Bank Transfer"),
        models.Transaction(user_id=DEMO_USER_ID, amount=4500, category="Food", type="expense", date=date(2026, 5, 2), notes="Groceries and dining", payment_method="UPI"),
        models.Transaction(user_id=DEMO_USER_ID, amount=12000, category="Rent", type="expense", date=date(2026, 5, 3), notes="Apartment rent", payment_method="Bank Transfer"),
        models.Transaction(user_id=DEMO_USER_ID, amount=3000, category="Shopping", type="expense", date=date(2026, 5, 4), notes="Clothes and essentials", payment_method="Card"),
        models.Transaction(user_id=DEMO_USER_ID, amount=1800, category="Bills", type="expense", date=date(2026, 5, 5), notes="Internet and electricity", payment_method="Auto Pay"),
        models.Transaction(user_id=DEMO_USER_ID, amount=2200, category="Travel", type="expense", date=date(2026, 5, 6), notes="Cab and metro rides", payment_method="UPI"),
        models.Transaction(user_id=DEMO_USER_ID, amount=6500, category="Freelance", type="income", date=date(2026, 4, 20), notes="Side project payout", payment_method="Bank Transfer"),
        models.Transaction(user_id=DEMO_USER_ID, amount=3800, category="Health", type="expense", date=date(2026, 4, 15), notes="Clinic and medicines", payment_method="Card"),
        models.Transaction(user_id=DEMO_USER_ID, amount=4200, category="Education", type="expense", date=date(2026, 4, 10), notes="Course subscription", payment_method="Card"),
        models.Transaction(user_id=DEMO_USER_ID, amount=2500, category="Entertainment", type="expense", date=date(2026, 4, 8), notes="Movies and streaming", payment_method="UPI"),
    ]
    budgets = [
        models.Budget(user_id=DEMO_USER_ID, category="Food", month="2026-05", limit_amount=7000),
        models.Budget(user_id=DEMO_USER_ID, category="Shopping", month="2026-05", limit_amount=5000),
        models.Budget(user_id=DEMO_USER_ID, category="Travel", month="2026-05", limit_amount=4000),
        models.Budget(user_id=DEMO_USER_ID, category="Bills", month="2026-05", limit_amount=3000),
    ]
    goals = [
        models.Goal(user_id=DEMO_USER_ID, title="Emergency Fund", target_amount=150000, current_amount=62000, deadline=date(2026, 12, 31)),
        models.Goal(user_id=DEMO_USER_ID, title="Buy Laptop", target_amount=90000, current_amount=38000, deadline=date(2026, 8, 31)),
        models.Goal(user_id=DEMO_USER_ID, title="Vacation Savings", target_amount=120000, current_amount=45000, deadline=date(2027, 1, 15)),
    ]
    notifications = [
        models.Notification(user_id=DEMO_USER_ID, title="Demo Mode Enabled", message="No login required. Explore every finance feature instantly.", level="success"),
        models.Notification(user_id=DEMO_USER_ID, title="Budget looks healthy", message="Food spending is under the monthly demo budget.", level="info"),
    ]

    db.add_all(transactions + budgets + goals + notifications)
    db.commit()


def _backfill_demo_history(db: Session) -> None:
    existing_notes = {
        note
        for (note,) in db.query(models.Transaction.notes).filter(models.Transaction.user_id == DEMO_USER_ID).all()
        if note
    }
    transactions = [
        models.Transaction(user_id=DEMO_USER_ID, amount=50000, category="Salary", type="income", date=date(2026, 3, 1), notes="March salary", payment_method="Bank Transfer"),
        models.Transaction(user_id=DEMO_USER_ID, amount=50000, category="Salary", type="income", date=date(2026, 2, 1), notes="February salary", payment_method="Bank Transfer"),
        models.Transaction(user_id=DEMO_USER_ID, amount=49000, category="Salary", type="income", date=date(2026, 1, 1), notes="January salary", payment_method="Bank Transfer"),
        models.Transaction(user_id=DEMO_USER_ID, amount=6100, category="Food", type="expense", date=date(2026, 3, 8), notes="March groceries and dining", payment_method="UPI"),
        models.Transaction(user_id=DEMO_USER_ID, amount=3900, category="Food", type="expense", date=date(2026, 2, 8), notes="February groceries and dining", payment_method="UPI"),
        models.Transaction(user_id=DEMO_USER_ID, amount=12000, category="Rent", type="expense", date=date(2026, 3, 3), notes="March apartment rent", payment_method="Bank Transfer"),
        models.Transaction(user_id=DEMO_USER_ID, amount=12000, category="Rent", type="expense", date=date(2026, 2, 3), notes="February apartment rent", payment_method="Bank Transfer"),
        models.Transaction(user_id=DEMO_USER_ID, amount=5200, category="Shopping", type="expense", date=date(2026, 3, 14), notes="March shopping", payment_method="Card"),
        models.Transaction(user_id=DEMO_USER_ID, amount=1700, category="Subscriptions", type="expense", date=date(2026, 3, 17), notes="Streaming and apps", payment_method="Auto Pay"),
        models.Transaction(user_id=DEMO_USER_ID, amount=14500, category="Travel", type="expense", date=date(2026, 2, 21), notes="Weekend trip anomaly", payment_method="Card"),
    ]
    additions = [txn for txn in transactions if txn.notes not in existing_notes]
    if additions:
        db.add_all(additions)
        db.commit()
