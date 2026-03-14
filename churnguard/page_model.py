"""
page_model.py
Model evaluation charts and metrics.
All charts match what was produced in 03_model.ipynb.
"""

import streamlit as st
import plotly.graph_objects as go
import ui

BLUE  = "#118DFF"
RED   = "#D64550"
GREEN = "#107C10"

_L = dict(
    paper_bgcolor = "white",
    plot_bgcolor  = "white",
    font_family   = "IBM Plex Sans",
    font_color    = "#252423",
    height        = 310,
    margin        = dict(l=10, r=10, t=38, b=10),
    xaxis         = dict(gridcolor="#EDEBE9", linecolor="#EDEBE9"),
    yaxis         = dict(gridcolor="#EDEBE9", linecolor="#EDEBE9"),
    title_font    = dict(size=12, color="#252423"),
    title_x       = 0,
    shapes        = [dict(
        type="rect", xref="paper", yref="paper",
        x0=0, y0=0, x1=1, y1=1,
        line=dict(color="#EDEBE9", width=1),
        fillcolor="rgba(0,0,0,0)", layer="above",
    )],
)

_OPTS = dict(use_container_width=True, config={"displayModeBar": False})


def render(df, metrics):
    acc  = metrics["accuracy"]
    auc  = metrics["roc_auc"]
    cm   = metrics["cm"]
    rep  = metrics["report"]
    imp  = metrics["importance"]
    fpr  = metrics["fpr"]
    tpr  = metrics["tpr"]

    ui.page_title("Model Results")
    st.write("""
        A Logistic Regression model was trained to predict whether each customer will churn.
        It uses six features: tenure, monthly charges, total charges, senior citizen status,
        number of active services, and the RFM score.
    """)
    ui.divider()

    ui.section("Performance Summary")
    ui.kpi_row([
        {"label": "Accuracy",   "value": f"{acc*100:.1f}%",              "sub": "Correct predictions on test set",         "accent": "#107C10"},
        {"label": "ROC-AUC",    "value": f"{auc:.3f}",                   "sub": "1.0 = perfect, 0.5 = random guess",       "accent": "#107C10"},
        {"label": "Precision",  "value": f"{rep['1']['precision']*100:.1f}%", "sub": "Of flagged churners who actually churn","accent": "#0078D4"},
        {"label": "Recall",     "value": f"{rep['1']['recall']*100:.1f}%",    "sub": "Of actual churners the model catches", "accent": "#0078D4"},
    ])
    ui.divider()

    ui.section("Confusion Matrix and Feature Importance")
    c1, c2 = st.columns(2)

    # Confusion matrix (from notebook: sns.heatmap(cm))
    tn, fp, fn, tp = cm.ravel()
    fig_cm = go.Figure(go.Heatmap(
        z=[[tn, fp], [fn, tp]],
        x=["Predicted: No", "Predicted: Yes"],
        y=["Actual: No",    "Actual: Yes"],
        colorscale=[[0, "#F3F2F1"], [1, BLUE]],
        showscale=False,
        text=[[str(tn), str(fp)], [str(fn), str(tp)]],
        texttemplate="<b>%{text}</b>",
        textfont=dict(size=20),
    ))
    fig_cm.update_layout(**_L, title_text="Confusion Matrix")
    c1.plotly_chart(fig_cm, **_OPTS)
    c1.caption(
        f"True Negatives: **{tn}** (correctly identified as loyal)  |  "
        f"True Positives: **{tp}** (correctly identified as churners)  |  "
        f"False Positives: **{fp}**  |  False Negatives: **{fn}**"
    )

    # Feature importance (from notebook: model.coef_)
    colors = [RED if c > 0 else GREEN for c in imp["Coefficient"]]
    fig_imp = go.Figure(go.Bar(
        x=imp["Coefficient"],
        y=imp["Feature"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:+.3f}" for v in imp["Coefficient"]],
        textposition="outside",
    ))
    fig_imp.update_layout(**_L, title_text="Feature Importance (Logistic Regression Coefficients)")
    fig_imp.update_xaxes(title="Coefficient value", zeroline=True, zerolinecolor="#EDEBE9")
    c2.plotly_chart(fig_imp, **_OPTS)
    c2.caption("Positive coefficients increase churn probability. Negative ones reduce it.")

    ui.divider()
    ui.section("ROC Curve")
    c3, c4 = st.columns(2)

    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines",
        name=f"Model  (AUC = {auc:.3f})",
        line=dict(color=BLUE, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(17,141,255,0.07)",
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines",
        line=dict(color="#C8C6C4", dash="dash"),
        showlegend=False,
    ))
    fig_roc.update_layout(**_L, title_text="ROC Curve")
    fig_roc.update_xaxes(title="False Positive Rate", range=[0, 1])
    fig_roc.update_yaxes(title="True Positive Rate",  range=[0, 1.02])
    c3.plotly_chart(fig_roc, **_OPTS)

    c4.markdown("#### How to read these results")
    c4.write("""
        **Accuracy (79%)** means the model gets the right answer about 4 out of 5 times
        when predicting whether a customer will churn.

        **ROC-AUC (0.83)** measures how well the model separates churners from
        loyal customers across all possible thresholds. A score of 1.0 is perfect;
        0.5 means no better than a coin flip.

        **The ROC curve** shows the trade-off between catching more churners (recall)
        and avoiding false alarms (precision). The further the curve bows toward the
        top-left corner, the better the model.

        **Feature importance** shows which inputs influence the prediction most.
        High monthly charges and short tenure are the strongest signals that a
        customer is likely to leave.
    """)