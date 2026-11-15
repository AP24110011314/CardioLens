# CardioLens — Heart Disease Risk Prediction App

A Streamlit web app that estimates the likelihood of heart disease from 11 clinical inputs, using a K-Nearest Neighbors model trained in Google Colab.

> ⚠️ **Educational project. Not a medical device and not a diagnosis.** Always consult a qualified doctor.

## Features
- Guided input form with friendly labels and valid ranges
- Risk probability with gauge, risk band and plain-language summary
- "Why this result?" — key-factor breakdown and what-if sliders
- Similar patients from the reference dataset (KNN neighbours)
- Batch prediction from a CSV upload, with downloadable results
- Prediction history (session only) with CSV export
- PDF report download
- Model Info page: metrics, confusion matrix, ROC curve, limitations
- Dark/light theme, mobile-friendly layout

See `PRD.md` and `FEATURES.md` for the full scope.

## Tech stack
Python · Streamlit · scikit-learn (KNN + StandardScaler) · pandas · joblib · Plotly · ReportLab (PDF)

## Project structure
See `ARCHITECTURE.md`. Short version:
```
app.py            # entry point + navigation
pages/            # Predict, Batch, Insights, Model Info, About
src/              # config, model_loader, preprocessing, predict, explain, report, ui
models/           # KNN_heart.pkl, scaler.pkl, columns.pkl
data/             # heart_reference.csv, model_metrics.json
tests/
```

## Setup
```bash
git clone <your-repo-url> && cd HeartDisease
python3.12 -m venv .venv && source .venv/bin/activate   # use 3.12 or 3.13
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501.

## Model & data
- Dataset: *Heart Failure Prediction Dataset* (fedesoriano, Kaggle, 2021) — 918 records, 11 features, merged from five public cardiology datasets (Cleveland, Hungarian, Switzerland, Long Beach VA, Statlog).
- Details, known issues and retraining steps: `MODEL_NOTES.md`.

## Docs index
| File | Purpose |
|---|---|
| `PRD.md` | Goals, users, requirements, scope |
| `FEATURES.md` | Feature specs with acceptance criteria |
| `UI_DESIGN.md` | Design system, layout, copy |
| `ARCHITECTURE.md` | Structure, data flow, modules |
| `MODEL_NOTES.md` | Model, data, fixes, ethics |
| `TASKS.md` | Step-by-step implementation checklist |
| `DEPLOYMENT.md` | Streamlit Cloud / alternatives |
| `AGENTS.md` | Rules for Claude Code / OpenCode |

## Credits
Built by Aman. Dataset: fedesoriano (2021), Heart Failure Prediction Dataset, Kaggle.
