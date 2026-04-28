def analyse_budget(income: float, expenses: float, savings_goal: float) -> str:
    surplus = income - expenses
    if surplus <= 0:
        return (f"Your expenses (₹{expenses}) exceed your income (₹{income})!\n"
                f"You need to cut ₹{abs(surplus):,.0f} from expenses immediately.")

    savings_rate = round((surplus / income) * 100, 1)
    can_meet_goal = "Yes" if surplus >= savings_goal else "No"
    shortfall = max(0, savings_goal - surplus)

    return (f"Monthly income:    ₹{income:,.0f}\n"
            f"Monthly expenses:  ₹{expenses:,.0f}\n"
            f"Monthly surplus:   ₹{surplus:,.0f}\n"
            f"Savings rate:      {savings_rate}%\n"
            f"Can meet goal:     {can_meet_goal}\n"
            f"Shortfall:         ₹{shortfall:,.0f}")

def suggest_investments(surplus: float, risk: str) -> str:
    if risk == "low":
        return (f"Low risk plan for ₹{surplus:,.0f}/month:\n"
                f"  FD / RD:        ₹{surplus*0.5:,.0f}\n"
                f"  PPF:            ₹{surplus*0.3:,.0f}\n"
                f"  Liquid fund:    ₹{surplus*0.2:,.0f}")
    elif risk == "medium":
        return (f"Medium risk plan for ₹{surplus:,.0f}/month:\n"
                f"  Index fund SIP: ₹{surplus*0.5:,.0f}\n"
                f"  PPF:            ₹{surplus*0.3:,.0f}\n"
                f"  FD:             ₹{surplus*0.2:,.0f}")
    else:
        return (f"High risk plan for ₹{surplus:,.0f}/month:\n"
                f"  Stocks/MF SIP:  ₹{surplus*0.6:,.0f}\n"
                f"  Index fund:     ₹{surplus*0.3:,.0f}\n"
                f"  Emergency fund: ₹{surplus*0.1:,.0f}")