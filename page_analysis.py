"""
page_analysis.py
Eight charts from 02_eda_churn_analysis.ipynb, in four sections.
Enhanced with StockPulse-style chart cards.
"""

import streamlit as st
import plotly.graph_objects as go
import ui

BLUE = "#0078D4"
RED  = "#D64550"
BLUE_LIGHT = "rgba(27,108,242,0.12)"
RED_LIGHT  = "rgba(229,56,59,0.12)"

_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_family="DM Sans",
    font_color="#252423",
    height=320,
    margin=dict(l=12, r=12, t=44, b=12),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font_size=12,
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1,
    ),
    xaxis=dict(
        gridcolor="#F3F2F1",
        linecolor="#EDEBE9",
        tickfont=dict(size=11),
        showgrid=False,
    ),
    yaxis=dict(
        gridcolor="#F3F2F1",
        linecolor="#EDEBE9",
        tickfont=dict(size=11),
        title="Count",
        gridwidth=1,
    ),
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

_CARD_WRAP_START = (
    '<div style="background:#FFFFFF;border:1px solid #EDEBE9;'
    'border-radius:8px;padding:4px 4px 0;'
    'box-shadow:0 1px 5px rgba(0,0,0,0.05);margin-bottom:2px;">'
)
_CARD_WRAP_END = '</div>'


def _chart_card(col, fig, opts):
    col.markdown(_CARD_WRAP_START, unsafe_allow_html=True)
    col.plotly_chart(fig, **opts)
    col.markdown(_CARD_WRAP_END, unsafe_allow_html=True)


def _bar(df, col, title, order):
    no  = [len(df[(df[col] == c) & (df["Churn"] == "No")])  for c in order]
    yes = [len(df[(df[col] == c) & (df["Churn"] == "Yes")]) for c in order]
    fig = go.Figure()
    fig.add_bar(
        name="Retained", x=order, y=no,
        marker_color=BLUE,
        marker_line_width=0,
        opacity=0.92,
    )
    fig.add_bar(
        name="Churned", x=order, y=yes,
        marker_color=RED,
        marker_line_width=0,
        opacity=0.92,
    )
    fig.update_layout(**_BASE, title_text=title, barmode="group", bargap=0.22, bargroupgap=0.06)
    return fig


def _box(df, y_col, title):
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df[df["Churn"] == "No"][y_col],
        name="Retained",
        marker_color=BLUE,
        fillcolor=BLUE_LIGHT,
        line_color=BLUE,
        boxpoints=False,
        whiskerwidth=0.5,
    ))
    fig.add_trace(go.Box(
        y=df[df["Churn"] == "Yes"][y_col],
        name="Churned",
        marker_color=RED,
        fillcolor=RED_LIGHT,
        line_color=RED,
        boxpoints=False,
        whiskerwidth=0.5,
    ))
    fig.update_layout(**_BASE, title_text=title)
    fig.update_yaxes(title=y_col)
    return fig


def render(df):
    ui.page_title(
        "Customer Analysis",
        "Which customer characteristics are linked to higher churn rates.",
    )

    # ── 1. Overall Churn ──────────────────────────────────────────────────────
    ui.section("Overall Churn")
    c1, c2 = st.columns(2)

    counts = df["Churn"].value_counts()
    fig1 = go.Figure(go.Bar(
        x=["Retained", "Churned"],
        y=[counts.get("No", 0), counts.get("Yes", 0)],
        marker_color=[BLUE, RED],
        marker_line_width=0,
        width=0.42,
        text=[counts.get("No", 0), counts.get("Yes", 0)],
        textposition="outside",
        textfont=dict(size=12, color="#252423"),
        opacity=0.93,
    ))
    fig1.update_layout(**_BASE, title_text="1. Churn Distribution")
    _chart_card(c1, fig1, _OPTS)
    ui.caption(
        "About 1 in 4 customers leaves every year. "
        "Retaining even a fraction would protect significant revenue."
    )

    avg_no  = df[df["Churn"] == "No"]["tenure"].mean()
    avg_yes = df[df["Churn"] == "Yes"]["tenure"].mean()
    _chart_card(c2, _box(df, "tenure", "2. Tenure vs Churn (months)"), _OPTS)
    ui.caption(
        f"Retained customers stay {avg_no:.0f} months on average. "
        f"Churned customers leave after just {avg_yes:.0f} months."
    )

    # ── 2. Contract and Internet ──────────────────────────────────────────────
    ui.section("Contract Type and Internet Service")
    c3, c4 = st.columns(2)
    _chart_card(
        c3,
        _bar(df, "Contract", "3. Contract Type vs Churn",
             ["Month-to-month", "One year", "Two year"]),
        _OPTS,
    )
    ui.caption(
        "Month-to-month customers churn far more. "
        "Long-term contracts reduce switching by creating commitment."
    )

    _chart_card(
        c4,
        _bar(df, "InternetService", "4. Internet Service vs Churn",
             ["DSL", "Fiber optic", "No"]),
        _OPTS,
    )
    ui.caption(
        "Fiber optic customers churn the most — "
        "likely due to higher costs and more competitive alternatives."
    )

    # ── 3. Billing and Payment ────────────────────────────────────────────────
    ui.section("Billing and Payment")
    c5, c6 = st.columns(2)
    _chart_card(c5, _box(df, "MonthlyCharges", "5. Monthly Charges vs Churn ($)"), _OPTS)
    ui.caption(
        "Customers who churn pay noticeably higher monthly bills. "
        "Price sensitivity is a clear churn driver."
    )

    pay_order = [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)",
    ]
    _chart_card(
        c6,
        _bar(df, "PaymentMethod", "6. Payment Method vs Churn", pay_order),
        _OPTS,
    )
    ui.caption(
        "Electronic check users churn the most. "
        "Auto-payment customers are far more loyal."
    )

    c7, c8 = st.columns(2)
    _chart_card(
        c7,
        _bar(df, "PaperlessBilling", "7. Paperless Billing vs Churn", ["Yes", "No"]),
        _OPTS,
    )
    ui.caption(
        "Paperless billing customers churn slightly more — "
        "switching providers is easier when everything is online."
    )

    # ── 4. Demographics ───────────────────────────────────────────────────────
    ui.section("Demographics")
    df2 = df.copy()
    df2["Senior"] = df2["SeniorCitizen"].map({0: "Non-Senior", 1: "Senior"})
    _chart_card(
        c8,
        _bar(df2, "Senior", "8. Senior Citizen vs Churn", ["Non-Senior", "Senior"]),
        _OPTS,
    )
    ui.caption(
        "Senior citizens churn at a higher rate — "
        "they may be more sensitive to price or have less digital engagement."
    )