import streamlit as st
from agents.orchestrator import run_finsight_ui
from utils.database import init_db, save_report, get_all_reports

st.set_page_config(page_title="FinSight", page_icon="💰", layout="centered")
init_db()

st.title("💰 FinSight — AI Personal Finance Advisor")
st.markdown("Tell us about yourself and get a **complete financial plan instantly!**")

user_name = st.text_input("உன் பெயர்", value="Devi")

st.divider()

col1, col2 = st.columns(2)
with col1:
    income   = st.number_input("Monthly Income (₹)", min_value=0, value=40000, step=1000)
    expenses = st.number_input("Monthly Expenses (₹)", min_value=0, value=28000, step=1000)
with col2:
    savings_goal = st.number_input("Monthly Savings Goal (₹)", min_value=0, value=5000, step=500)
    sip_amount   = st.number_input("SIP Amount per month (₹)", min_value=0, value=3000, step=500)

col3, col4 = st.columns(2)
with col3:
    stock = st.text_input("Stock to track (NSE)", value="RELIANCE")
with col4:
    years = st.slider("Investment period (years)", 1, 30, 10)

risk_level = st.radio("Your risk appetite", ["low", "medium", "high"], horizontal=True)

st.divider()

if st.button("🚀 Generate My Financial Plan", use_container_width=True):
    with st.spinner("FinSight agents are analysing your finances..."):
        result = run_finsight_ui(
            income=income,
            expenses=expenses,
            savings_goal=savings_goal,
            risk_level=risk_level,
            stock=stock,
            sip_amount=sip_amount,
            years=years
        )

    st.success("✅ Your personalised financial plan is ready!")

    st.subheader("📈 Live Market Data")
    st.info(result["market"])

    st.subheader("💰 Budget Analysis")
    surplus = income - expenses
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Surplus",  f"₹{surplus:,}")
    col2.metric("Savings Rate",     f"{round((surplus/income)*100, 1)}%")
    col3.metric("Goal Status",      "✅ Met" if surplus >= savings_goal else "❌ Shortfall")
    st.info(result["budget"])

    st.subheader("📊 Investment Plan")
    st.success(result["investments"])

    st.subheader("⚠️ Risk Report")
    score = int(result["risk_score"].split("/")[0])
    st.progress(score / 8)
    if score >= 7:
        st.success(result["risk_details"])
    elif score >= 4:
        st.warning(result["risk_details"])
    else:
        st.error(result["risk_details"])

    save_report(
        name=user_name,
        income=income,
        expenses=expenses,
        surplus=surplus,
        savings_rate=round((surplus / income) * 100, 1),
        risk_score=result["risk_score"],
        investment_plan=result["investments"]
    )
    st.toast("💾 Report saved to history!")

st.divider()
st.subheader("📋 Past Reports History")
reports = get_all_reports()
if reports:
    import pandas as pd
    df = pd.DataFrame(reports, columns=[
        "Name", "Income", "Expenses",
        "Surplus", "Savings Rate", "Risk Score", "Date"
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info("இன்னும் எந்த report உம் save ஆகல்ல — Generate பண்ணு!")