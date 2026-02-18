# 📹 5-Minute Demo Video Script

## Setup Before Recording
- Docker containers running (`docker-compose up -d`)
- Streamlit running (`python -m streamlit run frontend/app.py`)
- Postman open
- Browser tabs ready: localhost:8000/docs, localhost:3000, localhost:8501, GitHub repo

---

## Script (5 minutes)

### 0:00–0:30 — Introduction (30s)
- "Hi, I'm [Name]. This is my Student Depression Classification Pipeline for MTA Advanced Analytics II."
- "I'll walk through the entire system — from data to deployment."
- Show the GitHub repo briefly.

### 0:30–1:00 — Data Layer (30s)
- Open `data/load_to_postgres.py` — "100K student records stored in Neon Postgres."
- Open `src/data_loader.py` — "SQLAlchemy loads from Postgres, with CSV fallback."
- Quick terminal: `python -c "from src.data_loader import load_data_from_postgres; df = load_data_from_postgres(); print(df.shape)"`

### 1:00–1:45 — Model Training (45s)
- Open `src/train.py` — "scikit-learn Pipeline: StandardScaler + OneHotEncoder + RandomForest."
- "RandomizedSearchCV with 50 iterations, F1 scoring, balanced class weights."
- Show `models/metrics.json` — highlight F1, recall, best params.
- "Key insight: had to use class_weight=balanced because 90% of data is No Depression."

### 1:45–2:15 — W&B Tracking (30s)
- Open W&B dashboard in browser.
- Show experiment runs, metrics, confusion matrix, ROC curve.
- "Every experiment tracked — metrics, parameters, and model artifacts."

### 2:15–3:00 — FastAPI API (45s)
- Open http://localhost:8000/docs (Swagger UI).
- Show the 3 endpoints: /predict, /health, /metrics.
- Live demo: Click POST /predict → Try it out → Submit sample data → Show response.
- Click GET /health → Show healthy response.

### 3:00–3:30 — Postman Testing (30s)
- Switch to Postman.
- Send POST /predict with valid data → Show 200 response.
- Send POST /predict with missing fields → Show 422 error.
- "Pydantic validates all inputs with field-level constraints."

### 3:30–4:00 — Streamlit Frontend (30s)
- Open http://localhost:8501.
- Adjust sliders: set stress=10, sleep=3 → Predict → Show "Depression" result.
- Adjust sliders: set stress=2, sleep=8 → Predict → Show "No Depression" result.
- "Interactive UI that calls the FastAPI predict endpoint."

### 4:00–4:30 — Docker + Monitoring (30s)
- Terminal: `docker ps` — show 3 containers running.
- Open Grafana at http://localhost:3000 → Show the 6-panel dashboard.
- "Prometheus scrapes /metrics every 10 seconds. 6 Grafana panels for real-time monitoring."

### 4:30–5:00 — CI/CD, Tests & Conclusion (30s)
- Show `.github/workflows/backend.yml` — "Lint → Test → Deploy on push to main."
- Terminal: `python -m pytest tests/ -v` — "15 tests, all passing."
- Show Render dashboard briefly — "Backend and frontend deployed to Render."
- "Thank you! Full code on GitHub."

---

## Recording Tips
- Use OBS Studio, Loom, or Windows Game Bar (Win+G) to record.
- Record at 1080p, export as MP4.
- Speak clearly and keep a steady pace.
- Upload to YouTube (unlisted) or Google Drive and paste the link in the report.
