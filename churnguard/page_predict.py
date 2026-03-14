"""
page_predict.py
Enter a customer's details and get their churn probability from the trained model.
"""

import streamlit as st
import ui
from model import predict_customer, SEGMENT_ACTIONS

ALL_SERVICES = [
    "Phone Service",
    "Multiple Lines",
    "Online Security",
    "Online Backup",
    "Device Protection",
    "Tech Support",
    "Streaming TV",
    "Streaming Movies",
]


def render(model, scaler, df):
    ui.page_title("Churn Risk Predictor")
    st.write("Fill in the details below to see how likely a customer is to cancel their service.")
    ui.divider()

    # ── Input form ─────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Account")
        tenure  = st.slider("Months with the company", 1, 72, 12)
        monthly = st.number_input("Monthly bill ($)", min_value=18.0, max_value=120.0,
                                  value=65.0, step=0.5)
        senior  = st.checkbox("Senior citizen (age 65+)")

    with col2:
        st.markdown("#### Active Services")
        selected      = st.multiselect("Services this customer has", ALL_SERVICES,
                                       default=["Phone Service"])
        service_count = len(selected)
        st.caption(f"{service_count} service(s) selected")

    with col3:
        total_est = monthly * tenure
        st.markdown("#### Calculated Values")
        ui.kpi_row([
            {"label": "Months on service",     "value": str(tenure),             "accent": "#0078D4"},
            {"label": "Estimated total paid",  "value": f"${total_est:,.2f}",    "accent": "#0078D4"},
            {"label": "Number of services",    "value": str(service_count),      "accent": "#0078D4"},
        ])

    st.divider()

    # ── Predict button ─────────────────────────────────────────────────────────
    if st.button("Calculate Churn Risk", type="primary"):

        risk_pct, segment = predict_customer(
            model, scaler, df,
            tenure, monthly, int(senior), service_count,
        )

        ui.kpi_row([
            {"label": "Churn Probability", "value": f"{risk_pct:.1f}%",   "accent": "#D64550" if risk_pct > 40 else "#107C10"},
            {"label": "Customer Segment",  "value": segment,              "accent": "#0078D4"},
            {"label": "Monthly Bill",      "value": f"${monthly:.2f}",    "accent": "#0078D4"},
        ])

        ui.divider()

        if risk_pct > 70:
            ui.info_box(
                f"<b>High risk — act now.</b> This customer has a {risk_pct:.1f}% chance of leaving. "
                f"Consider a direct call, a discount offer, or a contract upgrade incentive.",
                kind="error",
            )
        elif risk_pct > 40:
            ui.info_box(
                f"<b>Medium risk — keep an eye on this customer.</b> Churn probability is {risk_pct:.1f}%. "
                f"A proactive check-in or small loyalty reward could make a difference.",
                kind="warning",
            )
        else:
            ui.info_box(
                f"<b>Low risk — customer is stable.</b> Only a {risk_pct:.1f}% chance of leaving. "
                f"Focus retention efforts elsewhere.",
                kind="success",
            )

        action = SEGMENT_ACTIONS.get(segment, "")
        ui.info_box(f"<b>Segment: {segment}</b> — {action}", kind="info")

        # ── What the model used ────────────────────────────────────────────────
        ui.expander("Show inputs used by the model", f"""
            <div style='font-size:0.84rem; color:#605E5C; line-height:2;'>
                <b style='color:#252423;'>Tenure (months):</b> {tenure}<br>
                <b style='color:#252423;'>Monthly charges:</b> ${monthly:.2f}<br>
                <b style='color:#252423;'>Total charges:</b> ${monthly * tenure:,.2f}<br>
                <b style='color:#252423;'>Senior citizen:</b> {'Yes' if senior else 'No'}<br>
                <b style='color:#252423;'>Service count:</b> {service_count}
            </div>
        """)