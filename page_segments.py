"""
page_segments.py
RFM segmentation charts and segment reference guide.
Enhanced StockPulse-style design.
"""

import streamlit as st
import plotly.graph_objects as go
import ui

SEG_ORDER  = [
    "Champions", "Loyal Customers", "At-Risk Customers",
    "Hibernating Customers", "Lost Customers",
]
SEG_COLORS = {
    "Champions":             "#107C10",
    "Loyal Customers":       "#0078D4",
    "At-Risk Customers":     "#CA5010",
    "Hibernating Customers": "#D64550",
    "Lost Customers":        "#605E5C",
}

# rgba fill versions for Plotly box plots (13% opacity)
SEG_FILLS = {
    "Champions":             "rgba(16,124,16,0.13)",
    "Loyal Customers":       "rgba(0,120,212,0.13)",
    "At-Risk Customers":     "rgba(202,80,16,0.13)",
    "Hibernating Customers": "rgba(214,69,80,0.13)",
    "Lost Customers":        "rgba(161,159,157,0.13)",
}
SEG_LIST = list(SEG_COLORS.values())

_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_family="DM Sans",
    font_color="#252423",
    margin=dict(l=12, r=12, t=44, b=96),
    xaxis=dict(
        gridcolor="#F3F2F1",
        linecolor="#EDEBE9",
        tickfont=dict(size=10.5),
        tickangle=-20,
        showgrid=False,
    ),
    yaxis=dict(
        gridcolor="#F3F2F1",
        linecolor="#EDEBE9",
        tickfont=dict(size=11),
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

_OPTS  = dict(use_container_width=True, config={"displayModeBar": False})
_CARD  = (
    '<div style="background:#FFFFFF;border:1px solid #EDEBE9;'
    'border-radius:8px;padding:4px 4px 0;'
    'box-shadow:0 1px 5px rgba(0,0,0,0.05);">'
)


def render(df):
    ui.page_title(
        "Customer Segments",
        "Customers grouped by Recency, Frequency and Monetary (RFM) score.",
    )

    # ── Segment summary strip ─────────────────────────────────────────────────
    seg_counts = df["Segment"].value_counts()
    ui.segment_badge_row(seg_counts.to_dict(), SEG_COLORS)

    # ── Charts ────────────────────────────────────────────────────────────────
    ui.section("Segment Distribution and Churn Risk")
    c1, c2 = st.columns(2)

    counts = df["Segment"].value_counts().reindex(SEG_ORDER).fillna(0)
    fig1 = go.Figure(go.Bar(
        x=SEG_ORDER,
        y=counts.values,
        marker_color=SEG_LIST,
        marker_line_width=0,
        opacity=0.92,
        text=counts.values.astype(int),
        textposition="outside",
        textfont=dict(size=11, family="DM Mono"),
    ))
    fig1.update_layout(**_BASE, title_text="Customer Segment Distribution", height=360)
    fig1.update_yaxes(title="Number of Customers")

    c1.markdown(_CARD, unsafe_allow_html=True)
    c1.plotly_chart(fig1, **_OPTS)
    c1.markdown("</div>", unsafe_allow_html=True)
    ui.caption(
        "Based on RFM scoring: Recency (tenure), Frequency (services used), Monetary (total spend)."
    )

    fig2 = go.Figure()
    for seg, color in SEG_COLORS.items():
        vals = df[df["Segment"] == seg]["Churn_Risk"]
        if len(vals):
            fig2.add_trace(go.Box(
                y=vals,
                name=seg,
                marker_color=color,
                fillcolor=SEG_FILLS[seg],
                line_color=color,
                boxpoints=False,
                whiskerwidth=0.5,
            ))
    fig2.update_layout(**_BASE, title_text="Churn Risk Score by Segment", height=360)
    fig2.update_yaxes(title="Churn Risk Probability", tickformat=".0%")

    c2.markdown(_CARD, unsafe_allow_html=True)
    c2.plotly_chart(fig2, **_OPTS)
    c2.markdown("</div>", unsafe_allow_html=True)
    ui.caption(
        "Higher RFM score = lower churn risk. "
        "At-Risk and Hibernating segments need immediate attention."
    )

    ui.divider()

    # ── Segment reference ─────────────────────────────────────────────────────
    ui.section("What Each Segment Means")

    segments = [
        (
            "Champions", "#107C10", "Very Low",
            "Long tenure, high service usage, highest total spend. The most valuable customers.",
            "Reward with loyalty perks. Offer early renewal deals and premium upgrades.",
        ),
        (
            "Loyal Customers", "#0078D4", "Low",
            "Solid long-term relationship with good service usage. Reliable and consistent.",
            "Offer contract renewal incentives and bundled service discounts.",
        ),
        (
            "At-Risk Customers", "#CA5010", "Medium",
            "Shorter tenure and fewer services. Early signs of disengagement are visible.",
            "Proactive outreach. Offer a 15–20% discount or a free service upgrade.",
        ),
        (
            "Hibernating Customers", "#D64550", "High",
            "Low engagement and low spending. Not taking advantage of available services.",
            "Win-back campaign with a limited-time bundle offer or free month.",
        ),
        (
            "Lost Customers", "#605E5C", "Very High",
            "Very new or fully disengaged. Highest probability of leaving imminently.",
            "Immediate contact with a strong retention incentive.",
        ),
    ]

    for name, color, risk, desc, action in segments:
        ui.expander(name, f"""
            <div style='display:grid;grid-template-columns:2.2fr 0.7fr 1.6fr;gap:20px;
                        font-size:0.83rem;color:#605E5C;'>
                <div>
                    <b style='color:#252423;display:block;margin-bottom:5px;'>Description</b>
                    {desc}
                </div>
                <div>
                    <b style='color:#252423;display:block;margin-bottom:5px;'>Churn Risk</b>
                    <span style='color:{color};font-weight:700;'>{risk}</span>
                </div>
                <div>
                    <b style='color:#252423;display:block;margin-bottom:5px;'>Recommended Action</b>
                    {action}
                </div>
            </div>
        """)