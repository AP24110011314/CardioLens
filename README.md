# CardioLens — Heart Disease Risk Prediction App

A Streamlit web app that estimates the likelihood of heart disease from 11 clinical inputs, using a K-Nearest Neighbors model trained in Google Colab.

> ⚠️ **Educational project. Not a medical device and not a diagnosis.** Always consult a qualified doctor.

## Features
- **Guided input form**: Friendly labels, validated ranges, and "I don't know" cholesterol handling.
- **Risk probability**: Plotly gauge, risk band (Low, Moderate, High), and plain-language summary.
- **Explainability**: Key-factor sensitivity breakdown and interactive what-if sliders.
- **Similar patients**: k-nearest reference cases with true outcomes.
- **Batch prediction**: Upload CSV, validate schema and ranges, download scored dataset.
- **Session history**: Local session prediction log, trend chart, and CSV export.
- **PDF report**: ReportLab one-page downloadable summary.
- **Model Info**: Architecture, hyperparameters, confusion matrix, limitations.
- **Dark theme & responsive**: Built for desktop and mobile.

## Tech Stack
Python 3.13 · Streamlit · scikit-learn 1.6.1 · pandas · joblib · Plotly · ReportLab

## Project Structure
```
HeartDisease/
├── app.py                    # entry point: page config & navigation
├── pages/
│   ├── 1_Predict.py          # form + result + what-if / similar / compare tabs
│   ├── 2_Batch_Prediction.py # batch CSV upload & download
│   ├── 3_Insights.py         # session history & trend
│   ├── 4_Model_Info.py       # model metrics & limitations
│   └── 5_About.py            # medical background & credits
├── src/
│   ├── config.py             # central specs, encodings, ranges, risk bands
│   ├── model_loader.py       # cached loaders for model/scaler/columns/metrics
│   ├── preprocessing.py      # build_frame, impute, encode, scale
│   ├── predict.py            # predict_single, predict_batch, risk bands
│   ├── explain.py            # sensitivity, what-if, neighbours
│   ├── report.py             # PDF generation
│   └── ui.py                 # custom CSS, gauge, badge, disclaimer
├── models/                   # KNN_heart.pkl, scaler.pkl, columns.pkl
├── data/                     # heart_reference.csv, model_metrics.json (exported from Colab)
├── tests/                    # pytest test suite
├── docs/                     # PRD, Architecture, UI design, features, model notes
├── .streamlit/config.toml    # dark theme configuration
└── requirements.txt
```

## Setup & Run

```bash
# 1. Clone & create Python 3.13 venv
git clone <your-repo-url> && cd HeartDisease
python3.13 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

## Running Tests

```bash
pytest -q
```

## Model & Data
- Dataset: *Heart Failure Prediction Dataset* (fedesoriano, Kaggle, 2021) — 918 records, 11 features, merged from five public cardiology datasets (Cleveland, Hungarian, Switzerland, Long Beach VA, Statlog).
- See `docs/MODEL_NOTES.md` for architecture details, limitations, and retraining instructions.

## Documentation Index
| Document | Content |
|---|---|
| [docs/PRD.md](docs/PRD.md) | Product requirements, personas, scope |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture, data flow, module contracts |
| [docs/UI_DESIGN.md](docs/UI_DESIGN.md) | Design system, tokens, layout, copy table |
| [docs/FEATURES.md](docs/FEATURES.md) | Feature specifications & acceptance criteria |
| [docs/MODEL_NOTES.md](docs/MODEL_NOTES.md) | Model details, fixes, retraining pipeline |
| [docs/TASKS.md](docs/TASKS.md) | Implementation checklist |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Streamlit Cloud deployment guide |

## Credits
Built by Aman. Dataset: fedesoriano (2021), Heart Failure Prediction Dataset, Kaggle.
