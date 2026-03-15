"""
data.py
Load and prepare the Telco dataset.
All steps copied directly from 03_model.ipynb.
"""

import os
import pandas as pd
import streamlit as st


SERVICES = [
    "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies",
]


def _find_csv():
    base = os.path.dirname(os.path.abspath(__file__))
    for p in [
        os.path.join(base, "Telco-Customer-Churn.csv"),
        os.path.join(base, "data", "Telco-Customer-Churn.csv"),
    ]:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        "Place Telco-Customer-Churn.csv next to app.py or inside a data/ folder."
    )


@st.cache_data
def load_data():
    df = pd.read_csv(_find_csv())

    # --- from 03_model.ipynb: Data Cleaning ---
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"] * df["tenure"])

    # Keep original Churn column ('Yes'/'No') for charts; add numeric version for model
    df["Churn_Binary"] = (df["Churn"] == "Yes").astype(int)

    # --- from 03_model.ipynb: Service Count ---
    df["Service_Count"] = df[SERVICES].apply(lambda x: (x == "Yes").sum(), axis=1)

    # --- from 03_model.ipynb: RFM Features ---
    df["Recency"]   = df["tenure"]
    df["Frequency"] = df["Service_Count"]
    df["Monetary"]  = df["TotalCharges"]

    # --- from 03_model.ipynb: RFM Scoring ---
    df["Recency_Score"]   = pd.qcut(df["Recency"],  5, labels=[5, 4, 3, 2, 1], duplicates="drop")
    df["Frequency_Score"] = pd.qcut(df["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    df["Monetary_Score"]  = pd.qcut(df["Monetary"],  5, labels=[1, 2, 3, 4, 5], duplicates="drop")

    for col in ["Recency_Score", "Frequency_Score", "Monetary_Score"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(3).astype(int)

    df["RFM_Score"] = df["Recency_Score"] + df["Frequency_Score"] + df["Monetary_Score"]

    # --- from 03_model.ipynb: Customer Segmentation ---
    def rfm_segment(score):
        if score >= 13:   return "Champions"
        elif score >= 10: return "Loyal Customers"
        elif score >= 7:  return "At-Risk Customers"
        elif score >= 4:  return "Hibernating Customers"
        else:             return "Lost Customers"

    df["Segment"] = df["RFM_Score"].apply(rfm_segment)

    return df
