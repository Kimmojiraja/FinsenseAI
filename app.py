# app.py
import streamlit as st
import pandas as pd
import time
import json
import os
import plotly.express as px
from infer import predict_category  



def load_changelog():
    if os.path.exists("changelog.json"):
        with open("changelog.json", "r") as f:
            return json.load(f)
    return []

# Load version info
def load_version():
    if os.path.exists("version.json"):
        with open("version.json", "r") as f:
            return json.load(f)
    return {}
    
VERSION = load_version()


import base64

def load_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None


# -------------------------
# Page config
# -------------------------

st.set_page_config( page_title="FinSenseAI", layout="wide", page_icon="💳" )


MODERN_DARK_CSS = """
<style>

/* ===== GLOBAL ===== */
html, body, .stApp {
    background-color: #0D0F12 !important;
    color: #E5E7EB !important;
    font-family: 'Inter', sans-serif;
}

/* Prevent global override mistakes */
* {
    color: inherit !important;
}

/* ===== HEADERS ===== */
h1, h2, h3, h4 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* ===== TEXT ===== */
p, label, span, div, .stMarkdown {
    color: #E5E7EB !important;
}

/* ===== INPUTS ===== */
input, textarea {
    background-color: #1E293B !important;
    color: #F3F4F6 !important;
    border-radius: 10px !important;
    border: 1px solid #374151 !important;
}

input::placeholder,
textarea::placeholder {
    color: #9CA3AF !important;
}

input:focus {
    border: 1px solid #60A5FA !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,0.3) !important;
}

/* ===== SELECTBOX ===== */
.stSelectbox > div > div {
    background-color: #1E293B !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    color: #E5E7EB !important;
}
.stSelectbox svg { color: #E5E7EB !important; }

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(90deg, #2563EB, #1D4ED8) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 12px 20px !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #1D4ED8, #1E40AF) !important;
    transform: translateY(-2px);
}

/* ===== CARDS ===== */
.result-card, .card {
    background: #111827 !important;
    border: 1px solid #1F2937 !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1F2937 !important;
}
section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

/* ===== FILE UPLOADER FIX ===== */
.stFileUploader {
    background-color: #1E293B !important;
    border: 1px dashed #475569 !important;
    border-radius: 10px !important;
}
.stFileUploader label, .uploadedFile {
    color: #E5E7EB !important;
}

/* ===== CODE BLOCK FIX ===== */
pre, code, .stCodeBlock {
    background-color: #111827 !important;
    color: #E5E7EB !important;
    border-radius: 8px !important;
    padding: 15px !important;
    border: 1px solid #1F2937 !important;
}

/* ===== EXPANDER ===== */
.stExpander, .st-expanderHeader, .stExpanderHeader {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
}
/* ----------------------------------------------------
   FIX: Buttons inside forms (Add Rule, Add Keyword Rule)
   ---------------------------------------------------- */
div.stButton > button,
button[kind="secondary"], .stForm button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 22px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}

div.stButton > button:hover,
button[kind="secondary"]:hover, 
.stForm button:hover {
    background: linear-gradient(135deg, #1e40af, #1d4ed8) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.55) !important;
}

<style>

 /* SELECTBOX MAIN */ 
div[data-baseweb="select"] {
    background-color: #1F2937 !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] * {
    color: #F8FAFC !important;
}

div[data-baseweb="select"] svg {
    fill: #F8FAFC !important;
}

/* SELECTBOX MENU */
ul[role="listbox"] {
    background: #111827 !important;
    border: 1px solid #374151 !important;
}

ul[role="listbox"] li {
    color: #F1F5F9 !important;
}

ul[role="listbox"] li:hover {
    background: #1E293B !important;
}

</style>
<style>

 /* FILE UPLOADER WRAPPER */
div[data-testid="stFileUploader"] {
    background-color: #1F2937 !important;
    border: 1px dashed #4B5563 !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* ICON */
div[data-testid="stFileUploader"] svg {
    fill: #E5E7EB !important;
}

/* TEXT */
div[data-testid="stFileUploader"] * {
    color: #F1F5F9 !important;
}

/* DRAG AREA */
.stFileUploader > section {
    background-color: #111827 !important;
    border-radius: 10px !important;
}

</style>
</style>
"""
st.markdown("""
<style>
/* ===========================
   ULTIMATE DARK THEME OVERRIDE
   Paste THIS at the very end
   =========================== */

/* force the whole app to inherit dark colors (safe) */
html, body, .stApp, section[data-testid="stSidebar"] {
    background: #0D0F12 !important;
    color: #E5E7EB !important;
}

/* Remove any translucent white layer from BaseWeb layer/popover */
div[data-baseweb="layer"],
div[data-baseweb="popover"],
div[data-baseweb="menu"],
div[data-baseweb="menu"] > div,
div[data-baseweb="menu"] > ul,
div[role="presentation"],
div[role="presentation"] > div {
    background: #111827 !important;
    color: #F8FAFC !important;
    border: 1px solid #374151 !important;
    box-shadow: none !important;
    -webkit-box-shadow: none !important;
    opacity: 1 !important;
}

/* Dropdown panel large white rectangle (virtual list containers used by rc-virtual-list) */
.rc-virtual-list-holder,
.rc-virtual-list-holder-inner,
div[role="listbox"],
ul[role="listbox"],
div[role="presentation"] ul,
div[role="presentation"] li {
    background: #111827 !important;
    color: #F8FAFC !important;
    opacity: 1 !important;
}

/* Menu items */
div[data-baseweb="menu-item"],
div[data-baseweb="menu-item"] * ,
div[role="option"],
div[role="option"] * {
    background: transparent !important;
    color: #F1F5F9 !important;
    opacity: 1 !important;
}

/* Hover / selected states */
div[data-baseweb="menu-item"]:hover,
div[role="option"]:hover,
li[role="option"]:hover {
    background: #1E293B !important;
    color: #FFFFFF !important;
}
div[data-baseweb="menu-item"][aria-selected="true"],
div[role="option"][aria-selected="true"],
li[role="option"][aria-selected="true"] {
    background: #1E40AF !important;
    color: #FFFFFF !important;
}

/* override any backdrop/overlay used by popovers */
div[role="presentation"][style*="background"],
div[data-testid="stModalBackdrop"],
div[aria-hidden="true"][style*="opacity"] {
    background: transparent !important;
    opacity: 1 !important;
}

/* ensure scrollbars match theme */
div[data-baseweb="menu"]::-webkit-scrollbar,
div[role="listbox"]::-webkit-scrollbar,
.rc-virtual-list-holder::-webkit-scrollbar {
    width: 10px !important;
    height: 10px !important;
}
div[data-baseweb="menu"]::-webkit-scrollbar-thumb,
div[role="listbox"]::-webkit-scrollbar-thumb,
.rc-virtual-list-holder::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
}

/* final safety: make all children inherit the menu bg so nothing shows white */
div[data-baseweb="menu"] * ,
div[data-baseweb="popover"] * ,
div[data-baseweb="layer"] * ,
div[role="presentation"] * {
    background-color: #111827 !important;
    color: #F8FAFC !important;
}

/* small tweak: make sure the closed selectbox (input area) stays dark */
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] input {
    background: #1F2937 !important;
    color: #F1F5F9 !important;
}

/* Prevent Streamlit from reapplying certain default inline styles */
*[style*="background: white"] {
    background: transparent !important;
}
*[style*="background:#fff"] {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

 /* Fix for JSON / code blocks (st.code, st.json, st.expander internal) */
div[data-testid="stCodeBlock"],
div[data-testid="stCodeBlock"] pre,
div[data-testid="stCodeBlock"] code,
.stCodeBlock,
.stCodeBlock pre,
.stCodeBlock code,
pre, code {
    background-color: #111827 !important;
    color: #E5E7EB !important;
    border: 1px solid #1F2937 !important;
    border-radius: 10px !important;
}

/* Fix for the white background wrapper around code/json */
.element-container, 
.element-container *[style*="background"],
.block-container *[style*="background:white"],
*[style*="background: rgb(255, 255, 255)"] {
    background-color: #111827 !important;
    color: #E5E7EB !important;
}

/* Hide the default white box-shadow around code blocks */
div[data-testid="stCodeBlock"] {
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)

# Paste this at the end of your Streamlit app (replace prior CSS blocks)
import streamlit as st

FINTECH_CSS = r"""
<style>
:root{
  --bg:#0b0d0f;
  --panel:#0f1720;
  --panel-2:#111827;
  --muted:#9aa4b2;
  --accent-1: linear-gradient(90deg,#2563eb,#7c3aed);
  --accent-2: linear-gradient(90deg,#1d4ed8,#06b6d4);
  --glass: rgba(255,255,255,0.03);
  --card-shadow: 0 10px 30px rgba(2,6,23,0.6);
}

/* ===== GLOBAL ===== */
html, body, .stApp {
  background: var(--bg) !important;
  color: #E6EEF8 !important;
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  -webkit-font-smoothing:antialiased;
}

/* Smooth transitions */
* { transition: all .18s cubic-bezier(.2,.8,.2,1) !important; }

/* ===== HERO / PAGE BANNER ===== */
.app-hero {
  display:block;
  margin: 18px auto 30px;
  padding: 28px;
  border-radius: 12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  box-shadow: 0 6px 30px rgba(2,6,23,0.55);
  border: 1px solid rgba(255,255,255,0.03);
  position: relative;
  overflow: hidden;
}

/* hero accent image */
.app-hero .hero-accent {
  position: absolute;
  right: 22px;
  top: 10px;
  width: 240px;
  height: 120px;
  background: url('/mnt/data/Screenshot 2025-11-23 183328.png') center/cover no-repeat;
  opacity: 0.12;
  filter: saturate(.8) blur(0.6px);
  transform: translateZ(0);
  pointer-events:none;
}

/* hero content */
.app-hero h1 {
  font-size: 36px;
  margin: 0 0 6px 0;
  letter-spacing: -0.5px;
  color: #FFFFFF;
}
.app-hero p.lead {
  margin:0;
  color: var(--muted);
  font-size: 15px;
}

/* ===== SIDEBAR POLISH ===== */
section[data-testid="stSidebar"] {
  background: #0f1724 !important;
  border-right: 1px solid rgba(255,255,255,0.03);
}
section[data-testid="stSidebar"] .css-1d391kg { color: #E6EEF8 !important; }

/* sidebar links - highlight current */
.stSidebar [role="list"] li {
  border-radius: 999px;
}
.stSidebar .css-1avcm0n > div[role="button"][aria-pressed="true"] {
  background: linear-gradient(90deg,#0f3bff22,#7c3aed22) !important;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02), 0 6px 18px rgba(2,6,23,0.45);
}

/* ===== CARDS ===== */
.card-pro {
  background: linear-gradient(180deg, rgba(16,22,30,0.86), rgba(11,14,18,0.9));
  border-radius: 12px;
  padding: 18px;
  border: 1px solid rgba(255,255,255,0.03);
  box-shadow: var(--card-shadow);
}

/* feature cards row */
.features {
  display:flex;
  gap: 18px;
  align-items: stretch;
}
.feature {
  flex:1;
  padding:14px;
  border-radius:10px;
  background: linear-gradient(180deg, rgba(18,26,36,0.6), rgba(14,18,24,0.6));
  border: 1px solid rgba(255,255,255,0.02);
}

/* ===== BUTTONS ===== */
.stButton>button, .stButton>button:focus {
  background: linear-gradient(90deg,#2563eb,#7c3aed) !important;
  color: #fff !important;
  font-weight:600;
  border-radius: 14px !important;
  padding: 12px 20px !important;
  box-shadow: 0 10px 30px rgba(37,99,235,0.16);
  border: none !important;
}
.stButton>button:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 36px rgba(37,99,235,0.22);
}

/* subtle ghost button */
.btn-ghost {
  background: transparent !important;
  border: 1px solid rgba(255,255,255,0.04) !important;
  color: var(--muted) !important;
}

/* ===== INPUTS / SELECTS ===== */
input, textarea, .stTextInput > div > input, .stTextArea > div > textarea {
  background: rgba(255,255,255,0.02) !important;
  border: 1px solid rgba(255,255,255,0.04) !important;
  padding: 12px !important;
  border-radius: 10px !important;
  color: #E6EEF8 !important;
}

/* Baseweb select / popover + virtual list + rc-virtual-list overrides */
div[data-baseweb="select"],
div[data-baseweb="menu"],
div[data-baseweb="menu"] *,
div[data-baseweb="popover"],
div[data-baseweb="layer"],
.rc-virtual-list-holder,
.rc-virtual-list-holder-inner {
  background: #0f1720 !important;
  color: #E6EEF8 !important;
  border: 1px solid rgba(255,255,255,0.03) !important;
  box-shadow: none !important;
}
div[data-baseweb="menu-item"]:hover,
li[role="option"]:hover {
  background: rgba(37,99,235,0.12) !important;
  color: #fff !important;
}

/* ===== CODE / JSON BLOCKS ===== */
div[data-testid="stCodeBlock"],
.stCodeBlock, pre, code {
  background: #0b1220 !important;
  color: #DDEBF9 !important;
  padding: 16px !important;
  border-radius: 10px !important;
  border: 1px solid rgba(255,255,255,0.03) !important;
}

/* ===== SECTION TITLES ===== */
.section-title {
  display:flex;
  align-items:center;
  gap:14px;
  background: linear-gradient(90deg, rgba(16,25,37,0.6), rgba(12,20,30,0.6));
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 12px;
  border: 1px solid rgba(255,255,255,0.02);
}
.section-title h2 {
  margin:0; font-size:20px; color: #fff;
}

/* ===== SMALL UI TWEAKS ===== */
hr { border: none; height: 1px; background: rgba(255,255,255,0.03); margin: 18px 0; }
a { color: #9ec6ff !important; text-decoration: none; }
a:hover { text-decoration: underline; }

/* ===== SCROLLBAR ===== */
*::-webkit-scrollbar { width: 9px; height:9px; }
*::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.06); border-radius: 8px; }

/* ===== SUBTLE ANIMATIONS (feel: subtle) ===== */
.card-pro, .feature, .app-hero { transition: transform .28s cubic-bezier(.2,.9,.2,1), box-shadow .28s; }
.card-pro:hover, .feature:hover { transform: translateY(-6px); box-shadow: 0 22px 40px rgba(3,10,30,0.6); }

/* final safety overrides (stop inline white) */
*[style*="background: white"], *[style*="background:#fff"], *[style*="background: rgb(255, 255, 255)"] {
  background: transparent !important;
  color: inherit !important;
}
</style>
"""

st.markdown(FINTECH_CSS, unsafe_allow_html=True)

# ---- Optional: Hero / Homepage block (paste into your homepage layout) ----
HOMEPAGE_HTML = r"""
<div class="app-hero">
  <div style="display:flex; gap:18px; align-items:center;">
    <div style="flex:1;">
      <h1>FinSenseAI — Sense for every spend</h1>
      <p class="lead">Smart transaction categorization, personalized rules, and powerful analytics — now with a modern fintech UI.</p>
      <div style="margin-top:12px;">
        <button class="stButton"><span>Get started</span></button>
        <button class="stButton btn-ghost" style="margin-left:10px">Learn more</button>
      </div>
    </div>
    <div class="hero-accent"></div>
  </div>
</div>
"""

st.markdown(MODERN_DARK_CSS, unsafe_allow_html=True)


# -------------------------
# Helpers
# -------------------------
def confidence_badge_html(conf):
    color = "#10B981" if conf >= 0.85 else ("#F59E0B" if conf >= 0.6 else "#EF4444")
    return f"<span style='background:{color}; color:white; padding:6px 10px; border-radius:10px; font-weight:600'>{conf:.4f}</span>"

def explanation_snippet(txt, max_len=120):
    if not isinstance(txt, str):
        return ""
    if len(txt) <= max_len:
        return txt
    return txt[:max_len].rsplit(" ", 1)[0] + "..."

def ensure_file(path, cols=None):
    """Ensure CSV exists with optional columns."""
    if os.path.exists(path):
        return
    if cols is None:
        pd.DataFrame().to_csv(path, index=False)
    else:
        pd.DataFrame(columns=cols).to_csv(path, index=False)

# Ensure storage files exist
ensure_file("history.csv", cols=["transaction","category","confidence","explanation","timestamp"])
ensure_file("feedback.csv", cols=["transaction","predicted_category","correct_category","confidence","feedback","timestamp"])

# -------------------------
# Base CSS + dark-mode and plotly fixes
# -------------------------
BASE_CSS = """
<style>
/* small input styling */
div.stButton > button { height:44px; border-radius:8px; font-weight:600; }

/* result card */
.result-card {
  animation: fadeIn 0.45s ease-in-out;
  padding: 18px;
  border-radius: 12px;
  background: #fbfcfe;
  border: 1px solid #e6eef9;
}
@keyframes fadeIn { from {opacity: 0; transform: translateY(6px);} to{opacity:1; transform: translateY(0);} }

/* small placeholder color */
input::placeholder { color:#94a3b8 !important; }

/* light-mode plotly background */
.plotly-graph-div, .plot-container, .svg-container { background-color: white !important; }

</style>
"""
st.markdown(BASE_CSS, unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.image("logo.png", width=120)
    st.markdown("<h2 style='color:#F0F6FC; margin-top:10px;'>FinSenseAI</h2>", unsafe_allow_html=True)

    page = st.radio("Navigation", 
        ["Home", "Bulk Upload", "Analytics", "Smart Insights", "Feedback Analytics", "User Preferences", "Changelog", "About"]
    )

    st.markdown("---")
    st.markdown(f"**Version:** {VERSION.get('version', '1.0.0')}")
    st.markdown(f"**Model:** {VERSION.get('model', 'Unknown')}")

    st.markdown("---")
    st.markdown("Team: **Kimmoji Raja**")


        # --- Version Display ---
    try:
        version_data = load_version()   # loaded earlier at top of file
        ver = version_data.get("version", "1.0.0")
        last_update = version_data.get("last_updated", "N/A")
    except:
        ver = "1.0.0"
        last_update = "N/A"

    st.markdown(f"**Version:** `{ver}`")
    st.markdown(f"<span style='font-size:12px;color:gray;'>Updated: {last_update}</span>", unsafe_allow_html=True)
    st.markdown("---")


    st.markdown("**GitHub:** [Repo link](#)")  # replace with real repo URL
    st.markdown("---")
    # ---- VERSION INFO SECTION ----
    st.markdown("### 🔖 Version Info")
    st.markdown(f"**App Version:** {VERSION.get('app_version', 'N/A')}")
    st.markdown(f"**Model Version:** {VERSION.get('model_version', 'N/A')}")
    st.markdown(f"**Dataset Version:** {VERSION.get('dataset_version', 'N/A')}")
    st.markdown(f"**Rule Engine:** {VERSION.get('rule_engine_version', 'N/A')}")
    st.markdown(f"**Last Updated:** {VERSION.get('last_updated', 'N/A')}")





# -------------------------
# Top header (logo + title)
# -------------------------
def render_header(title="FinSenseAI", subtitle="Sense For Every Spend."):
    st.markdown(f"""
    <div style='padding:12px 0 25px 0;'>
        <h1 style='margin-bottom:4px; font-size:32px; font-weight:700; color:#F0F6FC;'>{title}</h1>
        <span style='color:#8B949E; font-size:16px;'>{subtitle}</span>
    </div>
    """, unsafe_allow_html=True)


# -------------------------
# HOME PAGE
# -------------------------
if page == "Home":
    left_col, right_col = st.columns([2, 1])

    # =====================================
    # LEFT COLUMN
    # =====================================
    with left_col:

        # ---------------- CARD: HEADER + INPUT ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        render_header()
        st.markdown("---")

        tx_input = st.text_input(
            "Enter a transaction:",
            placeholder="e.g., Starbucks Coffee 350 INR"
        )

        st.write("")

        if st.button("Categorize", use_container_width=True):

            if not tx_input.strip():
                st.warning("Please enter a transaction string.")
            else:
                with st.spinner("Analyzing transaction with the model..."):
                    try:
                        result = predict_category(tx_input)
                    except Exception as e:
                        st.error(f"Model inference error: {e}")
                        result = {
                            "category": "Unknown",
                            "confidence": 0.0,
                            "explanation": "Inference failed."
                        }
                    time.sleep(0.4)

                # store session
                st.session_state["tx_input"] = tx_input
                st.session_state["result"] = result

                st.success("Prediction Complete ✓")

        st.markdown('</div>', unsafe_allow_html=True)
        # -------- END INPUT CARD --------


        # =========================================
        # RESULT + EXPLANATION CARD
        # =========================================
        if "result" in st.session_state:
            result = st.session_state["result"]

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(f"### 🏷 Category: **{result.get('category','Unknown')}**")

            st.markdown(
                f"### 📊 Confidence: "
                f"{confidence_badge_html(float(result.get('confidence',0.0)))}",
                unsafe_allow_html=True
            )

            st.markdown(
                f"### 🔍 Explanation:<br>"
                f"<span style='color:#64748B'>{explanation_snippet(result.get('explanation',''))}</span>",
                unsafe_allow_html=True
            )

            # Model version footer inside card
            st.markdown(
                f"<div style='font-size:12px; color:#94A3B8; margin-top:10px;'>"
                f"Model: {VERSION.get('model_version','N/A')} • "
                f"Dataset: {VERSION.get('dataset_version','N/A')}"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)
            # -------- END RESULT CARD --------


            # =========================================
            # FEEDBACK CARD
            # =========================================
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown("### 📝 Was this prediction correct?")

            c1, c2 = st.columns(2)

            # ---------- YES ----------
            with c1:
                if st.button("👍 Yes"):
                    fb = {
                        "transaction": tx_input,
                        "predicted_category": result.get("category", "Unknown"),
                        "correct_category": result.get("category", "Unknown"),
                        "confidence": float(result.get("confidence", 0.0)),
                        "feedback": "yes",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    try:
                        fb_df = pd.read_csv("feedback.csv")
                        fb_df = pd.concat([fb_df, pd.DataFrame([fb])], ignore_index=True)
                    except Exception:
                        fb_df = pd.DataFrame([fb])
                    fb_df.to_csv("feedback.csv", index=False)
                    st.success("Thanks — feedback recorded.")

            # ---------- NO ----------
            with c2:
                if st.button("👎 No"):
                    st.warning("Select the correct category:")

                    corrected = st.selectbox(
                        "Correct category:",
                        [
                            "Food & Dining", "Groceries", "Transport",
                            "Shopping", "Bills & Utilities", "Banking",
                            "Entertainment", "Other"
                        ]
                    )

                    if st.button("Submit Correction"):
                        fb = {
                            "transaction": tx_input,
                            "predicted_category": result.get("category", "Unknown"),
                            "correct_category": corrected,
                            "confidence": float(result.get("confidence", 0.0)),
                            "feedback": "no",
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                        try:
                            fb_df = pd.read_csv("feedback.csv")
                            fb_df = pd.concat([fb_df, pd.DataFrame([fb])], ignore_index=True)
                        except Exception:
                            fb_df = pd.DataFrame([fb])
                        fb_df.to_csv("feedback.csv", index=False)
                        st.success("Correction saved — thanks!")

            st.markdown('</div>', unsafe_allow_html=True)
            # -------- END FEEDBACK CARD --------


    # =====================================
    # RIGHT COLUMN — DEMO + TIPS
    # =====================================
    with right_col:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("#### 🚀 Quick Demo")
        st.markdown("- Enter a single transaction and press *Categorize*")
        st.markdown("- Use **Bulk Upload** to analyze many at once")
        st.markdown("- Visit **Analytics** to view category breakdowns")

        st.markdown("---")

        st.markdown("#### 💡 Tips")
        st.markdown("• Use merchant name + amount e.g., `Uber Trip 221`")
        st.markdown("• Use `history.csv` to see saved results")

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# BULK UPLOAD PAGE
# -------------------------
elif page == "Bulk Upload":
    st.markdown("<h2 style='font-size:28px;'>📁 Bulk Upload & Batch Categorization</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#94a3b8; margin-bottom:8px'>Upload a CSV containing a column with transaction text (e.g., description, text, transaction).</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
        except Exception:
            st.error("Could not read CSV. Ensure it's a valid CSV (UTF-8).")
            st.stop()

        col_candidates = [c for c in df.columns if any(k in c.lower() for k in ["trans","text","desc","merchant"])]
        chosen_col = col_candidates[0] if col_candidates else df.columns[0]
        st.info(f"Using column **{chosen_col}** for categorization.")
        if st.button("Start Batch Categorization", use_container_width=True):
            total = len(df)
            progress = st.progress(0)
            status = st.empty()
            results = []
            for i, row in df.iterrows():
                txt = str(row[chosen_col])
                try:
                    out = predict_category(txt)
                except Exception:
                    out = {"category":"Unknown","confidence":0.0,"explanation":""}
                results.append({
                    "transaction": txt,
                    "category": out.get("category","Unknown"),
                    "confidence": float(out.get("confidence",0.0)),
                    "explanation": out.get("explanation","")
                })
                if (i+1) % 5 == 0:
                    progress.progress((i+1)/total)
                    status.write(f"Processing {i+1}/{total}...")
            progress.progress(1.0)
            status.write("Done.")
            res_df = pd.DataFrame(results)
            res_df.to_csv("batch_results.csv", index=False)
            # append to history
            try:
                hist = pd.read_csv("history.csv")
                hist = pd.concat([hist, res_df.assign(timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))], ignore_index=True)
            except Exception:
                hist = res_df.assign(timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))
            hist.to_csv("history.csv", index=False)
            st.success("Batch categorization complete.")
            st.dataframe(res_df.head(200))
            csv_bytes = res_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Download results CSV", csv_bytes, "FinSenseAI_batch_results.csv", mime="text/csv", use_container_width=True)

# -------------------------
# -------------------------
# ANALYTICS PAGE
# -------------------------
elif page == "Analytics":
    st.markdown("## 📊 Analytics & Insights")

    try:
        hist = pd.read_csv("history.csv")
    except Exception:
        st.info("No history found — run predictions first.")
        st.stop()

    if hist.empty:
        st.info("History is empty — create some predictions first.")
        st.stop()

    # Category counts
    cat_counts = hist["category"].value_counts().reset_index()
    cat_counts.columns = ["category","count"]

    # Pie chart
    st.markdown("### Category Distribution")
    fig = px.pie(cat_counts, names="category", values="count", title="Spending by Category")
    st.plotly_chart(fig, use_container_width=True)

    # Confidence boxplot
    st.markdown("### Confidence by Category")
    st.plotly_chart(px.box(hist, x="category", y="confidence",
                           title="Confidence distribution per category"),
                    use_container_width=True)

    # Recent predictions
    st.markdown("### Recent Predictions (most recent 50)")
    st.dataframe(hist.sort_values("timestamp", ascending=False).head(50))

# -------------------------
# FEEDBACK ANALYTICS PAGE
# -------------------------
elif page == "Feedback Analytics":
    st.markdown("## 🗂️ Feedback Analytics")

    # ---- load feedback ----
    try:
        fb_df = pd.read_csv("feedback.csv")
    except Exception:
        st.info("No feedback logged yet.")
        st.stop()

    if fb_df.empty:
        st.info("No feedback to visualise.")
        st.stop()

    # ---- overall counts ----
    total = len(fb_df)
    yes_n = (fb_df["feedback"] == "yes").sum()
    no_n  = (fb_df["feedback"] == "no").sum()
    cols = st.columns(3)
    cols[0].metric("Total feedback", total)
    cols[1].metric("👍 Correct", yes_n)
    cols[2].metric("👎 Incorrect", no_n)

    # ---- accuracy ----
    if total:
        acc = yes_n / total
        st.metric("Model Accuracy (from feedback)", f"{acc:.1%}")

    # ---- feedback over time ----
    fb_df["timestamp"] = pd.to_datetime(fb_df["timestamp"], errors="coerce")
    daily = (fb_df
             .groupby([fb_df["timestamp"].dt.date, "feedback"])
             .size()
             .reset_index(name="count"))
    if not daily.empty:
        fig_line = px.line(daily, x="timestamp", y="count", color="feedback",
                          title="Daily feedback trend")
        st.plotly_chart(fig_line, use_container_width=True)

    # ---- confusion-style table ----
    st.markdown("### Confusion-style view")
    confusion = (fb_df
                .groupby(["predicted_category", "correct_category"])
                .size()
                .reset_index(name="n"))
    st.dataframe(confusion, use_container_width=True)

    # ---- raw table ----
    st.markdown("### Raw feedback log")
    st.dataframe(fb_df.sort_values("timestamp", ascending=False).head(200),
                use_container_width=True)
    


# -------------------------
# SMART INSIGHTS PAGE
# -------------------------
elif page == "Smart Insights":

    st.markdown("## 🧠 Smart Insights Dashboard")

    # Load history
    try:
        hist = pd.read_csv("history.csv")
    except:
        st.info("No history found — generate some predictions first.")
        st.stop()

    if hist.empty:
        st.info("Not enough data for insights yet.")
        st.stop()

    # Fix timestamps
    hist["timestamp"] = pd.to_datetime(hist["timestamp"], errors="coerce")
    hist = hist.dropna(subset=["timestamp"])

    # ====== TOP CATEGORIES THIS MONTH ======
    st.markdown("### 📌 Top Categories This Month")
    current_month = pd.Timestamp.now().month
    month_data = hist[hist["timestamp"].dt.month == current_month]

    if not month_data.empty:
        top_cats = month_data["category"].value_counts().reset_index()
        top_cats.columns = ["category", "count"]

        fig_bar = px.bar(
            top_cats,
            x="category",
            y="count",
            title="Most Frequent Categories This Month",
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No transactions yet for this month.")


    # ====== OVERALL PIE ======
    st.markdown("### 📌 Category Breakdown")
    fig_pie = px.pie(hist, names="category", title="Overall Category Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

    # ====== CONFIDENCE TREND ======
    st.markdown("### 📌 Model Confidence Trend Over Time")
    hist_sorted = hist.sort_values("timestamp")

    fig_line = px.line(
        hist_sorted, x="timestamp", y="confidence",
        title="Prediction Confidence Over Time"
    )
    st.plotly_chart(fig_line, use_container_width=True)


# -------------------------
# USER PREFERENCES PAGE
# -------------------------
# -------------------------
# USER PREFERENCES PAGE
# -------------------------
elif page == "User Preferences":
    st.markdown("## ⚙️ User Personalization Settings")
    st.markdown("Customize how FinSenseAI categorizes your transactions.")
    st.write("Your preferences override AI and rule-based predictions.")

    pref_path = "user_preferences.json"

    # ---------- Utility functions ----------
    def load_prefs():
        """Safely load user preferences JSON."""
        if os.path.exists(pref_path):
            try:
                with open(pref_path, "r") as f:
                    prefs = json.load(f)
            except:
                prefs = {}
        else:
            prefs = {}

        # ensure keys exist
        prefs.setdefault("merchant_rules", {})
        prefs.setdefault("keyword_rules", {})
        return prefs

    def save_prefs(data):
        with open(pref_path, "w") as f:
            json.dump(data, f, indent=4)

    prefs = load_prefs()

    # ---------------------------------------
    #           ADD MERCHANT RULE
    # ---------------------------------------
    st.markdown("### 🏪 Add Merchant-based Category Rule")
    st.caption("Example: **‘Swiggy’ → Food & Dining**")

    with st.form("add_merchant_rule"):
        merchant = st.text_input("Merchant name (e.g., Swiggy, IRCTC)")
        category = st.selectbox(
            "Assign Category",
            ["Food & Dining", "Groceries", "Transport", "Shopping",
             "Bills & Utilities", "Banking", "Entertainment", "Other"]
        )
        add_btn = st.form_submit_button("Add Rule")

        if add_btn:
            if merchant.strip():
                prefs["merchant_rules"][merchant.strip().lower()] = category
                save_prefs(prefs)
                st.success(f"Merchant Rule Added: {merchant} → {category}")
            else:
                st.error("Merchant name cannot be empty.")

    st.markdown("---")

    # ---------------------------------------
    #           ADD KEYWORD RULE
    # ---------------------------------------
    st.markdown("### 🔑 Add Keyword-based Rule")
    st.caption("Example: **‘subscription’ → Bills & Utilities**")

    with st.form("add_keyword_rule"):
        keyword = st.text_input("Keyword (e.g., subscription, groceries, recharge)")
        key_category = st.selectbox(
            "Assign Category",
            ["Food & Dining", "Groceries", "Transport", "Shopping",
             "Bills & Utilities", "Banking", "Entertainment", "Other"],
            key="keyword_category_select"
        )
        key_btn = st.form_submit_button("Add Keyword Rule")

        if key_btn:
            if keyword.strip():
                prefs["keyword_rules"][keyword.strip().lower()] = key_category
                save_prefs(prefs)
                st.success(f"Keyword Rule Added: '{keyword}' → {key_category}")
            else:
                st.error("Keyword cannot be empty.")

    st.markdown("---")

    # ---------------------------------------
    #         DISPLAY EXISTING RULES
    # ---------------------------------------
    st.markdown("### 📜 Existing Rules")
    
    # -------------------------
# RESET ALL RULES BUTTON
# -------------------------
    st.markdown("### 🔄 Reset All Preferences")

    if st.button("Reset All Rules"):
        prefs["merchant_rules"] = {}
        prefs["keyword_rules"] = {}
        save_prefs(prefs)
        st.warning("All rules have been reset.")
        st.experimental_rerun()
    # Merchant rules
    st.subheader("Merchant Rules")
    if prefs.get("merchant_rules"):
        for m, c in prefs["merchant_rules"].items():
            col1, col2 = st.columns([3,1])
            col1.write(f"**{m.capitalize()}** → {c}")
            if col2.button("Delete", key=f"del_m_{m}"):
                prefs["merchant_rules"].pop(m)
                save_prefs(prefs)
                st.warning(f"Deleted merchant rule: {m}")
                st.experimental_rerun()
    else:
        st.info("No merchant rules yet.")

    st.markdown("")

    # Keyword rules
    st.subheader("Keyword Rules")
    if prefs.get("keyword_rules"):
        for k, c in prefs["keyword_rules"].items():
            col1, col2 = st.columns([3,1])
            col1.write(f"**{k}** → {c}")
            if col2.button("Delete", key=f"del_k_{k}"):
                prefs["keyword_rules"].pop(k)
                save_prefs(prefs)
                st.warning(f"Deleted keyword rule: {k}")
                st.experimental_rerun()
    else:
        st.info("No keyword rules yet.")
    # -------------------------
    # Coming Soon Panel
    # -------------------------
    st.markdown("---")
    st.markdown("### 🚀 Coming Soon")

    st.info("""
    **Personalization 2.0 (Upcoming Features)**  
    - AI learns your spending habits  
    - Auto-suggested rules  
    - Personalized budget predictions  
    - Merchant intelligence  
    - Smart category auto-correction  
    """)



# -------------------------
# ABOUT PAGE
# -------------------------
elif page == "About":
    st.markdown("## About FinSenseAI")
    st.markdown("""
FinSenseAI is a transformer-based transaction categorization prototype designed for fintechs and banks.
- ✅ Standalone on-premise inference (no external API)
- ✅ Customizable category taxonomy
- ✅ Explainable predictions (confidence + short rationale)
- ✅ Bulk-processing + analytics
""")
    st.markdown("---")
    st.markdown("### Next steps for production")
    st.markdown("- Merchant normalization & enrichment\n- Retraining pipeline with labeled feedback\n- Caching & batched inference for throughput\n- RBAC and encryption for enterprise compliance")
    st.markdown("---")
    st.markdown("### Contacts")
    st.markdown("- Team lead: Kimmoji Raja")
    st.markdown("- GitHub: [FinSenseAI repo](https://github.com/Kimmojiraja)")
    st.markdown("### 🔖 Version Metadata (Technical)")
    st.json(VERSION)




# -------------------------
# CHANGELOG PAGE
# -------------------------
elif page == "Changelog":
    st.markdown("## 🧾 Changelog")
    st.markdown("Track the evolution of FinSenseAI over time.")
    st.markdown("---")

    changelog = load_changelog()

    if not changelog:
        st.info("No changelog entries found.")
        st.stop()

    for entry in changelog:
        st.markdown(f"### 🚀 Version {entry['version']}  —  *{entry['date']}*")
        for change in entry["changes"]:
            st.markdown(f"- {change}")
        st.markdown("---")


# -------------------------
# End
# -------------------------
