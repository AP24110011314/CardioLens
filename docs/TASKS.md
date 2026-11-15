# TASKS — Implementation Checklist

Work top to bottom. Commit after each task. Read `AGENTS.md` first.

## Phase 0 — Stabilise (½ day)
- [ ] Create a venv with Python 3.12/3.13; install `scikit-learn==1.6.1` (or re-export the model, `MODEL_NOTES.md` §5)
- [ ] Print `model.feature_names_in_` and `scaler.feature_names_in_`; confirm whether BMI is used
- [ ] Confirm encoding maps against the Colab notebook
- [ ] Export `heart_reference.csv` and `model_metrics.json` from Colab
- [ ] Create `requirements.txt` (`pip freeze` then trim) and `.gitignore` (`.venv`, `__pycache__`)
- [ ] `git init`, first commit

## Phase 1 — Refactor
- [ ] Create folders per `ARCHITECTURE.md`; move pickles to `models/`
- [ ] `src/config.py` with features, ranges, encodings, risk bands
- [ ] `src/model_loader.py` (cached), `src/preprocessing.py`, `src/predict.py`
- [ ] Switch to `predict_proba`
- [ ] Tests: encoding, imputation, band thresholds, golden rows from Colab

## Phase 2 — UI redesign (`UI_DESIGN.md`)
- [ ] `.streamlit/config.toml` theme; `set_page_config`
- [ ] `src/ui.py`: CSS, gauge, badge
- [ ] Rebuild Predict page: grouped form in `st.form`, friendly labels, cholesterol "I don't know"
- [ ] Result panel: gauge, band, summary, disclaimer
- [ ] Sidebar navigation (`st.navigation` or `pages/`)
- [ ] Remove the ☠️ from the title; add footer credit

## Phase 3 — Features (`FEATURES.md`)
- [ ] F3 key factors + what-if
- [ ] F4 similar patients
- [ ] F5 batch CSV (+ template download)
- [ ] F6 session history + export
- [ ] F9 Model Info page
- [ ] F7 PDF report
- [ ] F8 compare with population
- [ ] F10 About page

## Phase 4 — Quality
- [ ] `AppTest` smoke test for every page
- [ ] Manual test at mobile width, dark and light themes
- [ ] Run with `-W error::UserWarning` to confirm no sklearn warnings
- [ ] Lint/format (ruff/black), type hints on `src/`

## Phase 5 — Ship
- [ ] Finalise README with screenshots/GIF
- [ ] Push to GitHub, deploy (`DEPLOYMENT.md`)
- [ ] Add live link to README, resume and LinkedIn

## Definition of done
Deployed URL works · no warnings in logs · all tests pass · disclaimer on every result · docs match the code.
