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
    page_title            = "ChurnGuard Analytics",
    layout                = "wide",
    initial_sidebar_state = "collapsed",
    menu_items            = {},
)

# ── Step 1: External fonts  (separate call — never mix <link> and <style>) ────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">'
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">',
    unsafe_allow_html=True,
)

# ── Step 2: All global CSS in ONE dedicated <style> block ─────────────────────
st.markdown(
    """<style>
* { font-family: 'DM Sans', sans-serif !important; }

[data-testid="stAppViewContainer"] > .main { background: #F3F2F1; }
[data-testid="stAppViewContainer"]          { background: #F3F2F1; }
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
}

/* Kill the top gap Streamlit injects */
[data-testid="stAppViewBlockContainer"] { padding-top: 0 !important; }
div[class*="appview-container"] .main .block-container { padding-top: 0 !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }
.stMainBlockContainer { padding-top: 0 !important; }

/* Hide Streamlit chrome */
[data-testid="stHeader"]          { display: none !important; }
[data-testid="stToolbar"]         { display: none !important; }
[data-testid="stDecoration"]      { display: none !important; }
[data-testid="stStatusWidget"]    { display: none !important; }
#MainMenu                           { display: none !important; }
footer                              { display: none !important; }
header                              { display: none !important; }

/* Full viewport */
html, body { margin: 0 !important; padding: 0 !important; overflow-x: hidden; }
[data-testid="stAppViewContainer"] {
    padding: 0 !important;
    margin: 0 !important;
}
[data-testid="stAppViewContainer"] > .main {
    padding: 0 !important;
}

/* Tab panel inner padding preserved for content breathing room */
.stTabs [data-baseweb="tab-panel"] { padding: 24px 32px; background: #F3F2F1; }

.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-bottom: 2px solid #EDEBE9;
    padding: 0 32px;
    gap: 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.stTabs [data-baseweb="tab"] {
    padding: 14px 26px;
    font-size: 0.875rem;
    font-weight: 500;
    color: #605E5C;
    border-radius: 0;
    margin: 0;
    background: transparent;
    letter-spacing: 0.01em;
}
.stTabs [aria-selected="true"] {
    color: #0078D4 !important;
    font-weight: 600 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"] { background: #0078D4 !important; height: 2px !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }
.stTabs [data-baseweb="tab-panel"]     { padding: 28px 32px; background: #F3F2F1; }

.stTabs [data-baseweb="tab"]:nth-child(1) p::before
    { font-family:"Font Awesome 6 Free"; font-weight:900; content:"\f080\00a0\00a0"; }
.stTabs [data-baseweb="tab"]:nth-child(2) p::before
    { font-family:"Font Awesome 6 Free"; font-weight:900; content:"\f002\00a0\00a0"; }
.stTabs [data-baseweb="tab"]:nth-child(3) p::before
    { font-family:"Font Awesome 6 Free"; font-weight:900; content:"\f007\00a0\00a0"; }
.stTabs [data-baseweb="tab"]:nth-child(4) p::before
    { font-family:"Font Awesome 6 Free"; font-weight:900; content:"\f201\00a0\00a0"; }
.stTabs [data-baseweb="tab"]:nth-child(5) p::before
    { font-family:"Font Awesome 6 Free"; font-weight:900; content:"\f0e7\00a0\00a0"; }

::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F3F2F1; }
::-webkit-scrollbar-thumb { background: #C8C6C4; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #A19F9D; }

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0078D4, #2B88D8) !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 0.55rem 1rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 2px 8px rgba(0,120,212,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(0,120,212,0.45) !important;
}

[data-testid="stSlider"] > div > div > div > div { background: #0078D4 !important; }

[data-baseweb="tag"] { background: #EFF6FC !important; color: #0078D4 !important; }

@keyframes cg-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(74,222,128,0.7); }
    50%       { box-shadow: 0 0 0 4px rgba(74,222,128,0); }
}
</style>""",
    unsafe_allow_html=True,
)

# ── Load data and train model (cached) ────────────────────────────────────────
df_raw                     = load_data()
model, scaler, df, metrics = train_model(df_raw)

total   = len(df)
churned = int(df["Churn_Binary"].sum())
rate    = churned / total
acc     = metrics["accuracy"]
auc     = metrics["roc_auc"]

# ── Dark navy header  (NO <style> tags here) ──────────────────────────────────
st.markdown(
    f'<div style="background:linear-gradient(120deg,#0B1526 0%,#0D1F3C 60%,#0F2A52 100%);'
    f'padding:0 32px;display:flex;justify-content:space-between;align-items:center;'
    f'min-height:64px;box-shadow:0 2px 12px rgba(0,0,0,0.3);position:relative;overflow:hidden;">'

    f'<div style="position:absolute;inset:0;opacity:0.03;pointer-events:none;'
    f'background-image:linear-gradient(rgba(255,255,255,.5) 1px,transparent 1px),'
    f'linear-gradient(90deg,rgba(255,255,255,.5) 1px,transparent 1px);'
    f'background-size:28px 28px;"></div>'

    f'<div style="display:flex;align-items:center;gap:14px;position:relative;">'
    f'<div style="width:38px;height:38px;'
    f'background:linear-gradient(135deg,#0078D4 0%,#2B88D8 100%);'
    f'border-radius:8px;display:flex;align-items:center;justify-content:center;'
    f'color:white;font-size:1rem;box-shadow:0 2px 12px rgba(0,120,212,0.5);">'
    f'<i class="fa-solid fa-shield-halved"></i></div>'
    f'<div>'
    f'<div style="font-size:1.05rem;font-weight:700;color:#FFFFFF;'
    f'letter-spacing:-0.02em;line-height:1.2;">ChurnGuard</div>'
    f'<div style="font-size:0.62rem;color:#7B93B8;font-weight:500;'
    f'letter-spacing:0.06em;text-transform:uppercase;margin-top:1px;">'
    f'Telco &middot; Customer Retention Analytics</div>'
    f'</div></div>'

    f'<div style="display:flex;align-items:center;position:relative;">'

    f'<div style="padding:8px 24px;border-left:1px solid rgba(255,255,255,0.08);text-align:center;">'
    f'<div style="font-size:0.56rem;font-weight:600;color:#7B93B8;text-transform:uppercase;'
    f'letter-spacing:.1em;margin-bottom:4px;">'
    f'<i class="fa-solid fa-users" style="margin-right:5px;"></i>Total Customers</div>'
    f'<div style="font-size:1.05rem;font-weight:700;color:#FFFFFF;font-family:DM Mono,monospace;">'
    f'{total:,}</div></div>'

    f'<div style="padding:8px 24px;border-left:1px solid rgba(255,255,255,0.08);text-align:center;">'
    f'<div style="font-size:0.56rem;font-weight:600;color:#7B93B8;text-transform:uppercase;'
    f'letter-spacing:.1em;margin-bottom:4px;">'
    f'<i class="fa-solid fa-right-from-bracket" style="margin-right:5px;"></i>Churn Rate</div>'
    f'<div style="font-size:1.05rem;font-weight:700;color:#FF6B7A;font-family:DM Mono,monospace;">'
    f'{rate*100:.1f}%</div></div>'

    f'<div style="padding:8px 24px;border-left:1px solid rgba(255,255,255,0.08);text-align:center;">'
    f'<div style="font-size:0.56rem;font-weight:600;color:#7B93B8;text-transform:uppercase;'
    f'letter-spacing:.1em;margin-bottom:4px;">'
    f'<i class="fa-solid fa-bullseye" style="margin-right:5px;"></i>Model Accuracy</div>'
    f'<div style="font-size:1.05rem;font-weight:700;color:#4ADE80;font-family:DM Mono,monospace;">'
    f'{acc*100:.1f}%</div></div>'

    f'<div style="padding:8px 24px;border-left:1px solid rgba(255,255,255,0.08);text-align:center;">'
    f'<div style="font-size:0.56rem;font-weight:600;color:#7B93B8;text-transform:uppercase;'
    f'letter-spacing:.1em;margin-bottom:4px;">'
    f'<i class="fa-solid fa-chart-line" style="margin-right:5px;"></i>ROC-AUC</div>'
    f'<div style="font-size:1.05rem;font-weight:700;color:#60A5FA;font-family:DM Mono,monospace;">'
    f'{auc:.3f}</div></div>'

    f'<div style="padding:8px 20px;border-left:1px solid rgba(255,255,255,0.08);'
    f'display:flex;align-items:center;gap:8px;">'
    f'<div style="width:8px;height:8px;background:#4ADE80;border-radius:50%;'
    f'animation:cg-pulse 2s infinite;"></div>'
    f'<div style="font-size:0.72rem;color:#7B93B8;font-weight:500;">Live</div>'
    f'</div>'

    f'</div></div>',
    unsafe_allow_html=True,
)

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