"""
page_model.py
Model evaluation — confusion matrix, feature importance, ROC curve.
Enhanced StockPulse-style design.
"""

import streamlit as st
import plotly.graph_objects as go
import ui

BLUE  = "#0078D4"
RED   = "#D64550"
GREEN = "#107C10"

_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_family="DM Sans",
    font_color="#252423",
    height=320,
    margin=dict(l=12, r=12, t=44, b=12),
    xaxis=dict(gridcolor="#F3F2F1", linecolor="#EDEBE9", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#F3F2F1", linecolor="#EDEBE9", tickfont=dict(size=11)),
    title_font=dict(size=13, color="#252423", family="DM Sans"),
    title_x=0,
    title_pad=dict(l=4),
    shapes=[dict(
        type="rect", xref="paper", yref="paper",
        x0=0, y0=0, x1=1, y1=1,
        line=dict(color="#EDEBE9", width=1),
        fillcolor="rgba(0,0,0,0)", layer="above",
    )],
)

_OPTS = dict(use_container_width=True, config={"displayModeBar": False})

_CARD = (
    '<div style="background:#FFFFFF;border:1px solid #EDEBE9;'
    'border-radius:8px;padding:4px 4px 0;'
    'box-shadow:0 1px 5px rgba(0,0,0,0.05);">'
)


def render(df, metrics):
    acc = metrics["accuracy"]
    auc = metrics["roc_auc"]
    cm  = metrics["cm"]
    rep = metrics["report"]
    imp = metrics["importance"]
    fpr = metrics["fpr"]
    tpr = metrics["tpr"]

    ui.page_title(
        "Model Results",
        "Logistic Regression trained on tenure, charges, services, and RFM score.",
    )

    # ── Performance summary ────────────────────────────────────────────────────
    ui.section("Performance Summary")
    tn, fp, fn, tp = cm.ravel()
    ui.kpi_row([
        {"label": "Accuracy",           "value": f"{acc*100:.1f}%",                  "sub": "Overall correct predictions",             "accent": "#107C10"},
        {"label": "ROC-AUC",            "value": f"{auc:.3f}",                       "sub": "1.0 = perfect · 0.5 = random",            "accent": "#107C10"},
        {"label": "Precision",          "value": f"{rep['1']['precision']*100:.1f}%","sub": "Of predicted churners who actually churn", "accent": "#0078D4"},
        {"label": "Recall",             "value": f"{rep['1']['recall']*100:.1f}%",   "sub": "Of actual churners the model catches",     "accent": "#0078D4"},
        {"label": "True Positives",     "value": f"{tp:,}",                          "sub": f"Missed (false negatives): {fn:,}",        "accent": "#CA5010"},
    ])

    # ── Confusion matrix + Feature importance ─────────────────────────────────
    ui.section("Confusion Matrix and Feature Importance")
    c1, c2 = st.columns(2)

    fig_cm = go.Figure(go.Heatmap(
        z=[[tn, fp], [fn, tp]],
        x=["Predicted: No", "Predicted: Yes"],
        y=["Actual: No",    "Actual: Yes"],
        colorscale=[[0, "#EBF4FF"], [0.5, "#93C5FD"], [1, BLUE]],
        showscale=False,
        text=[[str(tn), str(fp)], [str(fn), str(tp)]],
        texttemplate="<b>%{text}</b>",
        textfont=dict(size=20, family="DM Mono"),
    ))
    fig_cm.update_layout(**_BASE, title_text="Confusion Matrix")

    c1.markdown(_CARD, unsafe_allow_html=True)
    c1.plotly_chart(fig_cm, **_OPTS)
    c1.markdown("</div>", unsafe_allow_html=True)
    ui.caption(
        f"TN {tn:,} — correctly identified as loyal.  TP {tp:,} — correctly flagged as churners.  "
        f"FP {fp:,} — false alarms.  FN {fn:,} — missed churners."
    )

    # Feature importance
    colors = [RED if v > 0 else GREEN for v in imp["Coefficient"]]
    fig_imp = go.Figure(go.Bar(
        x=imp["Coefficient"],
        y=imp["Feature"],
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        opacity=0.9,
        text=[f"{v:+.3f}" for v in imp["Coefficient"]],
        textposition="outside",
        textfont=dict(size=11, family="DM Mono"),
    ))
    fig_imp.update_layout(**_BASE, title_text="Feature Importance (LR Coefficients)")
    fig_imp.update_layout(margin=dict(l=12, r=60, t=44, b=12))
    fig_imp.update_xaxes(
        title="Coefficient",
        zeroline=True,
        zerolinecolor="#CBD5E0",
        zerolinewidth=1.5,
        showgrid=True,
    )
    fig_imp.update_yaxes(showgrid=False)

    c2.markdown(_CARD, unsafe_allow_html=True)
    c2.plotly_chart(fig_imp, **_OPTS)
    c2.markdown("</div>", unsafe_allow_html=True)
    ui.caption(
        "Positive coefficients increase churn probability. Negative ones reduce it. "
        "Monthly charges is the strongest positive predictor; tenure the strongest negative."
    )

    # ── ROC curve + interpretation ─────────────────────────────────────────────
    ui.section("ROC Curve")
    c3, c4 = st.columns([1.2, 1])

    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode="lines",
        name=f"Model  (AUC = {auc:.3f})",
        line=dict(color=BLUE, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(27,108,242,0.08)",
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode="lines",
        line=dict(color="#CBD5E0", dash="dash", width=1.5),
        showlegend=False,
    ))
    fig_roc.update_layout(
        **_BASE,
        title_text="ROC Curve",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font_size=12,
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
        ),
    )
    fig_roc.update_xaxes(title="False Positive Rate", range=[0, 1], showgrid=True)
    fig_roc.update_yaxes(title="True Positive Rate",  range=[0, 1.02])

    c3.markdown(_CARD, unsafe_allow_html=True)
    c3.plotly_chart(fig_roc, **_OPTS)
    c3.markdown("</div>", unsafe_allow_html=True)

    with c4:
        ui.section("How to Read These Results")
        ui.info_box(
            f"<b>Accuracy ({acc*100:.1f}%)</b> — the model gets the right answer about "
            f"4 out of 5 times when predicting churn.",
            kind="success",
        )
        ui.info_box(
            f"<b>ROC-AUC ({auc:.3f})</b> — measures how well the model separates "
            f"churners from loyal customers. A score of 1.0 is perfect; "
            f"0.5 means no better than a coin flip.",
            kind="info",
        )
        ui.info_box(
            "The <b>ROC curve</b> shows the trade-off between catching more churners "
            "(recall) and avoiding false alarms. Further toward the top-left = better.",
            kind="info",
        )
        ui.info_box(
            "<b>Feature importance</b>: high monthly charges and short tenure are "
            "the two strongest signals of churn.",
            kind="warning",
        )