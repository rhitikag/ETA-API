
import pickle
import json
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

# -------------------------
# Load artifacts at startup
# -------------------------
with open("lgb_models_folds.pkl", "rb") as f:
    models = pickle.load(f)

with open("features_list.pkl", "rb") as f:
    FEATURES = pickle.load(f)

CATEGORICAL_COLS = ["vendor_id"]  # keep in sync with training


# -------------------------
# Utils
# -------------------------
def prepare_dataframe(data: dict) -> pd.DataFrame:
    """
    Convert input dict -> DataFrame
    Enforce column order + categorical dtypes
    """
    df = pd.DataFrame([data], columns=FEATURES)

    # Restore categorical dtype(s)
    for col in CATEGORICAL_COLS:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df


# -------------------------
# Health check
# -------------------------
@app.get("/")
def health():
    return {"status": "ok"}


# -------------------------
# Predict via raw JSON body
# -------------------------
@app.post("/predict")
def predict(data: dict):
    try:
        df = prepare_dataframe(data)
        preds = models[0].predict(df)
        return {"prediction": float(preds[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# Predict via uploaded JSON file
# -------------------------
@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="Only .json files are supported")

        contents = await file.read()
        data = json.loads(contents)

        df = prepare_dataframe(data)
        preds = models[0].predict(df)

        return {
            "filename": file.filename,
            "prediction": float(preds[0])
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
