# TASKS — Implementation Checklist

Work top to bottom. Commit after each task. Read `AGENTS.md` first.

## Phase 0 — Stabilise (½ day)
- [x] Create a venv with Python 3.12/3.13; install `scikit-learn==1.6.1` (or re-export the model, `MODEL_NOTES.md` §5)
- [x] Print `model.feature_names_in_` and `scaler.feature_names_in_`; confirm whether BMI is used
- [x] Confirm encoding maps against the Colab notebook
- [ ] Export `heart_reference.csv` and `model_metrics.json` from Colab (user to provide; app degrades gracefully)
- [x] Create `requirements.txt` (`pip freeze` then trim) and `.gitignore` (`.venv`, `__pycache__`)
- [x] `git init`, first commit

## Phase 1 — Refactor
- [x] Create folders per `ARCHITECTURE.md`; move pickles to `models/`
- [x] `src/config.py` with features, ranges, encodings, risk bands
- [x] `src/model_loader.py` (cached), `src/preprocessing.py`, `src/predict.py`
- [x] Switch to `predict_proba`
- [x] Tests: encoding, imputation, band thresholds, golden rows from Colab

## Phase 2 — UI redesign (`UI_DESIGN.md`)
- [x] `.streamlit/config.toml` theme; `set_page_config`
- [x] `src/ui.py`: CSS, gauge, badge
- [x] Rebuild Predict page: grouped form in `st.form`, friendly labels, cholesterol "I don't know"
- [x] Result panel: gauge, band, summary, disclaimer
- [x] Sidebar navigation (`st.navigation` or `pages/`)
- [x] Remove the ☠️ from the title; add footer credit

## Phase 3 — Features (`FEATURES.md`)
- [x] F3 key factors + what-if
- [x] F4 similar patients
- [x] F5 batch CSV (+ template download)
- [x] F6 session history + export
- [x] F9 Model Info page
- [x] F7 PDF report
- [x] F8 compare with population
- [x] F10 About page

## Phase 4 — Quality
- [x] `AppTest` smoke test for every page
- [ ] Manual test at mobile width, dark and light themes
- [x] Run with `-W error::UserWarning` to confirm no sklearn warnings
- [x] Lint/format (ruff/black), type hints on `src/`

## Phase 5 — Ship
- [x] Finalise README with screenshots/GIF
- [ ] Push to GitHub, deploy (`DEPLOYMENT.md`)
- [ ] Add live link to README, resume and LinkedIn

## Definition of done
Deployed URL works · no warnings in logs · all tests pass · disclaimer on every result · docs match the code.
