import streamlit as st
from agents.orchestrator import run_finsight_ui
from utils.database import init_db, save_report, get_all_reports

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_db()

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500;600&display=swap');

* { font-family: 'DM Sans', sans-serif; }

.main { background: #0a0f1e; }
.block-container { padding: 2rem 3rem; max-width: 1100px; margin: auto; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    margin-bottom: 2rem;
    border: 1px solid rgba(100,200,255,0.15);
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #ffffff;
    margin: 0;
    letter-spacing: -1px;
}
.hero p {
    color: #94a3b8;
    font-size: 1.1rem;
    margin-top: 0.5rem;
}
.hero .badge {
    display: inline-block;
    background: rgba(56,189,248,0.15);
    color: #38bdf8;
    border: 1px solid #38bdf8;
    border-radius: 50px;
    padding: 0.3rem 1rem;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 1rem;
}

/* Cards */
.card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    color: #64748b;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Metric cards */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
}
.metric-card {
    flex: 1;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #f1f5f9;
    font-weight: 700;
}
.metric-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
}

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2rem 0 1rem 0;
}
.section-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #f1f5f9;
    margin: 0;
}

/* Generate button */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.9rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(14,165,233,0.5) !important;
}

/* Input styling */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    padding: 0.7rem 1rem !important;
}
.stSlider > div { padding: 0.5rem 0; }

/* Risk radio */
.stRadio > div { flex-direction: row; gap: 1rem; }

/* Result boxes */
.result-box {
    background: #0f172a;
    border-left: 3px solid #0ea5e9;
    border-radius: 0 12px 12px 0;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.7;
    white-space: pre-wrap;
}
.result-box.green { border-left-color: #10b981; }
.result-box.amber { border-left-color: #f59e0b; }
.result-box.red   { border-left-color: #ef4444; }

/* Risk progress */
.risk-bar-wrap {
    background: #1e293b;
    border-radius: 50px;
    height: 10px;
    margin: 1rem 0;
    overflow: hidden;
}
.risk-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #10b981, #f59e0b, #ef4444);
    transition: width 1s ease;
}

/* Table */
.dataframe {
    background: #0f172a !important;
    border-radius: 12px !important;
    border: 1px solid #1e293b !important;
    color: #cbd5e1 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #334155;
    font-size: 0.8rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1e293b;
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">⚡ POWERED BY AGENTIC AI</div>
    <h1>💰 FinSight</h1>
    <p>Your intelligent personal finance advisor — powered by multiple AI agents working together</p>
</div>
""", unsafe_allow_html=True)

# ── Input Section ─────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">👤 Personal Details</div>', unsafe_allow_html=True)
user_name = st.text_input("Your Name", placeholder="Enter your name", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-title">💵 Financial Overview</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    income       = st.number_input("Monthly Income (₹)", min_value=0, value=40000, step=1000)
    expenses     = st.number_input("Monthly Expenses (₹)", min_value=0, value=28000, step=1000)
with col2:
    savings_goal = st.number_input("Monthly Savings Goal (₹)", min_value=0, value=5000, step=500)
    sip_amount   = st.number_input("SIP Amount / month (₹)", min_value=0, value=3000, step=500)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-title">📊 Investment Preferences</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    stock = st.text_input("NSE Stock Symbol", value="RELIANCE", placeholder="e.g. TCS, INFY, HDFCBANK")
with col4:
    years = st.slider("Investment Horizon (years)", 1, 30, 10)

st.markdown("**Risk Appetite**")
risk_level = st.radio("", ["low", "medium", "high"], horizontal=True, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Generate Button ───────────────────────────────────────────
if st.button("🚀 Generate My Financial Plan"):
    name = user_name if user_name else "User"
    with st.spinner("🤖 AI agents are analysing your finances..."):
        result = run_finsight_ui(
            income=income, expenses=expenses,
            savings_goal=savings_goal, risk_level=risk_level,
            stock=stock, sip_amount=sip_amount, years=years
        )

    surplus      = income - expenses
    savings_rate = round((surplus / income) * 100, 1) if income > 0 else 0
    goal_met     = surplus >= savings_goal
    risk_score   = int(result["risk_score"].split("/")[0])
    risk_pct     = int((risk_score / 8) * 100)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#064e3b,#065f46);
                border-radius:12px;padding:1rem 1.5rem;
                color:#6ee7b7;font-weight:600;font-size:1rem;
                margin:1rem 0;border:1px solid #10b981;">
        ✅ Your personalised financial plan is ready, """ + name + """!
    </div>""", unsafe_allow_html=True)

    # Metrics
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">₹{surplus:,}</div>
            <div class="metric-label">Monthly Surplus</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{savings_rate}%</div>
            <div class="metric-label">Savings Rate</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{'✅' if goal_met else '❌'}</div>
            <div class="metric-label">Goal {'Met' if goal_met else 'Not Met'}</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{risk_score}/8</div>
            <div class="metric-label">Risk Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Market Data
    st.markdown("""
    <div class="section-header">
        <div class="section-icon" style="background:#0c4a6e;">📈</div>
        <p class="section-title">Live Market Data</p>
    </div>""", unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{result["market"]}</div>', unsafe_allow_html=True)

    # Budget
    st.markdown("""
    <div class="section-header">
        <div class="section-icon" style="background:#064e3b;">💰</div>
        <p class="section-title">Budget Analysis</p>
    </div>""", unsafe_allow_html=True)
    st.markdown(f'<div class="result-box green">{result["budget"]}</div>', unsafe_allow_html=True)

    # Investment Plan
    st.markdown("""
    <div class="section-header">
        <div class="section-icon" style="background:#1e1b4b;">📊</div>
        <p class="section-title">Investment Plan</p>
    </div>""", unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{result["investments"]}</div>', unsafe_allow_html=True)

    # Risk Report
    risk_color = "#10b981" if risk_score >= 7 else "#f59e0b" if risk_score >= 4 else "#ef4444"
    risk_box_class = "green" if risk_score >= 7 else "amber" if risk_score >= 4 else "red"
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon" style="background:#431407;">⚠️</div>
        <p class="section-title">Risk Report</p>
    </div>
    <div class="risk-bar-wrap">
        <div class="risk-bar-fill" style="width:{risk_pct}%;background:{risk_color};"></div>
    </div>
    <div class="result-box {risk_box_class}">{result["risk_details"]}</div>
    """, unsafe_allow_html=True)

    # Save to DB
    save_report(
        name=name, income=income, expenses=expenses,
        surplus=surplus, savings_rate=savings_rate,
        risk_score=result["risk_score"],
        investment_plan=result["investments"]
    )
    st.toast("💾 Report saved to history!")

# ── History ───────────────────────────────────────────────────
st.markdown("""
<div class="section-header" style="margin-top:3rem;">
    <div class="section-icon" style="background:#1e293b;">📋</div>
    <p class="section-title">Past Reports</p>
</div>""", unsafe_allow_html=True)

reports = get_all_reports()
if reports:
    import pandas as pd
    df = pd.DataFrame(reports, columns=[
        "Name", "Income (₹)", "Expenses (₹)",
        "Surplus (₹)", "Savings Rate (%)", "Risk Score", "Date"
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.markdown("""
    <div style="text-align:center;color:#334155;padding:2rem;
                border:1px dashed #1e293b;border-radius:12px;">
        No reports yet — fill the form above and generate your first plan!
    </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with ❤️ by Devi · FinSight — Agentic AI Personal Finance Advisor<br>
    Powered by Python · LangChain · Streamlit · yfinance
</div>
""", unsafe_allow_html=True)