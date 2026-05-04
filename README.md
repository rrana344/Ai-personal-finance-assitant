# FinMate AI

Full-stack AI-powered personal finance assistant for tracking income, expenses, budgets, goals, reports, predictions, receipt uploads, and AI-driven insights.

## Tech Stack

- Frontend: React, Vite, Tailwind CSS, Recharts, Axios, React Router
- Backend: FastAPI, SQLite, SQLAlchemy, JWT auth, passlib password hashing
- AI/ML: OpenAI-compatible optional chatbot, local rule-based fallback, pandas/scikit-learn prediction helpers
- Reports: CSV export endpoint
- OCR: Upload endpoint with optional pytesseract support

## Project Structure

```text
finance-assistant/
├── frontend/
├── backend/
├── ai/
├── uploads/
├── reports/
└── tests/
```

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

## Environment

Backend variables live in `backend/.env`.

- `SECRET_KEY`: JWT signing secret
- `DATABASE_URL`: defaults to local SQLite
- `OPENAI_API_KEY`: optional, enables real AI chat responses
- `OPENAI_MODEL`: optional, defaults to `gpt-4o-mini`

Frontend variables live in `frontend/.env`.

- `VITE_API_URL`: defaults to `http://localhost:8000`

## Demo Flow

1. Create an account from Signup.
2. Add income and expense transactions.
3. Create budgets and savings goals.
4. View dashboard analytics and financial health score.
5. Chat with the AI assistant for spending summaries and savings advice.
6. Upload a receipt to extract a draft transaction.
7. Export a CSV report.

## Resume Summary

Developed a full-stack AI-powered Personal Finance Assistant using React, FastAPI, SQLite/PostgreSQL-ready SQLAlchemy, JWT authentication, and Machine Learning helpers. Implemented intelligent expense tracking, budgeting, financial analytics, AI chatbot, expense prediction models, OCR receipt scanning, and interactive dashboards for personalized financial management.
