# FinGuard AI (AI Finance Controller)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-ai--finguard.netlify.app-blue?style=for-the-badge&logo=netlify)](https://ai-finguard.netlify.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-FinGuard--AI-black?style=for-the-badge&logo=github)](https://github.com/anjaliprasad24/FinGuard-AI)

Production-ready autonomous AI Finance Controller & Copilot system built with FastAPI, Next.js 14, PostgreSQL (pgvector), Scikit-Learn IsolationForest anomaly detection, and XAI grounded RAG.

🌐 **Live Demo:** [https://ai-finguard.netlify.app/](https://ai-finguard.netlify.app/)  
📦 **GitHub Repository:** [https://github.com/anjaliprasad24/FinGuard-AI](https://github.com/anjaliprasad24/FinGuard-AI)

---

## Tech Stack
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Recharts, Lucide Icons
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic
- **Analytics & ML:** Scikit-Learn (IsolationForest), Statsmodels/Pandas/NumPy
- **OCR & PII:** Tesseract (pytesseract), Regex PII Masker
- **Database & Vector Store:** PostgreSQL 16 + pgvector (or local SQLite)

---

## System Architecture

```text
  [ Raw Request / Upload ]
             │
             ▼
  ┌───────────────────────┐
  │   1. PII Scrubber     │ ──> Regex masks card numbers, PAN, phone, names
  └──────────┬────────────┘
             ▼
  ┌───────────────────────┐
  │ 2. Category & Entity  │ ──> Categorizes merchant + confidence score
  └──────────┬────────────┘
             ▼
  ┌───────────────────────┐
  │  3. Anomaly Engine    │ ──> Isolation Forest + Z-score against user's history
  └──────────┬────────────┘
             ▼
  ┌───────────────────────┐
  │  4. Policy & Runway   │ ──> Check limits, project month-end burn, test reserve floor
  └──────────┬────────────┘
             ▼
  ┌───────────────────────┐
  │  5. Goal Trajectory   │ ──> Recalculate target completion dates
  └──────────┬────────────┘
             ▼
  ┌───────────────────────┐
  │ 6. XAI Evidence Pack  │ ──> Construct structured JSON evidence
  └──────────┬────────────┘
             ▼
  ┌───────────────────────┐
  │ 7. Audit & Copilot    │ ──> Commit to SQL & trigger contextual LLM summary
  └──────────┬────────────┘
```

---

## Getting Started

### Using Docker
```bash
docker-compose up --build
```

### Local Execution (No Docker)
```bash
# Terminal 1: Backend
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```
