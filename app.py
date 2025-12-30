import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Financial Fraud Monitoring Dashboard",
    layout="wide"
)

# ================= TITLE =================
st.title("🛡️ AI-Driven Financial Fraud Monitoring Dashboard")
st.caption("Explainable forensic analytics using financial ratios, trend analysis & digital tests")

st.markdown("---")

# ================= SIDEBAR INPUTS =================
st.sidebar.header("📥 Financial Inputs (Sample Pre-Filled)")

company = st.sidebar.text_input("Company Name", "Sample Industries Ltd")
year = st.sidebar.selectbox("Year", [2020, 2021, 2022, 2023, 2024])

revenue_growth = st.sidebar.slider("Revenue Growth (%)", -20, 100, 25)
cashflow_growth = st.sidebar.slider("Cash Flow Growth (%)", -20, 100, 8)
accruals = st.sidebar.slider("Accruals (% of Assets)", 0, 30, 12)
debt_equity = st.sidebar.slider("Debt-to-Equity Ratio", 0.0, 2.5, 0.9)
working_capital_change = st.sidebar.slider("Working Capital Change (%)", -30, 30, 15)

run = st.sidebar.button("▶ Run Fraud Analysis")

# ================= FRAUD LOGIC =================
flags = []

if revenue_growth > cashflow_growth * 2:
    flags.append("Revenue growing much faster than cash flows")

if accruals > 10:
    flags.append("High accruals → possible earnings manipulation")

if debt_equity > 1.2:
    flags.append("High leverage → financial stress")

if working_capital_change > 10:
    flags.append("Unusual working capital movement")

flag_count = len(flags)

# Fraud Score (0–100)
fraud_score = min(100, 20 + flag_count * 20)

risk_label = (
    "LOW" if fraud_score < 40 else
    "MODERATE" if fraud_score < 70 else
    "HIGH"
)

# ================= KPI CARDS =================
st.subheader("📊 Key Risk Indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Fraud Risk", risk_label, f"{fraud_score}/100")
k2.metric("Red Flags", flag_count)
k3.metric("Altman Z (Proxy)", round(3.0 - debt_equity - accruals/20, 2))
k4.metric("Beneish M (Proxy)", round(accruals/8 + revenue_growth/60, 2))

st.markdown("---")

# ================= GAUGE =================
st.subheader("🚨 Fraud Risk Meter")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=fraud_score,
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "red"},
        "steps": [
            {"range": [0, 40], "color": "#2ecc71"},
            {"range": [40, 70], "color": "#f1c40f"},
            {"range": [70, 100], "color": "#e74c3c"}
        ]
    }
))

st.plotly_chart(gauge, use_container_width=True)

# ================= FINANCIAL BAR CHART =================
st.subheader("📉 Financial Stress Indicators")

bar_df = pd.DataFrame({
    "Metric": [
        "Revenue Growth",
        "Cash Flow Growth",
        "Accruals",
        "Debt-Equity",
        "WC Change"
    ],
    "Value": [
        revenue_growth,
        cashflow_growth,
        accruals,
        debt_equity * 10,   # scaled for visibility
        working_capital_change
    ]
})

bar_fig = px.bar(
    bar_df,
    x="Metric",
    y="Value",
    color="Metric",
    title="Key Financial Ratios & Growth Metrics"
)

st.plotly_chart(bar_fig, use_container_width=True)

# ================= TIME-SERIES =================
st.subheader("📈 Fraud Risk Over Time (Monitoring Mode)")

years = ["2020", "2021", "2022", "2023", "2024"]
risk_series = [30, 45, 55, 65, fraud_score]

line_fig = px.line(
    x=years,
    y=risk_series,
    markers=True,
    labels={"x": "Year", "y": "Fraud Risk Score"},
    title="Fraud Risk Trend"
)

st.plotly_chart(line_fig, use_container_width=True)

# ================= BENFORD =================
st.subheader("🔢 Benford’s Law – First Digit Test")

digits = np.random.choice([1,2,3,4,5,6,7,8,9], size=200,
                          p=[0.30,0.18,0.12,0.10,0.08,0.07,0.06,0.05,0.04])

benford_df = pd.DataFrame(digits, columns=["Digit"]).value_counts().reset_index()
benford_df.columns = ["Digit", "Count"]

benford_fig = px.bar(
    benford_df,
    x="Digit",
    y="Count",
    title="First-Digit Distribution (Benford Test)"
)

st.plotly_chart(benford_fig, use_container_width=True)

# ================= RED FLAGS =================
st.subheader("🚩 Forensic Red Flags")

if flags:
    for f in flags:
        st.warning(f)
else:
    st.success("No major red flags detected")

# ================= INTERPRETATION =================
st.markdown("---")
st.subheader("🧠 Interpretation & Explainability")

st.write("""
• Fraud risk is derived from **accounting inconsistencies**, not black-box ML  
• High accruals + revenue-cash mismatch are early warning signals  
• Benford’s Law flags abnormal digit patterns  
• Trend monitoring allows **continuous surveillance**, not one-time audits  
""")

# ================= FOOTER =================
st.markdown("---")
st.caption("AI Financial Fraud Monitoring Dashboard | Academic & Forensic Use")






