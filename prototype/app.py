import streamlit as st
import pandas as pd
import sqlite3
import re
from datetime import datetime

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Aevum Lifespan AI", layout="centered")

# -------------------------
# DATABASE
# -------------------------
conn = sqlite3.connect("aevum.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    created_at TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS biomarkers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    cholesterol REAL,
    ldl REAL,
    hdl REAL,
    triglycerides REAL,
    vitamin_d REAL,
    glucose REAL,
    created_at TEXT
)
""")

conn.commit()

# -------------------------
# LOGIN
# -------------------------
st.sidebar.title("Aevum Lifespan AI")

username = st.sidebar.text_input("Enter Username")

if username:
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", (username, str(datetime.now())))
    conn.commit()
    st.sidebar.success(f"Logged in as {username}")

# -------------------------
# DEMO DATA
# -------------------------
DEMO_DATA = {
    "cholesterol": 210,
    "ldl": 140,
    "hdl": 45,
    "triglycerides": 180,
    "vitamin_d": 20,
    "glucose": 95
}

# -------------------------
# EXTRACT BIOMARKERS
# -------------------------
def extract(text):
    def find(p):
        m = re.search(p, text, re.I)
        return float(m.group(1)) if m else None

    return {
        "cholesterol": find(r"cholesterol.*?(\d+)"),
        "ldl": find(r"ldl.*?(\d+)"),
        "hdl": find(r"hdl.*?(\d+)"),
        "triglycerides": find(r"triglycerides.*?(\d+)"),
        "vitamin_d": find(r"vitamin\s*d.*?(\d+)"),
        "glucose": find(r"glucose.*?(\d+)")
    }

# -------------------------
# FETCH DATA
# -------------------------
def get_data():
    if username:
        return pd.read_sql_query(f"""
        SELECT * FROM biomarkers WHERE username='{username}'
        """, conn)
    return pd.DataFrame()

df = get_data()

# -------------------------
# SELECT DATA
# -------------------------
if df.empty:
    current = DEMO_DATA
else:
    latest = df.iloc[-1]
    current = {
        "cholesterol": latest["cholesterol"],
        "ldl": latest["ldl"],
        "hdl": latest["hdl"],
        "triglycerides": latest["triglycerides"],
        "vitamin_d": latest["vitamin_d"],
        "glucose": latest["glucose"]
    }

# -------------------------
# RULE-BASED ENGINE (NO AI NEEDED)
# -------------------------
def generate_insights(data):
    summary = []
    risks = []
    recommendations = []

    # Cholesterol
    if data["cholesterol"] and data["cholesterol"] > 200:
        summary.append("Your cholesterol levels are elevated.")
        risks.append("Higher risk of cardiovascular disease.")
        recommendations.append("Reduce saturated fat intake and increase exercise.")

    # LDL
    if data["ldl"] and data["ldl"] > 130:
        risks.append("Elevated LDL increases heart disease risk.")
        recommendations.append("Increase fiber intake and reduce processed foods.")

    # HDL
    if data["hdl"] and data["hdl"] < 50:
        summary.append("HDL (good cholesterol) is on the lower side.")
        recommendations.append("Increase physical activity to improve HDL.")

    # Triglycerides
    if data["triglycerides"] and data["triglycerides"] > 150:
        risks.append("High triglycerides may impact metabolic health.")
        recommendations.append("Reduce sugar and refined carbs.")

    # Vitamin D
    if data["vitamin_d"] and data["vitamin_d"] < 30:
        summary.append("Vitamin D levels are low.")
        recommendations.append("Increase sunlight exposure and consider supplements.")

    # Glucose
    if data["glucose"] and data["glucose"] > 100:
        risks.append("Elevated glucose indicates risk of prediabetes.")
        recommendations.append("Improve diet and increase activity levels.")

    # Default fallback
    if not summary:
        summary.append("Your health markers are within a stable range.")
        recommendations.append("Maintain current lifestyle habits.")

    return summary, risks, recommendations

summary, risks, actions = generate_insights(current)

# -------------------------
# TABS
# -------------------------
tabs = st.tabs(["Summary", "Trends", "Recommendations", "Risks", "Uploads"])

# -------------------------
# SUMMARY
# -------------------------
with tabs[0]:
    st.header("Your Health Summary")

    st.metric("Health Score", "78", "+5")

    st.subheader("Key Insights")
    for s in summary:
        st.write(s)

# -------------------------
# TRENDS
# -------------------------
with tabs[1]:
    st.header("Health Trends")

    if not df.empty:
        st.line_chart(df[["cholesterol", "ldl", "glucose"]])
    else:
        st.info("Upload reports to see trends")

# -------------------------
# RECOMMENDATIONS
# -------------------------
with tabs[2]:
    st.header("Recommendations")

    for a in actions:
        st.success(a)

# -------------------------
# RISKS
# -------------------------
with tabs[3]:
    st.header("Risk Signals")

    for r in risks:
        st.warning(r)

# -------------------------
# UPLOAD
# -------------------------
with tabs[4]:
    st.header("Upload Health Report")

    text = st.text_area("Paste your report text")

    if st.button("Extract & Save"):
        data = extract(text)

        if username:
            c.execute("""
            INSERT INTO biomarkers (username, cholesterol, ldl, hdl, triglycerides, vitamin_d, glucose, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                username,
                data["cholesterol"],
                data["ldl"],
                data["hdl"],
                data["triglycerides"],
                data["vitamin_d"],
                data["glucose"],
                str(datetime.now())
            ))
            conn.commit()

        st.success("Data saved!")
        st.write(data)
