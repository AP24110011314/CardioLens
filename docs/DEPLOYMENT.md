# DEPLOYMENT

## 1. Prepare
- `requirements.txt` with pinned versions, including `scikit-learn==1.6.1` (or the version used to re-export the model). Generate with `pip freeze`, then keep only direct dependencies, e.g.:
```
streamlit
pandas
numpy
scikit-learn==1.6.1
joblib
plotly
reportlab
```
(pin Streamlit and the others to the versions you tested locally.)
- Entry file `app.py` at repo root; model files committed (they are small).
- No secrets are needed; do not commit `.venv`.

## 2. Streamlit Community Cloud (recommended, free)
1. Push the repo to GitHub (public).
2. Go to share.streamlit.io → **Create app** → pick repo, branch, `app.py`.
3. In **Advanced settings**, choose a Python version that has wheels for your pinned scikit-learn (3.12 or 3.13).
4. Deploy; check logs for `InconsistentVersionWarning` (should be gone).
5. Copy the `*.streamlit.app` URL into the README.

## 3. Alternatives
- **Hugging Face Spaces** (Streamlit SDK): add `README.md` front-matter `sdk: streamlit`.
- **Render / Railway**: start command `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.
- **Docker** (optional): `FROM python:3.12-slim`, install requirements, `CMD ["streamlit","run","app.py","--server.port=8501","--server.address=0.0.0.0"]`.

## 4. Post-deploy checklist
- [ ] All pages load, form submits, batch upload works
- [ ] Mobile layout checked
- [ ] Disclaimer visible
- [ ] Repo has README, LICENSE, screenshots
- [ ] Reboot app after any model/dependency change

## 5. Troubleshooting
| Symptom | Fix |
|---|---|
| `InconsistentVersionWarning` | Match scikit-learn version to the pickle or re-export |
| `ModuleNotFoundError` on cloud | Add package to `requirements.txt` |
| Wrong predictions after refactor | Re-run golden tests; check encoding maps and column order |
| Slow first load | Ensure `@st.cache_resource` on model loading |
