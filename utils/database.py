import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("finsight.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            income REAL,
            expenses REAL,
            surplus REAL,
            savings_rate REAL,
            risk_score TEXT,
            investment_plan TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_report(name, income, expenses, surplus,
                savings_rate, risk_score, investment_plan):
    conn = sqlite3.connect("finsight.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports
        (name, income, expenses, surplus, savings_rate,
         risk_score, investment_plan, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, income, expenses, surplus, savings_rate,
          risk_score, investment_plan,
          datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_all_reports():
    conn = sqlite3.connect("finsight.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, income, expenses, surplus,
               savings_rate, risk_score, created_at
        FROM reports ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows