"""
page_segments.py
RFM segmentation charts from 03_model.ipynb.
Charts: segment distribution + churn risk by segment.
"""

import streamlit as st
import plotly.graph_objects as go
import ui

SEG_ORDER = [
    "Champions",
    "Loyal Customers",
    "At-Risk Customers",
    "Hibernating Customers",
    "Lost Customers",
]

SEG_COLORS = ["#107C10", "#118DFF", "#CA5010", "#D64550", "#605E5C"]

_L = dict(
    paper_bgcolor = "white",
    plot_bgcolor  = "white",
    font_family   = "IBM Plex Sans",
    font_color    = "#252423",
    height        = 340,
    margin        = dict(l=10, r=10, t=38, b=90),
    xaxis         = dict(gridcolor="#EDEBE9", linecolor="#EDEBE9", tickangle=-20),
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


def render(df):
    st.markdown("# Customer Segments")
    st.write("""
        Customers are grouped using RFM Analysis — a scoring method based on three factors:
        how recently they joined (Recency), how many services they use (Frequency),
        and how much they have paid in total (Monetary).
        A combined score places each customer into one of five groups.
    """)
    st.divider()

    # ── Two charts from notebook 3 ─────────────────────────────────────────────
    c1, c2 = st.columns(2)

    # Chart: Customer Segments Distribution (sns.countplot on Segment)
    seg_counts = df["Segment"].value_counts().reindex(SEG_ORDER).fillna(0)
    fig1 = go.Figure(go.Bar(
        x=SEG_ORDER,
        y=seg_counts.values,
        marker_color=SEG_COLORS,
        text=seg_counts.values.astype(int),
        textposition="outside",
    ))
    fig1.update_layout(**_L, title_text="Customer Segments Distribution")
    fig1.update_yaxes(title="Number of Customers")
    c1.plotly_chart(fig1, **_OPTS)

    # Chart: Churn Risk by Segment (sns.boxplot on Churn_Risk)
    fig2 = go.Figure()
    for seg, color in zip(SEG_ORDER, SEG_COLORS):
        vals = df[df["Segment"] == seg]["Churn_Risk"]
        if len(vals) > 0:
            fig2.add_trace(go.Box(
                y=vals, name=seg,
                marker_color=color,
                boxpoints=False,
            ))
    fig2.update_layout(**_L, title_text="Churn Risk Score by Segment")
    fig2.update_yaxes(title="Churn Risk Probability", tickformat=".0%")
    c2.plotly_chart(fig2, **_OPTS)

    st.divider()

    # ── Segment descriptions ───────────────────────────────────────────────────
    st.markdown("### What Each Segment Means")

    segments = [
        ("Champions",             SEG_COLORS[0], "High RFM score",  "Very Low",  "Been with the company a long time, use many services, spend the most.",             "Reward with loyalty perks. Upsell to premium plans."),
        ("Loyal Customers",       SEG_COLORS[1], "Good RFM score",  "Low",       "Solid, long-term relationship with decent service usage.",                          "Offer early contract renewal and service bundles."),
        ("At-Risk Customers",     SEG_COLORS[2], "Mid RFM score",   "Medium",    "Shorter tenure and fewer services. Starting to show signs of disengagement.",       "Reach out proactively with a discount or upgrade offer."),
        ("Hibernating Customers", SEG_COLORS[3], "Low RFM score",   "High",      "Low engagement and low spending. Have not taken advantage of available services.",  "Run a win-back campaign with a limited-time bundle deal."),
        ("Lost Customers",        SEG_COLORS[4], "Lowest RFM score","Very High", "Very new or completely disengaged. Highest risk of leaving imminently.",            "Immediate outreach. Offer a strong incentive to stay."),
    ]

    for name, color, score, risk, desc, action in segments:
        ui.expander(name, f"""
            <div style='display:grid; grid-template-columns:2fr 1fr 1fr; gap:16px; font-size:0.84rem; color:#605E5C;'>
                <div><b style='color:#252423;'>Description</b><br>{desc}</div>
                <div><b style='color:#252423;'>Churn risk</b><br>{risk}</div>
                <div><b style='color:#252423;'>Recommended action</b><br>{action}</div>
            </div>
        """)