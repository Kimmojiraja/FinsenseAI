# api.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import time
import os
import json
from typing import List

from fastapi.middleware.cors import CORSMiddleware


# import your existing predictor
from infer import predict_category

app = FastAPI(title="FinSenseAI API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


HISTORY_PATH = "history.csv"
FEEDBACK_PATH = "feedback.csv"
PREFS_PATH = "user_preferences.json"

# Ensure files exist
def ensure_csv(path, cols=None):
    if not os.path.exists(path):
        if cols:
            pd.DataFrame(columns=cols).to_csv(path, index=False)
        else:
            pd.DataFrame().to_csv(path, index=False)

ensure_csv(HISTORY_PATH, ["transaction","category","confidence","explanation","timestamp"])
ensure_csv(FEEDBACK_PATH, ["transaction","predicted_category","correct_category","confidence","feedback","timestamp"])
if not os.path.exists(PREFS_PATH):
    with open(PREFS_PATH, "w") as f:
        json.dump({"merchant_rules": {}, "keyword_rules": {}}, f)

# ---------- Pydantic models ----------
class PredictRequest(BaseModel):
    text: str

class BatchResult(BaseModel):
    transaction: str
    category: str
    confidence: float
    explanation: str

# ---------- Endpoints ----------
@app.get("/")
def root():
    return {"status": "OK", "service": "FinSenseAI API"}

@app.post("/predict")
def predict(req: PredictRequest):
    text = req.text or ""
    out = predict_category(text)
    # save to history
    row = {
        "transaction": text,
        "category": out.get("category","Unknown"),
        "confidence": float(out.get("confidence",0.0)),
        "explanation": out.get("explanation",""),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        hist = pd.read_csv(HISTORY_PATH)
        hist = pd.concat([hist, pd.DataFrame([row])], ignore_index=True)
    except Exception:
        hist = pd.DataFrame([row])
    hist.to_csv(HISTORY_PATH, index=False)
    return out

@app.post("/batch")
async def batch_upload(file: UploadFile = File(...)):
    # accept CSV, find a candidate text column, run predict_category for each row
    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="Only CSV supported")
    contents = await file.read()
    df = pd.read_csv(pd.io.common.BytesIO(contents))
    # find column
    col_candidates = [c for c in df.columns if any(k in c.lower() for k in ["trans","text","desc","merchant"])]
    chosen = col_candidates[0] if col_candidates else df.columns[0]
    results = []
    for _, row in df.iterrows():
        txt = str(row[chosen])
        out = predict_category(txt)
        results.append({
            "transaction": txt,
            "category": out.get("category","Unknown"),
            "confidence": float(out.get("confidence",0.0)),
            "explanation": out.get("explanation","")
        })
    # append to history
    try:
        hist = pd.read_csv(HISTORY_PATH)
        hist = pd.concat([hist, pd.DataFrame(results).assign(timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))], ignore_index=True)
    except Exception:
        hist = pd.DataFrame(results).assign(timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))
    hist.to_csv(HISTORY_PATH, index=False)
    # return sample + save csv
    pd.DataFrame(results).to_csv("batch_results.csv", index=False)
    return {"total": len(results), "sample": results[:10]}

@app.get("/history")
def get_history(limit: int = 200):
    try:
        df = pd.read_csv(HISTORY_PATH)
    except Exception:
        return {"history": []}
    df = df.sort_values("timestamp", ascending=False).head(limit)
    return {"history": df.to_dict(orient="records")}

@app.post("/feedback")
def post_feedback(payload: dict):
    # expects transaction, predicted_category, correct_category, confidence, feedback
    expected = {"transaction","predicted_category","correct_category","confidence","feedback"}
    if not expected.issubset(set(payload.keys())):
        raise HTTPException(status_code=400, detail="Missing fields")
    entry = {
        "transaction": payload["transaction"],
        "predicted_category": payload["predicted_category"],
        "correct_category": payload["correct_category"],
        "confidence": float(payload.get("confidence",0.0)),
        "feedback": payload["feedback"],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        fb = pd.read_csv(FEEDBACK_PATH)
        fb = pd.concat([fb, pd.DataFrame([entry])], ignore_index=True)
    except Exception:
        fb = pd.DataFrame([entry])
    fb.to_csv(FEEDBACK_PATH, index=False)
    return {"status":"ok"}

@app.get("/feedback")
def get_feedback(limit: int = 500):
    try:
        df = pd.read_csv(FEEDBACK_PATH)
    except Exception:
        return {"feedback": []}
    return {"feedback": df.sort_values("timestamp", ascending=False).head(limit).to_dict(orient="records")}

@app.get("/prefs")
def get_prefs():
    try:
        with open(PREFS_PATH, "r") as f:
            return json.load(f)
    except:
        return {"merchant_rules": {}, "keyword_rules": {}}

@app.post("/prefs")
def save_prefs(payload: dict):
    with open(PREFS_PATH, "w") as f:
        json.dump(payload, f, indent=2)
    return {"status":"ok"}

@app.get("/version")
def version():
    # optional: check version.json
    if os.path.exists("version.json"):
        with open("version.json","r") as f:
            return json.load(f)
    return {"version":"1.0.0", "model":"Unknown"}
