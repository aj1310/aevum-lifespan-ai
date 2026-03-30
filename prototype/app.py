import streamlit as st
import pandas as pd
import sqlite3
import re
from datetime import datetime

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
# SIDEBAR
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
# EXTRACT
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
# CURRENT DATA
# -------------------------
if df.empty:
    current = DEMO_DATA
    st.info("Showing demo data. Upload your report for personalized insights.")
else:
    latest = df.iloc[-1]
    current = latest

# -------------------------
# SMART INSIGHTS ENGINE
# -------------------------
def generate_insights(data):
    primary = ""
    secondary = []
    actions = []

    # Primary driver
    if data["cholesterol"] > 200:
        primary = "Elevated cholesterol is your biggest health lever right now."

    # Secondary signals
    if data["hdl"] < 50:
        secondary.append("Low HDL reduces protective cardiovascular effect.")

    if data["vitamin_d"] < 30:
        secondary.append("Vitamin D deficiency may impact immunity and energy.")

    if data["triglycerides"] > 150:
        secondary.append("Triglycerides indicate metabolic imbalance.")

    # Actions
    actions = [
        "Increase physical activity (150 min/week)",
        "Reduce processed carbs and saturated fats",
        "Get 15–20 mins sunlight daily",
        "Improve sleep consistency"
    ]

    return primary, secondary, actions

primary, secondary, actions = generate_insights(current)

# -------------------------
# TABS
# -------------------------
tabs = st.tabs(["Summary", "Trends", "Recommendations", "Risks", "Uploads"])

# -------------------------
# SUMMARY (PREMIUM)
# -------------------------
with tabs[0]:
    st.title("Your Health Summary")

    st.metric("Health Score", "78", "+5")

    st.success("You're improving. Stay consistent 🚀")

    st.subheader("🧠 Primary Insight")
    st.markdown(f"### {primary}")

    st.subheader("📊 Key Signals")
    for s in secondary:
        st.markdown(f"- {s}")

    st.subheader("📌 Current Biomarkers")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Cholesterol", current["cholesterol"])
        st.metric("HDL", current["hdl"])

    with col2:
        st.metric("LDL", current["ldl"])
        st.metric("Glucose", current["glucose"])

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
    st.header("Action Plan")

    for a in actions:
        st.success(a)

# -------------------------
# RISKS
# -------------------------
with tabs[3]:
    st.header("Risk Signals")

    if current["cholesterol"] > 200:
        st.warning("Cardiovascular risk elevated")

    if current["glucose"] > 100:
        st.warning("Risk of prediabetes")

# -------------------------
# UPLOAD
# -------------------------
with tabs[4]:
    st.header("Upload Health Report")

    text = st.text_area("Paste report text")

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
