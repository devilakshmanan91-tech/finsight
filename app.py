import streamlit as st
from agents.orchestrator import run_finsight_ui
from agents.chatbot_agent import ask_finsight
from utils.database import (init_db, register_user, login_user,
                             save_report, get_user_reports,
                             get_all_reports, get_all_users, get_stats)

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500;600&display=swap');
* { font-family: 'DM Sans', sans-serif; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.hero {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    padding: 5rem 2rem; text-align: center;
    border-bottom: 1px solid rgba(100,200,255,0.1);
}
.hero h1 { font-family:'Playfair Display',serif; font-size:3.5rem; color:#fff; margin:0; letter-spacing:-1px; }
.hero p { color:#94a3b8; font-size:1.2rem; margin-top:1rem; }
.badge {
    display:inline-block; background:rgba(56,189,248,0.15);
    color:#38bdf8; border:1px solid #38bdf8; border-radius:50px;
    padding:0.3rem 1rem; font-size:0.8rem; font-weight:600;
    letter-spacing:1px; margin-bottom:1.5rem;
}
.features { background:#0a0f1e; padding:4rem 2rem; text-align:center; }
.features h2 { font-family:'Playfair Display',serif; color:#f1f5f9; font-size:2rem; margin-bottom:0.5rem; }
.features p { color:#64748b; margin-bottom:3rem; }
.feature-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1.5rem; max-width:1000px; margin:0 auto; }
.feature-card { background:#111827; border:1px solid #1e293b; border-radius:16px; padding:2rem; transition:transform 0.2s; }
.feature-card:hover { transform:translateY(-4px); }
.feature-icon { font-size:2.5rem; margin-bottom:1rem; }
.feature-title { font-weight:600; color:#f1f5f9; font-size:1.1rem; margin-bottom:0.5rem; }
.feature-desc { color:#64748b; font-size:0.9rem; line-height:1.6; }
.how-section { background:#060b14; padding:4rem 2rem; text-align:center; border-top:1px solid #1e293b; }
.how-section h2 { font-family:'Playfair Display',serif; color:#f1f5f9; font-size:2rem; margin-bottom:3rem; }
.steps-row { display:flex; justify-content:center; gap:2rem; flex-wrap:wrap; max-width:900px; margin:0 auto; }
.step-card { background:#111827; border:1px solid #1e293b; border-radius:16px; padding:1.5rem; width:160px; }
.step-number {
    background:linear-gradient(135deg,#0ea5e9,#6366f1); color:white;
    width:36px; height:36px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-weight:700; margin:0 auto 1rem auto;
}
.step-text { color:#94a3b8; font-size:0.85rem; line-height:1.5; }
.about-section { background:#0f172a; padding:4rem 2rem; text-align:center; border-top:1px solid #1e293b; }
.about-section h2 { font-family:'Playfair Display',serif; color:#f1f5f9; font-size:2rem; margin-bottom:1rem; }
.about-section p { color:#64748b; max-width:700px; margin:0 auto 2rem auto; line-height:1.8; }
.auth-container { max-width:460px; margin:3rem auto; padding:0 1rem; }
.auth-card { background:#111827; border:1px solid #1e293b; border-radius:20px; padding:2.5rem; box-shadow:0 20px 60px rgba(0,0,0,0.5); }
.auth-title { font-family:'Playfair Display',serif; font-size:1.8rem; color:#f1f5f9; text-align:center; margin-bottom:0.5rem; }
.auth-subtitle { color:#475569; text-align:center; font-size:0.9rem; margin-bottom:2rem; }
.app-container { max-width:1100px; margin:0 auto; padding:2rem; }
.card { background:#111827; border:1px solid #1e293b; border-radius:16px; padding:1.5rem; margin-bottom:1rem; }
.card-title { font-size:0.75rem; font-weight:600; letter-spacing:2px; color:#64748b; text-transform:uppercase; margin-bottom:1rem; }
.metric-row { display:flex; gap:1rem; margin:1rem 0; }
.metric-card { flex:1; background:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:1.2rem; text-align:center; }
.metric-value { font-family:'Playfair Display',serif; font-size:1.8rem; color:#f1f5f9; font-weight:700; }
.metric-label { font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:1px; margin-top:0.3rem; }
.section-header { display:flex; align-items:center; gap:0.75rem; margin:2rem 0 1rem 0; }
.section-icon { width:36px; height:36px; border-radius:8px; font-size:1rem; }
.section-title { font-family:'Playfair Display',serif; font-size:1.3rem; color:#f1f5f9; margin:0; }
.stButton > button {
    background:linear-gradient(135deg,#0ea5e9,#6366f1) !important;
    color:white !important; border:none !important; border-radius:12px !important;
    padding:0.9rem 2rem !important; font-size:1rem !important;
    font-weight:600 !important; width:100% !important;
    box-shadow:0 4px 20px rgba(14,165,233,0.3) !important;
}
.result-box {
    background:#0f172a; border-left:3px solid #0ea5e9;
    border-radius:0 12px 12px 0; padding:1.2rem 1.5rem;
    margin:0.5rem 0; color:#cbd5e1; font-size:0.95rem;
    line-height:1.7; white-space:pre-wrap;
}
.result-box.green { border-left-color:#10b981; }
.result-box.amber { border-left-color:#f59e0b; }
.result-box.red   { border-left-color:#ef4444; }
.risk-bar-wrap { background:#1e293b; border-radius:50px; height:10px; margin:1rem 0; overflow:hidden; }
.risk-bar-fill { height:100%; border-radius:50px; }
.chat-bubble-user {
    background:#1e40af; color:#fff; border-radius:18px 18px 4px 18px;
    padding:0.8rem 1.2rem; margin:0.5rem 0; max-width:80%; margin-left:auto; font-size:0.95rem;
}
.chat-bubble-ai {
    background:#111827; color:#cbd5e1; border:1px solid #1e293b;
    border-radius:18px 18px 18px 4px; padding:0.8rem 1.2rem;
    margin:0.5rem 0; max-width:85%; font-size:0.95rem; line-height:1.6;
}
.footer { background:#060b14; text-align:center; color:#334155; font-size:0.85rem; padding:2rem; border-top:1px solid #1e293b; }
.footer a { color:#38bdf8; text-decoration:none; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# Session state
defaults = {
    "page": "landing", "logged_in": False, "username": "",
    "is_admin": False, "chat_history": [], "last_context": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()

def do_logout():
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()

def quick_ask(q):
    st.session_state.chat_history.append(("user", q))
    with st.spinner("🤖 Thinking..."):
        ans = ask_finsight(q, st.session_state.last_context)
    st.session_state.chat_history.append(("ai", ans))
    st.rerun()

# ══════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="hero">
        <div class="badge">⚡ POWERED BY AGENTIC AI</div>
        <h1>💰 FinSight</h1>
        <p>Your intelligent personal finance advisor<br>
        powered by multiple AI agents working together</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="features">
        <h2>Everything you need to manage your finances</h2>
        <p>FinSight uses multiple AI agents to give you personalised advice</p>
        <div class="feature-grid">
            <div class="feature-card"><div class="feature-icon">📈</div>
                <div class="feature-title">Live Market Data</div>
                <div class="feature-desc">Real-time NSE stock prices and SIP projections fetched instantly</div>
            </div>
            <div class="feature-card"><div class="feature-icon">💰</div>
                <div class="feature-title">Budget Analysis</div>
                <div class="feature-desc">AI analyses your income and expenses to find the best savings strategy</div>
            </div>
            <div class="feature-card"><div class="feature-icon">⚠️</div>
                <div class="feature-title">Risk Scoring</div>
                <div class="feature-desc">Get a personalised risk score out of 8 with actionable warnings</div>
            </div>
            <div class="feature-card"><div class="feature-icon">🤖</div>
                <div class="feature-title">AI Chatbot</div>
                <div class="feature-desc">Ask anything — powered by Groq LLaMA 3.3, knows YOUR financial data</div>
            </div>
            <div class="feature-card"><div class="feature-icon">📊</div>
                <div class="feature-title">Investment Plan</div>
                <div class="feature-desc">India-specific plans — SIP, PPF, FD, Index funds tailored to your goals</div>
            </div>
            <div class="feature-card"><div class="feature-icon">🔒</div>
                <div class="feature-title">100% Private</div>
                <div class="feature-desc">bcrypt encrypted passwords — only you can see your reports</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="how-section">
        <h2>How FinSight works</h2>
        <div class="steps-row">
            <div class="step-card"><div class="step-number">1</div>
                <div class="feature-icon">📝</div>
                <div class="feature-title">Register</div>
                <div class="step-text">Create your free account in seconds</div>
            </div>
            <div class="step-card"><div class="step-number">2</div>
                <div class="feature-icon">💵</div>
                <div class="feature-title">Enter Details</div>
                <div class="step-text">Add income, expenses and goals</div>
            </div>
            <div class="step-card"><div class="step-number">3</div>
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Analyses</div>
                <div class="step-text">4 AI agents build your plan</div>
            </div>
            <div class="step-card"><div class="step-number">4</div>
                <div class="feature-icon">📋</div>
                <div class="feature-title">Get Report</div>
                <div class="step-text">Personalised financial advice</div>
            </div>
            <div class="step-card"><div class="step-number">5</div>
                <div class="feature-icon">💬</div>
                <div class="feature-title">Chat with AI</div>
                <div class="step-text">Ask follow-up questions anytime</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-section">
        <h2>About FinSight</h2>
        <p>FinSight is an Agentic AI personal finance advisor built specifically
        for Indian users. It uses multiple specialised AI agents — a Data Agent
        for live NSE market data, an Analysis Agent for budget planning,
        a Risk Agent for financial health scoring, and an AI Chatbot powered
        by Groq LLaMA 3.3 for personalised conversations.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Get Started Free"):
            go("register")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔑 Login to FinSight"):
            go("login")

    st.markdown("""
    <div style="background:#060b14;padding:3rem 2rem;border-top:1px solid #1e293b;">
        <h2 style="font-family:'Playfair Display',serif;color:#f1f5f9;text-align:center;font-size:2rem;margin-bottom:2rem;">Contact Us</h2>
        <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;">
            <div style="background:#111827;border:1px solid #1e293b;border-radius:16px;padding:2rem;text-align:center;width:200px;">
                <div style="font-size:2rem;">📧</div>
                <div style="color:#f1f5f9;font-weight:600;margin:0.5rem 0;">Email</div>
                <div style="color:#64748b;font-size:0.85rem;">support@finsight.ai</div>
            </div>
            <div style="background:#111827;border:1px solid #1e293b;border-radius:16px;padding:2rem;text-align:center;width:200px;">
                <div style="font-size:2rem;">💻</div>
                <div style="color:#f1f5f9;font-weight:600;margin:0.5rem 0;">GitHub</div>
                <div style="color:#64748b;font-size:0.85rem;">devilakshmanan91-tech</div>
            </div>
            <div style="background:#111827;border:1px solid #1e293b;border-radius:16px;padding:2rem;text-align:center;width:200px;">
                <div style="font-size:2rem;">📍</div>
                <div style="color:#f1f5f9;font-weight:600;margin:0.5rem 0;">Location</div>
                <div style="color:#64748b;font-size:0.85rem;">Tamil Nadu, India</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Built with ❤️ by <b>Devi</b> · FinSight — Agentic AI Personal Finance Advisor<br>
        Powered by Python · Groq LLaMA 3.3 · Streamlit · SQLite · yfinance
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# REGISTER PAGE
# ══════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════
# REGISTER PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "register":
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-bottom:2rem;">
        <div style="font-size:3rem;">💰</div>
        <div style="font-family:'Playfair Display',serif;
                    font-size:2rem;color:#f1f5f9;">Create Account</div>
        <div style="color:#475569;margin-top:0.5rem;">
            Join FinSight — it's free!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    nu  = st.text_input("👤 Username", placeholder="e.g. devi2024",
                        key="reg_username")
    em  = st.text_input("📧 Email Address",
                        placeholder="e.g. devi@gmail.com", key="reg_email")
    np  = st.text_input("🔒 Password", type="password",
                        placeholder="Min 6 characters", key="reg_pass")
    np2 = st.text_input("🔒 Confirm Password", type="password",
                        placeholder="Repeat password", key="reg_pass2")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Create My Account", use_container_width=True):
        if nu and em and np and np2:
            if np != np2:
                st.error("❌ Passwords don't match!")
            elif len(np) < 6:
                st.error("❌ Password must be at least 6 characters!")
            elif "@" not in em:
                st.error("❌ Please enter a valid email!")
            else:
                with st.spinner("⏳ Creating your account..."):
                    ok, msg = register_user(nu, em, np)
                if ok:
                    st.success("✅ Account created successfully!")
                    st.info("👉 Click **Already registered? Login** below!")
                else:
                    st.error("❌ " + msg)
        else:
            st.warning("⚠️ Please fill all fields!")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;color:#334155;
                font-size:0.8rem;margin-top:1rem;">
        🔒 Your password is encrypted · Your data is private
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Home", use_container_width=True):
            go("landing")
    with col2:
        if st.button("Already registered? Login", use_container_width=True):
            go("login")

    st.markdown('</div>', unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "login":
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:2rem;">
        <div style="font-size:3rem;">👋</div>
        <div style="font-family:'Playfair Display',serif;
                    font-size:2rem;color:#f1f5f9;">Welcome Back!</div>
        <div style="color:#475569;margin-top:0.5rem;">
            Sign in to your FinSight account
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    u = st.text_input("👤 Username",
                      placeholder="Enter your username",
                      key="login_user")
    p = st.text_input("🔒 Password", type="password",
                      placeholder="Enter your password",
                      key="login_pass")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔑 Login → Enter FinSight", use_container_width=True):
        if u and p:
            with st.spinner("⏳ Logging in..."):
                ok, is_admin = login_user(u, p)
            if ok:
                st.session_state.logged_in = True
                st.session_state.username  = u
                st.session_state.is_admin  = is_admin
                st.success("✅ Login successful! Loading...")
                import time; time.sleep(0.5)
                go("app")
            else:
                st.error("❌ Invalid username or password!")
        else:
            st.warning("⚠️ Please fill all fields!")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;color:#334155;
                font-size:0.8rem;margin-top:1rem;">
        🔒 Your data is encrypted and secure
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Home", use_container_width=True):
            go("landing")
    with col2:
        if st.button("New here? Register Free", use_container_width=True):
            go("register")

    st.markdown('</div>', unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════
# APP PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "app":
    if not st.session_state.logged_in:
        go("login")

    st.markdown('<div class="app-container">', unsafe_allow_html=True)

    if st.session_state.is_admin:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"### 👑 Admin Dashboard — Welcome, **{st.session_state.username}**!")
        with col2:
            if st.button("Logout"):
                do_logout()

        import pandas as pd
        total_users, total_reports = get_stats()
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card"><div class="metric-value">{total_users}</div><div class="metric-label">Total Users</div></div>
            <div class="metric-card"><div class="metric-value">{total_reports}</div><div class="metric-label">Total Reports</div></div>
            <div class="metric-card"><div class="metric-value">🟢</div><div class="metric-label">System Live</div></div>
            <div class="metric-card"><div class="metric-value">🤖</div><div class="metric-label">AI Active</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        atab1, atab2 = st.tabs(["👥 All Users", "📋 All Reports"])
        with atab1:
            users = get_all_users()
            if users:
                df_u = pd.DataFrame(users, columns=["Username","Email","Is Admin","Joined"])
                df_u["Is Admin"] = df_u["Is Admin"].apply(lambda x: "👑 Admin" if x else "👤 User")
                st.dataframe(df_u, use_container_width=True, hide_index=True)
            else:
                st.info("No users yet!")
        with atab2:
            reports = get_all_reports()
            if reports:
                df_r = pd.DataFrame(reports, columns=["Username","Income (₹)","Expenses (₹)","Surplus (₹)","Savings Rate (%)","Risk Score","Date"])
                st.dataframe(df_r, use_container_width=True, hide_index=True)
            else:
                st.info("No reports yet!")

    else:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1rem;">
                <span style="color:#38bdf8;font-size:1.1rem;font-weight:600;">👋 Welcome back, {st.session_state.username}!</span>
                <span style="color:#475569;font-size:0.9rem;margin-left:1rem;">Generate plan → Chat with AI → Track history</span>
            </div>""", unsafe_allow_html=True)
        with col2:
            if st.button("Logout"):
                do_logout()

        tab_plan, tab_chat, tab_history = st.tabs(["🚀 Financial Plan","🤖 AI Chatbot","📋 My Reports"])

        with tab_plan:
            st.markdown('<div class="card"><div class="card-title">💵 Financial Overview</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                income       = st.number_input("Monthly Income (₹)", min_value=0, value=40000, step=1000)
                expenses     = st.number_input("Monthly Expenses (₹)", min_value=0, value=28000, step=1000)
            with c2:
                savings_goal = st.number_input("Monthly Savings Goal (₹)", min_value=0, value=5000, step=500)
                sip_amount   = st.number_input("SIP Amount / month (₹)", min_value=0, value=3000, step=500)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card"><div class="card-title">📊 Investment Preferences</div>', unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                stock = st.text_input("NSE Stock Symbol", value="RELIANCE", placeholder="e.g. TCS, INFY, HDFCBANK")
            with c4:
                years = st.slider("Investment Horizon (years)", 1, 30, 10)
            st.markdown("**Your Risk Appetite**")
            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                st.markdown("""<div style="background:#064e3b;border-radius:8px;padding:0.5rem;text-align:center;font-size:0.8rem;color:#6ee7b7;">🟢 <b>Low</b><br>Safe · FD · PPF</div>""", unsafe_allow_html=True)
            with rc2:
                st.markdown("""<div style="background:#451a03;border-radius:8px;padding:0.5rem;text-align:center;font-size:0.8rem;color:#fbbf24;">🟡 <b>Medium</b><br>Balanced · Index funds</div>""", unsafe_allow_html=True)
            with rc3:
                st.markdown("""<div style="background:#450a0a;border-radius:8px;padding:0.5rem;text-align:center;font-size:0.8rem;color:#fca5a5;">🔴 <b>High</b><br>Aggressive · Stocks</div>""", unsafe_allow_html=True)
            risk_level = st.radio("Select Risk Level", ["low", "medium", "high"], horizontal=True, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚀 Generate My Financial Plan"):
                with st.spinner("🤖 AI agents analysing your finances..."):
                    result = run_finsight_ui(
                        income=income, expenses=expenses,
                        savings_goal=savings_goal, risk_level=risk_level,
                        stock=stock, sip_amount=sip_amount, years=years
                    )
                surplus      = income - expenses
                savings_rate = round((surplus/income)*100,1) if income > 0 else 0
                goal_met     = surplus >= savings_goal
                risk_score   = int(result["risk_score"].split("/")[0])
                risk_pct     = int((risk_score/8)*100)
                risk_color   = "#10b981" if risk_score >= 7 else "#f59e0b" if risk_score >= 4 else "#ef4444"
                risk_class   = "green"   if risk_score >= 7 else "amber"   if risk_score >= 4 else "red"

                st.session_state.last_context = {
                    "income": income, "expenses": expenses, "surplus": surplus,
                    "savings_rate": savings_rate, "risk_score": result["risk_score"],
                    "investment_plan": result["investments"]
                }

                st.markdown("""
                <div style="background:linear-gradient(135deg,#064e3b,#065f46);border-radius:12px;padding:1rem 1.5rem;color:#6ee7b7;font-weight:600;margin:1rem 0;border:1px solid #10b981;">
                    ✅ Plan ready! Go to 🤖 AI Chatbot tab to ask questions!
                </div>""", unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-card"><div class="metric-value">₹{surplus:,}</div><div class="metric-label">Monthly Surplus</div></div>
                    <div class="metric-card"><div class="metric-value">{savings_rate}%</div><div class="metric-label">Savings Rate</div></div>
                    <div class="metric-card"><div class="metric-value">{'✅' if goal_met else '❌'}</div><div class="metric-label">Goal {'Met' if goal_met else 'Not Met'}</div></div>
                    <div class="metric-card"><div class="metric-value">{risk_score}/8</div><div class="metric-label">Risk Score</div></div>
                </div>""", unsafe_allow_html=True)

                st.markdown("""<div class="section-header"><div class="section-icon" style="background:#0c4a6e;">📈</div><p class="section-title">Live Market Data</p></div>""", unsafe_allow_html=True)
                st.markdown(f'<div class="result-box">{result["market"]}</div>', unsafe_allow_html=True)
                st.markdown("""<div class="section-header"><div class="section-icon" style="background:#064e3b;">💰</div><p class="section-title">Budget Analysis</p></div>""", unsafe_allow_html=True)
                st.markdown(f'<div class="result-box green">{result["budget"]}</div>', unsafe_allow_html=True)
                st.markdown("""<div class="section-header"><div class="section-icon" style="background:#1e1b4b;">📊</div><p class="section-title">Investment Plan</p></div>""", unsafe_allow_html=True)
                st.markdown(f'<div class="result-box">{result["investments"]}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="section-header"><div class="section-icon" style="background:#431407;">⚠️</div><p class="section-title">Risk Report</p></div>
                <div class="risk-bar-wrap"><div class="risk-bar-fill" style="width:{risk_pct}%;background:{risk_color};"></div></div>
                <div class="result-box {risk_class}">{result["risk_details"]}</div>
                """, unsafe_allow_html=True)

                save_report(
                    username=st.session_state.username,
                    income=income, expenses=expenses, surplus=surplus,
                    savings_rate=savings_rate, risk_score=result["risk_score"],
                    investment_plan=result["investments"]
                )
                st.toast("💾 Saved to My Reports!")

        with tab_chat:
            st.markdown("### 🤖 FinSight AI Chatbot")
            if not st.session_state.last_context:
                st.markdown("""
                <div style="text-align:center;background:#0f172a;border:2px dashed #1e293b;border-radius:16px;padding:3rem;color:#475569;">
                    <div style="font-size:3rem;">🤖</div>
                    <div style="font-size:1.1rem;color:#64748b;margin-top:1rem;">Go to 🚀 Financial Plan tab first!</div>
                </div>""", unsafe_allow_html=True)
            else:
                ctx = st.session_state.last_context
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #10b981;border-radius:12px;padding:1rem;margin-bottom:1rem;color:#6ee7b7;font-size:0.85rem;">
                    🧠 AI knows — Income: ₹{ctx['income']:,} · Surplus: ₹{ctx['surplus']:,} · Risk: {ctx['risk_score']} · Savings: {ctx['savings_rate']}%
                </div>""", unsafe_allow_html=True)

                st.markdown("**⚡ Quick questions:**")
                qc1, qc2, qc3 = st.columns(3)
                with qc1:
                    if st.button("🏠 Buy a house?"): quick_ask("Can I buy a house now?")
                with qc2:
                    if st.button("📈 Best investment?"): quick_ask("What is the best investment for me?")
                with qc3:
                    if st.button("🎯 Reach goal faster?"): quick_ask("How can I reach my savings goal faster?")
                qc4, qc5, qc6 = st.columns(3)
                with qc4:
                    if st.button("💳 Take a loan?"): quick_ask("Should I take a personal loan?")
                with qc5:
                    if st.button("📱 Reduce expenses?"): quick_ask("How to reduce my monthly expenses?")
                with qc6:
                    if st.button("🏦 Emergency fund?"): quick_ask("How much emergency fund should I keep?")

                st.markdown("---")
                for role, msg in st.session_state.chat_history:
                    if role == "user":
                        st.markdown(f'<div class="chat-bubble-user">👤 {msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-bubble-ai">🤖 {msg}</div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                question = st.text_input("", placeholder="Ask anything about your finances...", key="chat_input", label_visibility="collapsed")
                cs1, cs2 = st.columns([3, 1])
                with cs1:
                    if st.button("Send 💬", key="send_btn"):
                        if question.strip():
                            quick_ask(question)
                with cs2:
                    if st.button("🗑️ Clear", key="clear_btn"):
                        st.session_state.chat_history = []
                        st.rerun()

        with tab_history:
            st.markdown("### 📋 My Financial Reports")
            st.markdown("""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:10px;padding:0.8rem 1.2rem;color:#64748b;font-size:0.85rem;margin-bottom:1rem;">
                📌 Only <b style="color:#38bdf8;">you</b> can see your reports — 100% private!
            </div>""", unsafe_allow_html=True)
            import pandas as pd
            reports = get_user_reports(st.session_state.username)
            if reports:
                df = pd.DataFrame(reports, columns=["Username","Income (₹)","Expenses (₹)","Surplus (₹)","Savings Rate (%)","Risk Score","Date"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.markdown("""
                <div style="text-align:center;color:#334155;padding:3rem;border:1px dashed #1e293b;border-radius:12px;">
                    <div style="font-size:2rem;">📋</div>
                    No reports yet! Generate your first plan above!
                </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        Built with ❤️ by <b>Devi</b> · FinSight — Agentic AI Personal Finance Advisor<br>
        Powered by Python · Groq LLaMA 3.3 · Streamlit · SQLite · yfinance
    </div>""", unsafe_allow_html=True)