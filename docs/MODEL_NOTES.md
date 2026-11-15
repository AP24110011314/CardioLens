# MODEL_NOTES

## 1. Artefacts
| File | Content |
|---|---|
| `KNN_heart.pkl` | `KNeighborsClassifier` |
| `scaler.pkl` | `StandardScaler` |
| `columns.pkl` | column list from training (currently not used by `app.py`) |

## 2. Dataset
- *Heart Failure Prediction Dataset* (fedesoriano, Kaggle, Sept 2021): 918 records after removing 272 duplicates from 1,190, merged from five datasets (Cleveland 303, Hungarian 294, Switzerland 123, Long Beach VA 200, Statlog 270).
- 11 features + target `HeartDisease` (1 = disease). Classes: 508 positive / 410 negative.
- Features: Age, Sex, ChestPainType (TA/ATA/NAP/ASY), RestingBP, Cholesterol, FastingBS, RestingECG (Normal/ST/LVH), MaxHR, ExerciseAngina, Oldpeak, ST_Slope (Up/Flat/Down).
- Citation: fedesoriano. (September 2021). *Heart Failure Prediction Dataset*. Kaggle.

## 3. Issues found in the current app (fix first)
1. **sklearn version mismatch** — terminal shows models pickled with scikit-learn **1.6.1** but loaded with **1.9.1** (`InconsistentVersionWarning`). Pickles are not guaranteed across versions. Fix: either
   - `pip install scikit-learn==1.6.1` (use Python 3.12/3.13 so a wheel exists), or
   - re-export from Colab with the version you deploy (preferred; see §5).
2. **BMI is probably unused.** The dataset has no BMI column; `app.py` builds BMI but then keeps only `model.feature_names_in_`. Run `print(model_columns, scaler_columns)`. If BMI isn't there, remove the slider or label it "informational only".
3. **Encodings must match training.** The app uses manual label-encoding maps; confirm they equal the Colab preprocessing (or ship a single Pipeline, §5).
4. **Cholesterol = 0 means missing** in this dataset (and one RestingBP = 0 row exists). Training should impute with the median of non-zero values; the app should offer "I don't know" and apply the same median.
5. **Input ranges** in the UI don't match the data (Oldpeak min 0.0 blocks negative values present in the data; Cholesterol 100–400 cuts off values up to ~600).
6. **Only a hard 0/1 label is shown.** Use `predict_proba`. Note: KNN probability = share of k neighbours in class 1 (with k=5 only 0, .2, .4, .6, .8, 1) — coarse and uncalibrated.

## 4. Evaluation to report on the Model Info page
Stratified train/test split + 5-fold CV; accuracy, precision, **recall** (missing a positive is costly), F1, ROC-AUC, confusion matrix, ROC curve. Compare KNN against Logistic Regression, Random Forest, and a gradient-boosted model; keep KNN only if it's competitive. Tune `n_neighbors`, `weights`, `metric` with GridSearchCV. Consider `CalibratedClassifierCV` for better probabilities.

## 5. Recommended Colab export (single Pipeline)
```python
import joblib, json, sklearn, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

df = pd.read_csv("heart.csv")
chol_med = df.loc[df.Cholesterol > 0, "Cholesterol"].median()
df["Cholesterol"] = df["Cholesterol"].replace(0, chol_med)
df = df[df.RestingBP > 0]

X, y = df.drop(columns="HeartDisease"), df["HeartDisease"]
num = ["Age","RestingBP","Cholesterol","MaxHR","Oldpeak"]
cat = ["Sex","ChestPainType","FastingBS","RestingECG","ExerciseAngina","ST_Slope"]
pre = ColumnTransformer([("num", StandardScaler(), num),
                         ("cat", OneHotEncoder(handle_unknown="ignore"), cat)])
pipe = Pipeline([("pre", pre), ("clf", KNeighborsClassifier(n_neighbors=7, weights="distance"))])

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
pipe.fit(Xtr, ytr)
proba = pipe.predict_proba(Xte)[:, 1]

joblib.dump(pipe, "heart_pipeline.pkl")
df.to_csv("heart_reference.csv", index=False)
json.dump({"sklearn": sklearn.__version__, "chol_median": float(chol_med),
           "roc_auc": float(roc_auc_score(yte, proba)),
           "report": classification_report(yte, pipe.predict(Xte), output_dict=True),
           "confusion_matrix": confusion_matrix(yte, pipe.predict(Xte)).tolist()},
          open("model_metrics.json", "w"), indent=2)
```
With a Pipeline the app just passes a raw-valued DataFrame (strings included) — no manual encoding or scaling, so the encoding-mismatch bug disappears. Update `preprocessing.py` accordingly.

## 6. Limitations (show in UI)
- Small, older, merged dataset (918 rows); sources used different diagnostic practices.
- Only 11 features; no family history, smoking, lipids breakdown, etc.
- Not validated clinically; may be biased by sex/age distribution of the data.
- Output is a statistical resemblance to dataset patients, not a diagnosis.
