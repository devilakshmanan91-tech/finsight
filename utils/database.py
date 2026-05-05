import sqlite3
import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

DB = "finsight.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            is_admin    INTEGER DEFAULT 0,
            created_at  TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT,
            income          REAL,
            expenses        REAL,
            surplus         REAL,
            savings_rate    REAL,
            risk_score      TEXT,
            investment_plan TEXT,
            created_at      TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS otp_store (
            email      TEXT PRIMARY KEY,
            otp        TEXT,
            created_at TEXT
        )
    """)
    # Create admin
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        hashed = bcrypt.hashpw("Admin@123".encode(), bcrypt.gensalt())
        c.execute("""
            INSERT INTO users (username, email, password, is_admin, created_at)
            VALUES (?, ?, ?, 1, ?)
        """, ("admin", "admin@finsight.ai", hashed.decode(),
              datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def send_otp(email: str, sender_email: str, sender_password: str) -> str:
    otp = str(random.randint(100000, 999999))
    try:
        msg = MIMEText(f"""
Hi there!

Your FinSight verification code is:

    {otp}

This code expires in 10 minutes.
Do not share this with anyone.

— FinSight AI Team
        """)
        msg["Subject"] = "FinSight — Your OTP Verification Code"
        msg["From"]    = sender_email
        msg["To"]      = email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        # Save OTP
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO otp_store (email, otp, created_at)
            VALUES (?, ?, ?)
        """, (email, otp, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()
        return "sent"
    except Exception as e:
        return f"error: {str(e)}"

def verify_otp(email: str, entered_otp: str) -> bool:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT otp FROM otp_store WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == entered_otp

def register_user(username, email, password):
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        c.execute("""
            INSERT INTO users (username, email, password, is_admin, created_at)
            VALUES (?, ?, ?, 0, ?)
        """, (username, email, hashed.decode(),
              datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists!"
        return False, "Email already registered!"

def login_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT password, is_admin FROM users WHERE username = ?",
              (username,))
    row = c.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[0].encode()):
        return True, bool(row[1])
    return False, False

def save_report(username, income, expenses, surplus,
                savings_rate, risk_score, investment_plan):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO reports
        (username, income, expenses, surplus, savings_rate,
         risk_score, investment_plan, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, income, expenses, surplus, savings_rate,
          risk_score, investment_plan,
          datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_user_reports(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT username, income, expenses, surplus,
               savings_rate, risk_score, created_at
        FROM reports WHERE username = ?
        ORDER BY created_at DESC
    """, (username,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_reports():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT username, income, expenses, surplus,
               savings_rate, risk_score, created_at
        FROM reports ORDER BY created_at DESC
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_users():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT username, email, is_admin, created_at
        FROM users ORDER BY created_at DESC
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE is_admin = 0")
    total_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM reports")
    total_reports = c.fetchone()[0]
    conn.close()
    return total_users, total_reports