def calculate_risk_score(income: float, expenses: float,
                          has_emergency_fund: bool,
                          has_insurance: bool,
                          investment_type: str) -> dict:
    score = 0
    reasons = []

    # Expense ratio check
    expense_ratio = expenses / income
    if expense_ratio > 0.8:
        reasons.append("Expenses too high — above 80% of income")
    elif expense_ratio > 0.6:
        score += 1
        reasons.append("Expenses moderate — between 60-80% of income")
    else:
        score += 2
        reasons.append("Expenses healthy — below 60% of income")

    # Emergency fund
    if has_emergency_fund:
        score += 2
        reasons.append("Good — emergency fund exists")
    else:
        reasons.append("Risky — no emergency fund (keep 6 months expenses)")

    # Insurance
    if has_insurance:
        score += 2
        reasons.append("Good — insurance coverage exists")
    else:
        reasons.append("Risky — no insurance coverage")

    # Investment type
    if investment_type == "low":
        score += 2
        reasons.append("Conservative investments — stable")
    elif investment_type == "medium":
        score += 1
        reasons.append("Balanced investments — moderate risk")
    else:
        reasons.append("Aggressive investments — high risk")

    # Score label
    if score >= 7:
        label = "Low risk — your finances are healthy"
    elif score >= 4:
        label = "Medium risk — some areas need attention"
    else:
        label = "High risk — take action immediately"

    return {
        "score": f"{score}/8",
        "label": label,
        "details": reasons
    }

def format_risk_report(result: dict) -> str:
    lines = [
        f"Risk score: {result['score']}",
        f"Status:     {result['label']}",
        "\nBreakdown:"
    ]
    for r in result["details"]:
        lines.append(f"  - {r}")
    return "\n".join(lines)