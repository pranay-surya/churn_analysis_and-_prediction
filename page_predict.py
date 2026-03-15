"""
page_predict.py
Predict churn risk for a new customer.
Enhanced StockPulse-style design.
"""

import streamlit as st
import ui
from model import predict_customer, SEGMENT_ACTIONS

ALL_SERVICES = [
    "Phone Service", "Multiple Lines", "Online Security",
    "Online Backup", "Device Protection", "Tech Support",
    "Streaming TV", "Streaming Movies",
]

_LABEL_STYLE = (
    "font-size:0.65rem;font-weight:700;color:#252423;"
    "text-transform:uppercase;letter-spacing:.09em;margin-bottom:10px;"
)


def render(model, scaler, df):
    ui.page_title(
        "Churn Risk Predictor",
        "Enter a customer's details to get their churn probability from the trained model.",
    )

    # ── Input panel ────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="background:#FFFFFF;border:1px solid #EDEBE9;border-radius:10px;'
        'padding:24px 26px 20px;box-shadow:0 1px 6px rgba(0,0,0,0.05);'
        'margin-bottom:20px;">',
        unsafe_allow_html=True,
    )

    ui.section("Customer Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div style="{_LABEL_STYLE}">Account</div>', unsafe_allow_html=True)
        tenure  = st.slider("Months with the company", 1, 72, 12)
        monthly = st.number_input(
            "Monthly bill ($)", min_value=18.0, max_value=120.0, value=65.0, step=0.5,
        )
        senior = st.checkbox("Senior citizen (age 65+)")

    with col2:
        st.markdown(f'<div style="{_LABEL_STYLE}">Active Services</div>', unsafe_allow_html=True)
        selected      = st.multiselect("Select services", ALL_SERVICES, default=["Phone Service"])
        service_count = len(selected)
        ui.caption(f"{service_count} of {len(ALL_SERVICES)} services selected")

    with col3:
        st.markdown(f'<div style="{_LABEL_STYLE}">Summary</div>', unsafe_allow_html=True)

        # Mini stat cards
        st.markdown(
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;">'
            f'<div style="background:#F3F2F1;border:1px solid #EDEBE9;border-radius:6px;'
            f'padding:10px 12px;">'
            f'<div style="font-size:0.6rem;font-weight:700;color:#605E5C;'
            f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Tenure</div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:#252423;'
            f'font-family:\'DM Mono\',monospace;">{tenure}m</div></div>'
            f'<div style="background:#F3F2F1;border:1px solid #EDEBE9;border-radius:6px;'
            f'padding:10px 12px;">'
            f'<div style="font-size:0.6rem;font-weight:700;color:#605E5C;'
            f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Total Paid</div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:#252423;'
            f'font-family:\'DM Mono\',monospace;">${monthly*tenure:,.0f}</div></div>'
            f'<div style="background:#F3F2F1;border:1px solid #EDEBE9;border-radius:6px;'
            f'padding:10px 12px;">'
            f'<div style="font-size:0.6rem;font-weight:700;color:#605E5C;'
            f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Services</div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:#252423;'
            f'font-family:\'DM Mono\',monospace;">{service_count}</div></div>'
            f'<div style="background:#F3F2F1;border:1px solid #EDEBE9;border-radius:6px;'
            f'padding:10px 12px;">'
            f'<div style="font-size:0.6rem;font-weight:700;color:#605E5C;'
            f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Monthly</div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:#252423;'
            f'font-family:\'DM Mono\',monospace;">${monthly:.0f}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        run = st.button("⚡  Calculate Churn Risk", type="primary", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Result ─────────────────────────────────────────────────────────────────
    if run:
        risk_pct, segment = predict_customer(
            model, scaler, df, tenure, monthly, int(senior), service_count,
        )

        ui.section("Prediction Result")
        r1, r2 = st.columns([1, 1.6])

        with r1:
            ui.result_card(risk_pct, segment, monthly)

        with r2:
            if risk_pct > 70:
                ui.info_box(
                    f"<b>High risk — act now.</b> This customer has a {risk_pct:.1f}% probability "
                    f"of leaving. A direct call, a discount offer, or a contract upgrade incentive "
                    f"should be arranged within the next few days.",
                    kind="error",
                )
            elif risk_pct > 40:
                ui.info_box(
                    f"<b>Medium risk — monitor this customer.</b> Churn probability is {risk_pct:.1f}%. "
                    f"A proactive check-in or a small loyalty reward could prevent them from leaving.",
                    kind="warning",
                )
            else:
                ui.info_box(
                    f"<b>Low risk — customer is stable.</b> Only a {risk_pct:.1f}% chance of leaving. "
                    f"No immediate action required. Focus retention efforts on higher-risk accounts.",
                    kind="success",
                )

            action = SEGMENT_ACTIONS.get(segment, "")
            ui.info_box(
                f"<b>Segment recommendation — {segment}:</b> {action}",
                kind="info",
            )

        ui.expander("Model inputs used for this prediction", f"""
            <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:12px;
                        font-size:0.83rem;color:#605E5C;'>
                <div><b style='color:#252423;'>Tenure</b><br>{tenure} months</div>
                <div><b style='color:#252423;'>Monthly charges</b><br>${monthly:.2f}</div>
                <div><b style='color:#252423;'>Total charges</b><br>${monthly*tenure:,.2f}</div>
                <div><b style='color:#252423;'>Senior citizen</b><br>{'Yes' if senior else 'No'}</div>
                <div><b style='color:#252423;'>Service count</b><br>{service_count}</div>
            </div>
        """)