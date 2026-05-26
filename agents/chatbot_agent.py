import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_finsight(question: str, user_context: dict) -> str:
    """
    user_context = {
        income, expenses, surplus,
        savings_rate, risk_score, investment_plan
    }
    """
    system_prompt = f"""
You are FinSight AI — a smart personal finance advisor for Indian users.

IMPORTANT: Use ONLY the data below. Do NOT assume or change these values:
- Monthly Income:    ₹{user_context.get('income', 0):,}
- Monthly Expenses:  ₹{user_context.get('expenses', 0):,}
- Monthly Surplus:   ₹{user_context.get('surplus', 0):,}
- Savings Rate:      {user_context.get('savings_rate', 0)}%
- Risk Score:        {user_context.get('risk_score', 'N/A')} out of 8
- Investment Plan:   {user_context.get('investment_plan', 'N/A')}

Rules:
- ALWAYS use the exact numbers above — never change them
- Give India-specific advice (SIP, PPF, FD, NSE)
- Keep answers short, clear, friendly
- Always end with one actionable tip
- If user gives different numbers — politely say their plan is based on above data
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": question}
        ],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content