import yfinance as yf

def fetch_stock_price(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker + ".NS")
        hist = stock.history(period="5d")   # more reliable than stock.info
        if hist.empty:
            return f"{ticker}: live price unavailable right now"
        price = round(hist["Close"].iloc[-1], 2)
        return f"{ticker}: ₹{price:,.2f}"
    except Exception:
        return f"{ticker}: live price unavailable right now"

def fetch_stock_history(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker + ".NS")
        hist = stock.history(period="1mo")
        if hist.empty:
            return f"{ticker}: 1-month data unavailable right now"
        start = round(hist["Close"].iloc[0], 2)
        end = round(hist["Close"].iloc[-1], 2)
        change = round(((end - start) / start) * 100, 2)
        return f"{ticker}: 1-month return = {change}%"
    except Exception:
        return f"{ticker}: 1-month data unavailable right now"

def calculate_sip_returns(monthly: float, years: int, rate: float) -> str:
    months = years * 12
    r = rate / 100 / 12
    if r == 0:
        future = monthly * months
    else:
        future = monthly * (((1 + r) ** months - 1) / r) * (1 + r)
    invested = monthly * months
    profit = round(future - invested, 2)
    return (f"SIP ₹{monthly}/month for {years} years at {rate}% return:\n"
            f"  Invested: ₹{invested:,.0f}\n"
            f"  Future value: ₹{round(future, 2):,.0f}\n"
            f"  Profit: ₹{profit:,.0f}")