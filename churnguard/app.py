"""
app.py
Main Streamlit entry point.
Run:  streamlit run app.py
"""

import streamlit as st
from data  import load_data
from model import train_model
import page_overview, page_analysis, page_segments, page_model, page_predict

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title   = "ChurnGuard",
    layout       = "wide",
    initial_sidebar_state = "collapsed",
    menu_items   = {},
)

# ── Fonts + global styles ─────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* { font-family: 'IBM Plex Sans', sans-serif !important; }

/* Tabs — BaseUI selectors, always stable */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-bottom: 2px solid #EDEBE9;
    padding: 0 32px;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    padding: 13px 22px;
    font-size: 0.875rem;
    font-weight: 500;
    color: #605E5C;
    border-radius: 0;
    margin: 0;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #0078D4 !important;
    font-weight: 600 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"] { background: #0078D4 !important; height: 2px !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }
.stTabs [data-baseweb="tab-panel"]     { padding: 28px 32px; }
</style>
""", unsafe_allow_html=True)

# ── App header ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:white; border-bottom:1px solid #EDEBE9; padding:14px 32px;">
    <span style="font-size:1.05rem; font-weight:700; color:#252423; letter-spacing:-0.01em;">
        ChurnGuard
    </span>
    <span style="font-size:0.78rem; color:#A19F9D; margin-left:14px;">
        Telco Customer Retention System
    </span>
</div>
""", unsafe_allow_html=True)

# ── Load data and train model (cached) ────────────────────────────────────────
df_raw                    = load_data()
model, scaler, df, metrics = train_model(df_raw)

# ── Navigation ────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Overview",
    "Customer Analysis",
    "Customer Segments",
    "Model Results",
    "Churn Predictor",
])

with tabs[0]: page_overview.render(df, metrics)
with tabs[1]: page_analysis.render(df)
with tabs[2]: page_segments.render(df)
with tabs[3]: page_model.render(df, metrics)
with tabs[4]: page_predict.render(model, scaler, df)