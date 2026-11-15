# PRD — CardioLens (Heart Disease Risk Prediction App)

## 1. Problem
The current app (`app.py`) takes 12 raw inputs on one long page, shows only a binary "likely / unlikely" message, gives no probability, no explanation, and uses cryptic labels (TA, ATA, NAP, ASY, "0/1"). Users cannot tell *how* risky a result is or *why*.

## 2. Goals
1. Clean, modern, trustworthy UI.
2. Show a **probability + risk band**, not just a label.
3. Explain results (key factors, what-if, similar cases).
4. Add useful extras: batch CSV, history, PDF report, model info.
5. Make the project portfolio-ready: tests, docs, deployed link.

## 3. Non-goals
- Medical diagnosis or treatment advice.
- User accounts / storing personal health data on a server.
- Retraining inside the app.

## 4. Users
| Persona | Need |
|---|---|
| Curious user | Quick, understandable risk estimate |
| Student / recruiter / reviewer | See a polished ML project with metrics and explainability |
| Clinician-style user (demo) | Batch-score many rows from a CSV |

## 5. User stories
- As a user, I enter my values with clear labels and tooltips so I don't need medical jargon.
- As a user, I see a risk % and band (Low/Moderate/High) with a short explanation.
- As a user, I change one input (what-if) and see how the risk moves.
- As a user, I download a PDF summary of my result.
- As a reviewer, I open Model Info and see accuracy, recall, ROC-AUC, confusion matrix and limitations.
- As a user, I upload a CSV and download predictions for every row.

## 6. Requirements
**P0 (must)**
- Redesigned input form (grouped, `st.form`, validated ranges)
- Probability via `predict_proba`, gauge, risk band
- Disclaimer visible on every result
- Pickle/version issue fixed (see `MODEL_NOTES.md`)
- Code refactor into `src/` modules, `requirements.txt`

**P1 (should)**
- Key-factor explanation + what-if
- Similar patients (KNN neighbours)
- Batch CSV prediction
- Model Info page
- Session history + CSV export

**P2 (nice)**
- PDF report
- Compare-to-population charts
- Multi-language labels, health-tips page
- Alternative models comparison (LogReg / RF / XGBoost) in Colab

## 7. Non-functional
- Prediction < 1 s; model loaded once (`st.cache_resource`)
- No personal data persisted or logged
- Works on mobile widths; WCAG-friendly contrast
- Reproducible install with pinned dependencies

## 8. Success metrics
- App deploys and runs without warnings
- 100% of inputs validated; invalid CSVs give clear errors
- Model Info shows metrics from the actual saved model
- README + docs complete; ≥ 10 unit tests pass

## 9. Risks
| Risk | Mitigation |
|---|---|
| Pickle built on sklearn 1.6.1, app runs 1.9.1 | Pin 1.6.1 or re-export model (`MODEL_NOTES.md`) |
| Encoding maps differ from training | Single source in `src/config.py`, test against Colab samples |
| Users treat output as diagnosis | Persistent disclaimer, careful copy |
| KNN probabilities are coarse | Explain in UI; consider calibrated model |

## 10. Milestones
1. Fix model + refactor → 2. New UI → 3. Explainability → 4. Batch/History/PDF → 5. Tests + deploy + README.
