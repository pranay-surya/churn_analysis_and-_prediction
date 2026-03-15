"""
page_overview.py
Business overview — KPI cards, drivers, donut, model summary.
Enhanced StockPulse-style design.
"""

import streamlit as st
import plotly.graph_objects as go
import ui

BLUE = "#0078D4"
RED  = "#D64550"


def render(df, metrics):
    total = len(df)
    if total == 0:
        st.warning("No customer data available.")
        return

    required_cols = {"Churn_Binary", "MonthlyCharges", "Churn_Risk"}
    missing_cols  = required_cols - set(df.columns)
    if missing_cols:
        st.error(f"Missing columns in dataset: {', '.join(missing_cols)}")
        return

    churned   = int(df["Churn_Binary"].sum())
    rate      = churned / total
    avg_bill  = df["MonthlyCharges"].mean()
    rev_risk  = churned * avg_bill * 12
    high_risk = int((df["Churn_Risk"] > 0.7).sum())

    acc = metrics.get("accuracy", 0)
    auc = metrics.get("roc_auc",  0)

    one_in_n       = round(1 / rate) if rate > 0 else "N/A"
    test_set_count = int(total * 0.2)

    ui.page_title(
        "Customer Retention Overview",
        "How many customers are leaving, what it costs, and what the model predicts.",
    )

    # ── KPI row ────────────────────────────────────────────────────────────────
    ui.kpi_row([
        {"label": "Total Customers",     "value": f"{total:,}",        "sub": "In the dataset",                "accent": "#0078D4"},
        {"label": "Churn Rate",          "value": f"{rate*100:.1f}%",  "sub": f"{churned:,} customers per year","accent": "#D64550"},
        {"label": "Avg Monthly Bill",    "value": f"${avg_bill:.2f}",  "sub": "Per customer",                  "accent": "#CA5010"},
        {"label": "Revenue at Risk",     "value": f"${rev_risk:,.0f}", "sub": "Lost annually to churn",        "accent": "#D64550"},
        {"label": "High Risk Customers", "value": f"{high_risk:,}",    "sub": "Churn probability above 70%",   "accent": "#CA5010"},
    ])

    ui.divider()

    # ── Context + donut ────────────────────────────────────────────────────────
    col_a, col_b = st.columns([2.2, 1])

    with col_a:
        ui.section("What is Customer Churn?")
        st.markdown(
            "<p style='font-size:0.9rem;color:#252423;line-height:1.75;margin:0 0 12px 0;'>"
            "Churn is when a customer cancels their subscription and moves to a competitor. "
            "For telecom companies this is one of the costliest problems &#8212; acquiring a new "
            "customer is several times more expensive than keeping an existing one.</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='font-size:0.9rem;color:#252423;line-height:1.75;margin:0;'>"
            f"In this dataset of <b>{total:,} customers</b>, roughly "
            f"<b>1&nbsp;in&nbsp;{one_in_n} leaves every year</b>. "
            f"With an average monthly bill of <b>&#36;{avg_bill:.2f}</b>, each departing customer "
            f"costs the company about <b>&#36;{avg_bill*12:,.0f} in lost annual revenue</b>. "
            f"This dashboard uses exploratory analysis and a machine learning model to find "
            f"which customers are most likely to leave, so the team can act before it happens.</p>",
            unsafe_allow_html=True,
        )

        ui.section("Three Main Drivers of Churn")
        ui.driver_cards([
            (
                "Contract Type",
                "Month-to-month customers churn at 42%. Customers on two-year contracts barely leave at 3%. "
                "The absence of commitment makes switching easy.",
            ),
            (
                "Internet Service",
                "Fiber optic users churn at 41% — nearly double the rate of DSL customers. "
                "Higher costs and more competitive alternatives likely drive this.",
            ),
            (
                "Payment Method",
                "Electronic check users churn the most. Customers on automatic bank transfer or "
                "credit card payment are significantly more loyal.",
            ),
        ])

    with col_b:
        ui.section("Overall Churn Split")

        # Donut chart
        fig = go.Figure(go.Pie(
            values=[churned, total - churned],
            labels=["Churned", "Retained"],
            hole=0.66,
            marker=dict(
                colors=[RED, BLUE],
                line=dict(color="white", width=2),
            ),
            textinfo="percent+label",
            textfont=dict(size=11, family="DM Sans"),
            showlegend=False,
            direction="clockwise",
            sort=False,
        ))
        fig.add_annotation(
            text=f"<b style='font-size:15px'>{rate*100:.1f}%</b><br>"
                 f"<span style='font-size:11px;color:#605E5C'>churn rate</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="DM Mono", color="#252423"),
        )
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_family="DM Sans",
            margin=dict(l=10, r=10, t=10, b=10),
            height=250,
            shapes=[dict(
                type="rect", xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="#EDEBE9", width=1),
                fillcolor="rgba(0,0,0,0)", layer="above",
            )],
        )

        # Wrap in card
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #EDEBE9;'
            'border-radius:8px;padding:4px 4px 0;'
            'box-shadow:0 1px 5px rgba(0,0,0,0.05);">',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        ui.stat_row([
            ("Retained", f"{total - churned:,}"),
            ("Churned",  f"{churned:,}"),
        ])

    ui.divider()

    # ── Model summary ──────────────────────────────────────────────────────────
    ui.section("Prediction Model at a Glance")
    st.write(
        "A Logistic Regression model was trained on 80% of the data and evaluated on the "
        "remaining 20%. It predicts the probability that each customer will churn."
    )
    ui.kpi_row([
        {"label": "Algorithm",          "value": "Logistic Reg.",  "sub": "Trained on 6 features",                     "accent": "#0078D4"},
        {"label": "Accuracy",           "value": f"{acc*100:.1f}%","sub": "On the held-out test set",                  "accent": "#107C10"},
        {"label": "ROC-AUC Score",      "value": f"{auc:.3f}",     "sub": "Higher is better (max 1.0)",                "accent": "#107C10"},
        {"label": "Train / Test Split", "value": "80% / 20%",      "sub": f"{test_set_count:,} customers in test set", "accent": "#0078D4"},
    ])