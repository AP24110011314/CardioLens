# ❤️ CardioLens — Heart Disease Risk Prediction

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cardiolenspro.streamlit.app)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn 1.6.1](https://img.shields.io/badge/scikit--learn-1.6.1-orange.svg)](https://scikit-learn.org/)

**CardioLens** is an interactive clinical ML web application that estimates heart disease risk probability from 11 standard health inputs using a K-Nearest Neighbors (KNN) model trained on the Kaggle Heart Failure Prediction Dataset.

🔗 **Live Application**: [https://cardiolenspro.streamlit.app](https://cardiolenspro.streamlit.app)

> ⚠️ **Disclaimer**: *CardioLens is an educational and portfolio project. It is not a certified medical device and does not provide clinical diagnoses or treatment advice. Always consult a licensed healthcare professional.*

---

## 🌟 Key Features

- **Guided Risk Assessment**: Grouped clinical input form with plain-language labels, tooltips, and validated physical ranges.
- **Missing Value Handling**: Handles missing cholesterol ("I don't know") with dataset median imputation.
- **Probabilistic Scoring**: Visual Plotly risk gauge mapped to **Low**, **Moderate**, and **High** risk bands.
- **Explainable AI (XAI)**:
  - *Key Factors*: Sensitivity breakdown comparing patient inputs against healthy reference baselines.
  - *What-If Analysis*: Real-time interactive sliders showing how lifestyle adjustments impact risk.
  - *Similar Patients*: Nearest reference neighbor lookup with true clinical outcomes.
  - *Population Comparison*: Distribution histograms comparing patient parameters to dataset distributions.
- **Batch CSV Scoring**: Upload tabular patient cohorts, validate schemas, score, and download enriched CSVs.
- **Downloadable Clinical Report**: Generates a one-page PDF risk summary via ReportLab.
- **Session History**: Track predictions within your session with interactive trend charts and CSV export.
- **Model Transparency**: Dedicated Model Info page detailing architecture, ROC-AUC, confusion matrix, and clinical limitations.

---

## 🛠️ Tech Stack

- **Frontend / Framework**: Streamlit
- **Machine Learning**: scikit-learn 1.6.1 (KNeighborsClassifier, StandardScaler)
- **Data & Computing**: pandas, numpy, joblib
- **Visualization**: Plotly Express & Plotly Graph Objects
- **Reporting**: ReportLab (PDF generation)
- **Quality & Testing**: pytest, ruff

---

## 🚀 Quickstart (Run Locally)

```bash
git clone https://github.com/AP24110011314/CardioLens.git
cd CardioLens
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧪 Running Tests

```bash
pytest -q
```

---

## 📊 Dataset & Credits

- **Dataset**: *Heart Failure Prediction Dataset* (fedesoriano, Kaggle, 2021) — 918 records across 11 features, merging five public cardiology cohorts.
- **Developed by**: Aman ([GitHub Profile](https://github.com/AP24110011314))
