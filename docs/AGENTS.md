# AGENTS.md — Instructions for Claude Code / OpenCode

(Copy this file to `CLAUDE.md` if your agent expects that name.)

## Project
CardioLens: Streamlit app predicting heart disease risk from 11 clinical inputs using a pickled scikit-learn KNN model. Educational only.

## Read first
`PRD.md` → `ARCHITECTURE.md` → `UI_DESIGN.md` → `FEATURES.md` → `MODEL_NOTES.md` → work through `TASKS.md` in order.

## Commands
```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
pytest -q
ruff check . && ruff format .
```

## Rules
1. Do not retrain, edit or overwrite files in `models/`. Fixes to the model happen in Colab.
2. Encoding maps, ranges, labels and risk bands live **only** in `src/config.py`.
3. Keep column order identical to `model.feature_names_in_`; never reorder by hand.
4. Use `@st.cache_resource` for models and `@st.cache_data` for data.
5. Use `st.form` for the main input form.
6. Never store or log user health inputs; history is `st.session_state` only.
7. Every result view shows the disclaimer: "Educational estimate, not a diagnosis."
8. Never display raw codes (TA, ASY, 0/1) to users — use the labels in `UI_DESIGN.md`.
9. Show errors with `st.error`, not stack traces.
10. Add type hints and a test for each new function in `src/`.
11. Small commits with clear messages; one task from `TASKS.md` per commit.
12. If a doc and the code disagree, ask the user or update the doc in the same commit.

## Definition of done (per task)
Code runs · tests pass · no new warnings · UI matches `UI_DESIGN.md` · checkbox ticked in `TASKS.md`.
