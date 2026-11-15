# FEATURES — Specs & Acceptance Criteria

Priority: P0 must · P1 should · P2 nice.

## F1 — Redesigned input form (P0)
- Three grouped sections: **Personal** (age, sex), **Vitals** (resting BP, cholesterol, fasting sugar, max HR), **Cardiac tests** (chest pain type, resting ECG, exercise angina, ST depression, ST slope).
- Wrapped in `st.form` so the model is not re-run on every widget change.
- Friendly labels + `help=` tooltips (see `UI_DESIGN.md` copy table).
- Ranges follow the dataset: age 18–100 (dataset ~28–77), RestingBP up to 200, MaxHR up to ~202, Cholesterol up to ~603, Oldpeak roughly −2.6 to 6.2 (the current UI blocks negatives).
- **Cholesterol "I don't know" checkbox**: the dataset stores missing cholesterol as `0`; the app should impute the training median instead of sending a fake value.
- ✅ Done when: all 11 model inputs validated, no raw codes (TA/ASY/0/1) visible.

## F2 — Probability, gauge & risk band (P0)
- Use `model.predict_proba`; show % for the positive class.
- Plotly gauge + badge: Low < 30 %, Moderate 30–60 %, High > 60 % (app-defined bands, not clinical).
- Note under the gauge: KNN probabilities are coarse (fractions of k neighbours).
- ✅ Done when: result shows %, band, one-sentence summary, disclaimer.

## F3 — Key factors & what-if (P1)
- One-at-a-time sensitivity: for each input, replace with a reference "typical/healthy" value and record the change in probability → horizontal bar chart of top 5 factors.
- What-if panel: 3 sliders (e.g., MaxHR, Cholesterol, Oldpeak) re-score live and show Δ risk.
- ✅ Done when: factors sum to a sensible ranking, what-if updates under 1 s.

## F4 — Similar patients (P1)
- Use `model.kneighbors` on the scaled input; show the k nearest reference rows with their true outcome and distance.
- Needs `data/heart_reference.csv` exported from Colab (public dataset rows only).
- ✅ Done when: table shows k rows + "x of k had heart disease".

## F5 — Batch CSV prediction (P1)
- Upload CSV with the 11 columns (template download button).
- Validate columns, types, ranges; show row-level errors.
- Output table with probability + band; download as CSV; summary counts + histogram.
- ✅ Done when: 1,000-row file scores in a few seconds; bad files give clear messages.

## F6 — Session history (P1)
- `st.session_state` list of past predictions (timestamp, inputs, %, band).
- Trend line chart + "Clear history" + CSV export. Nothing stored server-side.

## F7 — PDF report (P2)
- ReportLab one-page report: inputs table, risk %, band, top factors, disclaimer, date.
- `st.download_button`.

## F8 — Compare with population (P2)
- Histograms/box plots of reference dataset with the user's value marked (age, MaxHR, cholesterol, Oldpeak) and split by outcome.

## F9 — Model Info page (P1)
- Reads `data/model_metrics.json` produced in Colab: accuracy, precision, recall, F1, ROC-AUC, confusion matrix, ROC curve image, class balance (508 positive / 410 negative in the dataset), training date, library versions.
- Limitations section (see `MODEL_NOTES.md`).

## F10 — About / Health info page (P2)
- Explains each input in plain language, general lifestyle information from reputable sources (link out; do not give medical advice), data credits.

## F11 — Theme & responsiveness (P0)
- `.streamlit/config.toml` theme, custom CSS in `src/ui.py`, works at ~360 px width.

## F12 — Robustness (P0)
- Models loaded with `@st.cache_resource`, errors shown with `st.error` (never raw stack traces).
- Unit tests for encoding, imputation, band thresholds, batch validation.

## Backlog ideas
Model comparison (LogReg/RF/XGBoost) · calibrated probabilities · SHAP for tree models · Hindi/Telugu UI labels · Docker image · API endpoint (FastAPI).
