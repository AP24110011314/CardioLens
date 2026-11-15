# ARCHITECTURE

## 1. Target structure
```
HeartDisease/
├── app.py                    # entry point: page config, st.navigation
├── pages/
│   ├── 1_Predict.py          # form + result + what-if/similar/compare tabs
│   ├── 2_Batch_Prediction.py
│   ├── 3_Insights.py         # dataset charts, history
│   ├── 4_Model_Info.py
│   └── 5_About.py
├── src/
│   ├── config.py             # feature specs, ranges, labels, encoding maps, risk bands
│   ├── model_loader.py       # cached load of model/scaler/columns
│   ├── preprocessing.py      # build_frame(), impute, encode, scale
│   ├── predict.py            # predict_proba, risk_band
│   ├── explain.py            # sensitivity, what_if, neighbours
│   ├── report.py             # PDF generation
│   └── ui.py                 # CSS, gauge, badge, reusable components
├── models/                   # KNN_heart.pkl, scaler.pkl, columns.pkl
├── data/                     # heart_reference.csv, model_metrics.json, roc.png
├── assets/                   # logo, icons
├── tests/                    # test_preprocessing.py, test_predict.py, test_batch.py
├── .streamlit/config.toml
├── requirements.txt
└── *.md docs
```
Move the `.pkl` files into `models/` and update paths in `model_loader.py`.

## 2. Data flow
```
Form / CSV → build_frame() → impute (cholesterol 0 → median)
          → encode categoricals (config maps)
          → select model_columns (training order)
          → scaler.transform(scaler_columns)
          → model.predict_proba → risk_band → UI
                                 ↘ explain.* (sensitivity, neighbours)
```
This mirrors the current `app.py` logic (build DataFrame → keep `model.feature_names_in_` → scale `scaler.feature_names_in_` → predict) but split into testable functions.

## 3. Module contracts
```python
# src/config.py
FEATURES: dict            # name -> {label, type, min, max, default, help, options}
ENCODINGS: dict           # Sex, ChestPainType, RestingECG, ST_Slope, ExerciseAngina, FastingBS maps
RISK_BANDS = [(0.30,"Low"), (0.60,"Moderate"), (1.01,"High")]

# src/model_loader.py
@st.cache_resource
def load_artifacts() -> tuple[model, scaler, list[str], list[str]]: ...

# src/preprocessing.py
def build_frame(inputs: dict | pd.DataFrame) -> pd.DataFrame: ...
def prepare(df, model_columns, scaler, scaler_columns) -> pd.DataFrame: ...

# src/predict.py
def predict(inputs) -> dict   # {"proba": float, "label": int, "band": str}

# src/explain.py
def sensitivity(inputs, reference: dict) -> pd.DataFrame
def neighbours(inputs, k=5) -> pd.DataFrame
```

## 4. Encoding maps (must equal training)
Current app mapping: Sex Male=1/Female=0 · ChestPainType TA0, ATA1, NAP2, ASY3 · RestingECG LVH0, Normal1, ST2 · ST_Slope Down0, Flat1, Up2 · ExerciseAngina Yes1/No0. **Verify these against the Colab notebook** before trusting predictions; keep them only in `config.py`.

## 5. Caching & state
- `@st.cache_resource` for model artefacts
- `@st.cache_data` for reference dataset and metrics
- `st.session_state["history"]` for prediction history; `st.session_state["last_inputs"]` for what-if

## 6. Error handling
- Missing files → friendly error + stop
- Input outside range → blocked by widget limits and re-validated in `build_frame`
- CSV problems → collected into a list and shown in a table

## 7. Testing strategy
- Unit: encoding, imputation, band thresholds, column order
- Golden test: 5–10 rows from Colab with known model outputs must match the app output
- Smoke: `streamlit.testing.v1.AppTest` loads each page without exceptions

## 8. Security & privacy
No database, no logging of inputs, no external calls; history lives in the browser session only.
