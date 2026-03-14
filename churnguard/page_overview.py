"""
page_overview.py
Business overview — KPI cards, what churn is, and key findings.
"""

import streamlit as st
import plotly.graph_objects as go
import ui

BLUE = "#118DFF"
RED  = "#D64550"


def render(df, metrics):
    total     = len(df)
    churned   = int(df["Churn_Binary"].sum())
    rate      = churned / total
    avg_bill  = df["MonthlyCharges"].mean()
    rev_risk  = churned * avg_bill * 12
    high_risk = int((df["Churn_Risk"] > 0.7).sum())

    ui.page_title("Customer Retention Overview")
    st.write("A summary of how many customers are leaving and what it costs the business.")
    ui.divider()

    ui.kpi_row([
        {"label": "Total Customers",     "value": f"{total:,}",            "sub": "In this dataset",                   "accent": "#0078D4"},
        {"label": "Churn Rate",          "value": f"{rate*100:.1f}%",      "sub": f"{churned:,} customers lost per year","accent": "#D64550"},
        {"label": "Avg Monthly Bill",    "value": f"${avg_bill:.2f}",      "sub": "Per customer",                       "accent": "#CA5010"},
        {"label": "Revenue at Risk",     "value": f"${rev_risk:,.0f}",     "sub": "Lost annually to churn",             "accent": "#D64550"},
        {"label": "High Risk Customers", "value": f"{high_risk:,}",        "sub": "Churn probability above 70%",        "accent": "#CA5010"},
    ])

    ui.divider()

    # ── Context + donut ────────────────────────────────────────────────────────
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown("### What is Customer Churn?")
        st.write("""
            Churn is when a customer cancels their subscription and switches to a competitor.
            For telecom companies this is one of the costliest problems — acquiring a new
            customer is several times more expensive than keeping an existing one.
        """)
        st.write(f"""
            In this dataset of **{total:,} customers**, roughly **1 in 4 leaves every year**.
            With an average monthly bill of **${avg_bill:.2f}**, each customer who leaves costs
            the company about **${avg_bill * 12:,.0f} in lost annual revenue**.
            This dashboard uses exploratory analysis and a machine learning model to identify
            which customers are most likely to leave, so the team can act early.
        """)

        st.markdown("### Three Main Drivers of Churn")
        k1, k2, k3 = st.columns(3)
        k1.info("**Contract type**\n\nMonth-to-month customers churn at 42%. Customers on two-year contracts barely leave at 3%.")
        k2.info("**Internet service**\n\nFiber optic users churn at 41% — nearly double the rate of DSL customers.")
        k3.info("**Payment method**\n\nElectronic check users churn the most. Customers on auto-pay are far more loyal.")

    with col_b:
        fig = go.Figure(go.Pie(
            values=[churned, total - churned],
            labels=["Churned", "Retained"],
            hole=0.62,
            marker_colors=[RED, BLUE],
            textinfo="percent+label",
            textfont_size=11,
            showlegend=False,
        ))
        fig.add_annotation(
            text=f"<b>{rate * 100:.1f}%</b><br>churn rate",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#252423", family="IBM Plex Sans"),
        )
        fig.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            font_family="IBM Plex Sans",
            margin=dict(l=10, r=10, t=20, b=10),
            height=270,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    ui.divider()

    st.markdown("### Prediction Model at a Glance")
    st.write("A Logistic Regression model was trained to predict which customers will churn. Results:")

    acc = metrics["accuracy"]
    auc = metrics["roc_auc"]
    ui.kpi_row([
        {"label": "Algorithm",         "value": "Logistic Regression", "sub": "Trained on 6 features",         "accent": "#0078D4"},
        {"label": "Accuracy",          "value": f"{acc*100:.1f}%",     "sub": "On held-out test data",         "accent": "#107C10"},
        {"label": "ROC-AUC",           "value": f"{auc:.3f}",          "sub": "Higher is better (max 1.0)",    "accent": "#107C10"},
        {"label": "Train / Test Split","value": "80% / 20%",           "sub": "1,409 customers in test set",   "accent": "#0078D4"},
    ])