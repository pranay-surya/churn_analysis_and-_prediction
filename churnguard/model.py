"""
model.py
Train the churn model and score all customers.
All ML steps copied directly from 03_model.ipynb.
"""

import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score, roc_curve,
)


FEATURES = [
    "tenure", "MonthlyCharges", "TotalCharges",
    "SeniorCitizen", "Service_Count", "RFM_Score",
]

SEGMENT_ACTIONS = {
    "Champions":             "Top customer. Reward with loyalty perks and early renewal offers.",
    "Loyal Customers":       "Stable customer. Offer service bundles and contract upgrades.",
    "At-Risk Customers":     "Needs attention. Consider a 15–20% discount or free service upgrade.",
    "Hibernating Customers": "Disengaged. Run a win-back campaign with a limited-time offer.",
    "Lost Customers":        "Very high risk. Immediate outreach with a strong incentive.",
}


@st.cache_data
def train_model(_df):
    """
    Trains Logistic Regression — exact code from 03_model.ipynb.
    Returns (model, scaler, df_with_risk, metrics).
    """
    df = _df.copy()

    # --- from 03_model.ipynb: Prepare Dataset ---
    X = df[FEATURES]
    y = df["Churn_Binary"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # --- from 03_model.ipynb: Feature Scaling ---
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # --- from 03_model.ipynb: Logistic Regression ---
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # --- from 03_model.ipynb: Prediction & Evaluation ---
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    # --- from 03_model.ipynb: Churn Probability Score for all customers ---
    df["Churn_Risk"] = model.predict_proba(scaler.transform(X))[:, 1]

    # --- from 03_model.ipynb: Feature Importance ---
    importance = pd.DataFrame({
        "Feature":     FEATURES,
        "Coefficient": model.coef_[0],
    }).sort_values("Coefficient").reset_index(drop=True)

    fpr, tpr, _ = roc_curve(y_test, y_prob)

    metrics = {
        "accuracy":   accuracy_score(y_test, y_pred),
        "roc_auc":    roc_auc_score(y_test, y_prob),
        "cm":         confusion_matrix(y_test, y_pred),
        "report":     classification_report(y_test, y_pred, output_dict=True),
        "importance": importance,
        "fpr":        fpr,
        "tpr":        tpr,
    }

    return model, scaler, df, metrics


def rfm_segment(score):
    if score >= 13:   return "Champions"
    elif score >= 10: return "Loyal Customers"
    elif score >= 7:  return "At-Risk Customers"
    elif score >= 4:  return "Hibernating Customers"
    else:             return "Lost Customers"


def predict_customer(model, scaler, df, tenure, monthly, senior, service_count):
    """
    Predict churn probability for one new customer.
    RFM score is estimated by comparing against the training data distribution.
    """
    total_charges = monthly * tenure

    # Score each RFM dimension using percentile rank against training data
    r = max(1, min(5, round((1 - (df["Recency"]   < tenure)        .mean()) * 4 + 1)))
    f = max(1, min(5, round((    (df["Frequency"]  < service_count) .mean()) * 4 + 1)))
    m = max(1, min(5, round((    (df["Monetary"]   < total_charges) .mean()) * 4 + 1)))
    rfm = r + f + m

    row = pd.DataFrame(
        [[tenure, monthly, total_charges, int(senior), service_count, rfm]],
        columns=FEATURES,
    )
    probability = model.predict_proba(scaler.transform(row))[0][1]
    segment     = rfm_segment(rfm)

    return round(probability * 100, 1), segment
