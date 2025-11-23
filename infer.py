import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import json
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:16"


device = torch.device("cpu")

# Load category map
with open("category_map.json", "r") as f:
    category_map = json.load(f)

# Load tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained(
    "model/FinSenseAI_tokenizer",
    local_files_only=True
)

# Load model
model = DistilBertForSequenceClassification.from_pretrained(
    "model/FinSenseAI_model",
    low_cpu_mem_usage=True,
    dtype="auto",
    device_map=None
)
model.to(device)
model.eval()

# -------------------------
# RULE-BASED MERCHANT MAP
# -------------------------
MERCHANT_MAP = {
    "starbucks": "Food & Dining",
    "swiggy": "Food & Dining",
    "zomato": "Food & Dining",
    "kfc": "Food & Dining",
    "dominos": "Food & Dining",
    "pizza hut": "Food & Dining",

    "uber": "Transport",
    "ola": "Transport",
    "rapido": "Transport",

    "dmart": "Groceries",
    "bigbasket": "Groceries",
    "reliance fresh": "Groceries",

    "amazon": "Shopping",
    "flipkart": "Shopping",
    "myntra": "Shopping",
    "ajio": "Shopping",

    "airtel": "Bills & Utilities",
    "jio": "Bills & Utilities",
    "bsnl": "Bills & Utilities",
    "electricity": "Bills & Utilities",

    "icici": "Banking",
    "hdfc": "Banking",
    "sbi": "Banking",
    "axis": "Banking",
    "kotak": "Banking"
}

# -------------------------
# USER PREFERENCES LOADER
# -------------------------
def load_user_preferences():
    path = "user_preferences.json"

    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                prefs = json.load(f)
        except:
            prefs = {}
    else:
        prefs = {}

    # ensure required keys exist
    prefs.setdefault("merchant_rules", {})
    prefs.setdefault("keyword_rules", {})

    return prefs


# -------------------------
# APPLY USER PREFERENCES
# -------------------------
def apply_user_preferences(text, ai_category):
    prefs = load_user_preferences()

    text_lower = text.lower()

    merchant_rules = prefs.get("merchant_rules", {})
    keyword_rules  = prefs.get("keyword_rules", {})

    # Merchant rules
    for merchant, user_cat in merchant_rules.items():
        if merchant.lower() in text_lower:
            return user_cat, "rule"

    # Keyword rules
    for keyword, user_cat in keyword_rules.items():
        if keyword.lower() in text_lower:
            return user_cat, "rule"

    return ai_category, "ai"


# -------------------------
# AI MODEL PREDICTION
# -------------------------
def model_predict(text):
    text_lower = text.lower().strip()

    # Short input protection
    if len(text_lower) < 3:
        return {
            "category": "Other",
            "confidence": 0.20,
            "explanation": "Input too short."
        }

    # 1️⃣ Merchant Rule Match
    for merchant, cat in MERCHANT_MAP.items():
        if merchant in text_lower:
            return {
                "category": cat,
                "confidence": 0.99,
                "explanation": f"Matched merchant '{merchant}'."
            }

    # 2️⃣ Transformer model prediction
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=72
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)[0]
    idx = torch.argmax(probs).item()
    confidence = float(probs[idx])
    label = category_map[str(idx)]

    # Low confidence fallback
    if confidence < 0.60:
        return {
            "category": "Other",
            "confidence": confidence,
            "explanation": "Low confidence prediction."
        }

    keywords = " ".join([w for w in text_lower.split() if len(w) > 3])

    return {
        "category": label,
        "confidence": confidence,
        "explanation": f"Model identified keywords: '{keywords}'."
    }

# -------------------------
# FINAL HYBRID PREDICTOR
# -------------------------
def predict_category(text):
    ai_output = model_predict(text)
    ai_category = ai_output["category"]

    # Apply user preferences
    final_category, method = apply_user_preferences(text, ai_category)

    ai_output["category"] = final_category
    ai_output["explanation"] += f" (classified by {method})"

    return ai_output