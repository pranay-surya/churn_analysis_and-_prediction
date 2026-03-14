"""
page_analysis.py
Eight charts from 02_eda_churn_analysis.ipynb, organized into sections.
Chart types match the notebook (count plots → grouped bar, box plots → box).
"""

import streamlit as st
import plotly.graph_objects as go

BLUE = "#118DFF"
RED  = "#D64550"

# Shared layout for all charts
_L = dict(
    paper_bgcolor = "white",
    plot_bgcolor  = "white",
    font_family   = "IBM Plex Sans",
    font_color    = "#252423",
    height        = 310,
    margin        = dict(l=10, r=10, t=38, b=10),
    legend        = dict(bgcolor="rgba(0,0,0,0)", font_size=11),
    xaxis         = dict(gridcolor="#EDEBE9", linecolor="#EDEBE9"),
    yaxis         = dict(gridcolor="#EDEBE9", linecolor="#EDEBE9", title="Count"),
    title_font    = dict(size=12, color="#252423"),
    title_x       = 0,
    shapes        = [dict(
        type="rect", xref="paper", yref="paper",
        x0=0, y0=0, x1=1, y1=1,
        line=dict(color="#EDEBE9", width=1),
        fillcolor="rgba(0,0,0,0)",
        layer="above",
    )],
)


def _grouped_bar(df, col, title, order):
    """Grouped bar — equivalent to sns.countplot(x=col, hue='Churn')."""
    no  = [len(df[(df[col] == c) & (df["Churn"] == "No")])  for c in order]
    yes = [len(df[(df[col] == c) & (df["Churn"] == "Yes")]) for c in order]
    fig = go.Figure()
    fig.add_bar(name="Retained", x=order, y=no,  marker_color=BLUE)
    fig.add_bar(name="Churned",  x=order, y=yes, marker_color=RED)
    fig.update_layout(**_L, title_text=title, barmode="group")
    return fig


def _box(df, y_col, title):
    """Box plot — equivalent to sns.boxplot(x='Churn', y=y_col)."""
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df[df["Churn"] == "No"][y_col],
        name="Retained", marker_color=BLUE, boxpoints=False,
    ))
    fig.add_trace(go.Box(
        y=df[df["Churn"] == "Yes"][y_col],
        name="Churned",  marker_color=RED,  boxpoints=False,
    ))
    fig.update_layout(**_L, title_text=title)
    fig.update_yaxes(title=y_col)
    return fig


_OPTS = dict(use_container_width=True, config={"displayModeBar": False})


def render(df):
    st.markdown("# Customer Analysis")
    st.write("Exploring which customer characteristics are linked to higher churn rates.")

    # ── Section 1: Churn Overview ─────────────────────────────────────────────
    st.divider()
    st.markdown("### Overall Churn")

    c1, c2 = st.columns(2)

    # Chart 1 — Churn Distribution (sns.countplot(x='Churn'))
    counts = df["Churn"].value_counts()
    fig1 = go.Figure(go.Bar(
        x=["Retained (No)", "Churned (Yes)"],
        y=[counts.get("No", 0), counts.get("Yes", 0)],
        marker_color=[BLUE, RED],
        width=0.4,
        text=[counts.get("No", 0), counts.get("Yes", 0)],
        textposition="outside",
    ))
    fig1.update_layout(**_L, title_text="1. Churn Distribution")
    c1.plotly_chart(fig1, **_OPTS)
    c1.caption("About 1 in 4 customers leaves every year. Retaining even a fraction of them would save significant revenue.")

    # Chart 2 — Tenure vs Churn (sns.boxplot(x='Churn', y='tenure'))
    avg_no  = df[df["Churn"] == "No"]["tenure"].mean()
    avg_yes = df[df["Churn"] == "Yes"]["tenure"].mean()
    c2.plotly_chart(_box(df, "tenure", "2. Tenure vs Churn (months)"), **_OPTS)
    c2.caption(f"Loyal customers stay for {avg_no:.0f} months on average. Churned customers leave after just {avg_yes:.0f} months.")

    # ── Section 2: Contract and Internet ─────────────────────────────────────
    st.divider()
    st.markdown("### Contract Type and Internet Service")

    c3, c4 = st.columns(2)

    # Chart 3 — Contract Type vs Churn
    c3.plotly_chart(
        _grouped_bar(df, "Contract", "3. Contract Type vs Churn",
                     ["Month-to-month", "One year", "Two year"]),
        **_OPTS,
    )
    c3.caption("Month-to-month customers churn far more often. Long-term contracts create loyalty and reduce switching.")

    # Chart 4 — Internet Service vs Churn
    c4.plotly_chart(
        _grouped_bar(df, "InternetService", "4. Internet Service vs Churn",
                     ["DSL", "Fiber optic", "No"]),
        **_OPTS,
    )
    c4.caption("Fiber optic customers churn at the highest rate, possibly due to higher costs or more competitive alternatives.")

    # ── Section 3: Billing and Payment ────────────────────────────────────────
    st.divider()
    st.markdown("### Billing and Payment")

    c5, c6 = st.columns(2)

    # Chart 5 — Monthly Charges vs Churn
    c5.plotly_chart(_box(df, "MonthlyCharges", "5. Monthly Charges vs Churn ($)"), **_OPTS)
    c5.caption("Customers who churn pay noticeably higher monthly bills. Price is a clear factor in the decision to leave.")

    # Chart 6 — Payment Method vs Churn
    pay_order = [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)",
    ]
    c6.plotly_chart(
        _grouped_bar(df, "PaymentMethod", "6. Payment Method vs Churn", pay_order),
        **_OPTS,
    )
    c6.caption("Electronic check users churn the most. Automatic payment methods are associated with greater commitment.")

    # Chart 7 — Paperless Billing vs Churn
    c7, c8 = st.columns(2)
    c7.plotly_chart(
        _grouped_bar(df, "PaperlessBilling", "7. Paperless Billing vs Churn", ["Yes", "No"]),
        **_OPTS,
    )
    c7.caption("Customers on paperless billing churn slightly more, likely because switching providers online is easier for them.")

    # ── Section 4: Demographics ───────────────────────────────────────────────
    st.divider()
    st.markdown("### Demographics")

    # Chart 8 — Senior Citizen vs Churn
    df2 = df.copy()
    df2["Senior"] = df2["SeniorCitizen"].map({0: "Non-Senior", 1: "Senior"})
    c8.plotly_chart(
        _grouped_bar(df2, "Senior", "8. Senior Citizen vs Churn", ["Non-Senior", "Senior"]),
        **_OPTS,
    )
    c8.caption("Senior citizens churn at a higher rate. They may be more sensitive to price changes or find it harder to navigate online services.")