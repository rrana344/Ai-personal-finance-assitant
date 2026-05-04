# AI Modules

The production API lives in `backend/app/services`.

- `ai_chat.py`: OpenAI-compatible chat with local fallback.
- `prediction.py`: scikit-learn linear regression forecast.
- `ocr.py`: receipt extraction with optional Tesseract.

## Training With Provided Dataset

The provided CSV has been copied to:

```text
ai/data/personal_finance_tracker_dataset.csv
```

Train the ML models:

```bash
cd ai/training
python train_finance_models.py
```

The script trains Random Forest models for:

- monthly expense prediction
- actual savings forecasting
- financial advice score prediction
- financial stress classification
- savings-goal success classification

It writes:

- `backend/app/ml_artifacts/finance_models.joblib`
- `backend/app/ml_artifacts/finance_model_metrics.json`

The `/predictions` API automatically uses the trained artifact when it exists, while still returning the live transaction trend forecast.
