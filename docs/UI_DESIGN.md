# UI_DESIGN — Design System & Layout

## 1. Principles
Calm, clinical-but-friendly · one clear primary action · plain language · never rely on colour alone · disclaimer always visible.

## 2. Page setup
```python
st.set_page_config(
    page_title="CardioLens",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)
```
Replace the current title `Heart Disease Prediction App by Aman☠️` with a heart icon title; move "by Aman" to the footer/About page.

## 3. Theme (`.streamlit/config.toml`)
```toml
[theme]
base = "light"
primaryColor = "#E5484D"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F4F6F8"
textColor = "#1F2328"
font = "sans serif"
```

## 4. Colour tokens
| Token | Hex | Use |
|---|---|---|
| Primary | #E5484D | buttons, accents |
| Low risk | #2BB673 | badge, gauge low band |
| Moderate | #F5A524 | badge, gauge mid band |
| High risk | #E5484D | badge, gauge high band |
| Surface | #F4F6F8 | cards |
| Muted text | #656D76 | captions, help |

Always pair colour with text ("Low risk") and an icon.

## 5. Layout (wide)
```
┌ Sidebar ─────┐ ┌ Main ───────────────────────────────────────────┐
│ ❤ CardioLens│ │ Title + one-line description + disclaimer banner│
│ • Predict    │ │ ┌ Form (60%) ───────────┐ ┌ Result (40%) ─────┐ │
│ • Batch      │ │ │ Personal              │ │ Gauge + badge     │ │
│ • Insights   │ │ │ Vitals                │ │ Summary sentence  │ │
│ • Model Info │ │ │ Cardiac tests         │ │ Top factors chart │ │
│ • About      │ │ │ [Predict risk]        │ │ Download PDF      │ │
│              │ │ └───────────────────────┘ └───────────────────┘ │
│ Dark/Light   │ │ Tabs: What-if | Similar patients | Compare      │
└──────────────┘ └─────────────────────────────────────────────────┘
```
On mobile Streamlit stacks columns: form first, result below. Use `st.columns([3,2], gap="large")`.

## 5.1 Components
- `st.form` + `st.form_submit_button("Predict risk", type="primary", use_container_width=True)`
- `st.container(border=True)` cards per input group
- `st.metric` for probability, band, "neighbours with disease"
- `st.tabs` for What-if / Similar patients / Compare
- `st.expander("What do these inputs mean?")`
- `st.toast` on success; `st.spinner` while predicting
- `st.dataframe(column_config=...)` with `ProgressColumn` for batch probabilities

## 6. Copy table (replace raw labels)
| Field | Label | Options / help |
|---|---|---|
| Sex | Sex | Male / Female |
| ChestPainType | Chest pain type | TA → Typical angina · ATA → Atypical angina · NAP → Non-anginal pain · ASY → No symptoms (asymptomatic) |
| RestingBP | Resting blood pressure (mm Hg) | "Systolic BP at rest" |
| Cholesterol | Serum cholesterol (mg/dL) | + checkbox "I don't know" |
| FastingBS | Fasting blood sugar | "≤ 120 mg/dL" / "> 120 mg/dL" |
| RestingECG | Resting ECG | Normal · ST-T wave abnormality · Left ventricular hypertrophy |
| MaxHR | Maximum heart rate (bpm) | "Highest rate reached during exercise test" |
| ExerciseAngina | Exercise-induced angina | No / Yes |
| Oldpeak | ST depression (mm) | "ST depression induced by exercise vs rest" |
| ST_Slope | ST slope | Upsloping · Flat · Downsloping |

Internal values (TA, ATA, 0/1…) stay in `src/config.py`; users only see labels.

## 7. Result copy
- Low: "Your inputs are similar to patients without heart disease in our reference data."
- Moderate: "Some inputs resemble patients with heart disease. Consider a routine check-up."
- High: "Your inputs resemble patients with heart disease. Please consult a doctor."
- Footer on every result: "This is an educational estimate, not a diagnosis."

## 8. Custom CSS (in `src/ui.py`, injected once)
- Card radius 12 px, 1 px border `#2A313C`, padding 1rem
- Hide Streamlit footer/menu only if desired (`#MainMenu`, `footer`)
- Badge pill: `padding: .25rem .75rem; border-radius: 999px; font-weight: 600`

## 9. Accessibility
Contrast ≥ 4.5:1 · text + icon with colour · keyboard-friendly form · tooltips for all medical terms · alt text/captions for charts.

## 10. Empty / error states
- Before first prediction: friendly placeholder with sample values button ("Try an example").
- Batch errors: table of row number + problem.
- Model load failure: clear message + link to troubleshooting in README.
