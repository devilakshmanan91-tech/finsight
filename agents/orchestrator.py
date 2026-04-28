from tools.data_tools import fetch_stock_price, calculate_sip_returns
from agents.analysis_agent import analyse_budget, suggest_investments
from agents.risk_agent import calculate_risk_score, format_risk_report


def run_finsight(income: float, expenses: float,
                 savings_goal: float, risk_level: str,
                 stock: str, sip_amount: float, years: int):

    print("\n========== FINSIGHT REPORT ==========\n")

    # Agent 1 — Data
    print("📈 LIVE MARKET DATA")
    print(fetch_stock_price(stock))
    print(calculate_sip_returns(sip_amount, years, 12))

    print("\n💰 BUDGET ANALYSIS")
    # Agent 2 — Analysis
    print(analyse_budget(income, expenses, savings_goal))
    surplus = income - expenses
    print(suggest_investments(surplus, risk_level))

    print("\n⚠️  RISK REPORT")
    # Agent 3 — Risk
    result = calculate_risk_score(
        income=income,
        expenses=expenses,
        has_emergency_fund=False,
        has_insurance=True,
        investment_type=risk_level
    )
    print(format_risk_report(result))

    print("\n=====================================")
    print("✅ Report complete! Built by FinSight")


def run_finsight_ui(income: float, expenses: float,
                    savings_goal: float, risk_level: str,
                    stock: str, sip_amount: float, years: int):

    # Agent 1 — Data
    market = (fetch_stock_price(stock) + "\n" +
              calculate_sip_returns(sip_amount, years, 12))

    # Agent 2 — Analysis
    surplus = income - expenses
    budget = analyse_budget(income, expenses, savings_goal)
    investments = suggest_investments(surplus, risk_level)

    # Agent 3 — Risk
    risk_result = calculate_risk_score(
        income=income,
        expenses=expenses,
        has_emergency_fund=False,
        has_insurance=True,
        investment_type=risk_level
    )

    return {
        "market":       market,
        "budget":       budget,
        "investments":  investments,
        "risk_score":   risk_result["score"],
        "risk_details": format_risk_report(risk_result)
    }