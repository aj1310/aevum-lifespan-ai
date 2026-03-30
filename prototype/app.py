import streamlit as st
import pandas as pd
import sqlite3
import re
from datetime import datetime
from openai import OpenAI

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Aevum Lifespan AI", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
# SIDEBAR LOGIN
# -------------------------
st.sidebar.title("Aevum Lifespan AI")

username = st.sidebar.text_input("Enter Username")

if username:
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", (username, str(datetime.now())))
    conn.commit()
    st.sidebar.success(f"Logged in as {username}")

# -------------------------
# DEMO FALLBACK
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
        df = pd.read_sql_query(f"""
        SELECT * FROM biomarkers WHERE username='{username}'
        """, conn)
        return df
    return pd.DataFrame()

df = get_data()

# -------------------------
# TABS
# -------------------------
tabs = st.tabs(["Summary", "Trends", "Recommendations", "Risks", "Uploads"])

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

# -------------------------
# SELECT DATA (IMPORTANT FIX)
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
# AI ENGINE
# -------------------------
def generate_ai(data):
    prompt = f"""
    Biomarkers:
    Cholesterol {data['cholesterol']}
    LDL {data['ldl']}
    HDL {data['hdl']}
    Triglycerides {data['triglycerides']}
    Vitamin D {data['vitamin_d']}
    Glucose {data['glucose']}

    Provide:
    1. Summary
    2. Risks
    3. Recommendations
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except:
        return "AI unavailable. Showing demo insights."

ai_output = generate_ai(current)

# -------------------------
# PARSE
# -------------------------
def parse(text):
    s, r, a = [], [], []
    for line in text.split("\n"):
        l = line.lower()
        if "risk" in l:
            r.append(line)
        elif "recommend" in l:
            a.append(line)
        else:
            s.append(line)
    return s, r, a

summary, risks, actions = parse(ai_output)

# -------------------------
# SUMMARY TAB
# -------------------------
with tabs[0]:
    st.header("Your Health Summary")

    st.metric("Health Score", "78", "+5")

    st.subheader("Key Insights")
    for i in summary:
        if i.strip():
            st.write(i)

# -------------------------
# TRENDS TAB
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
        if a.strip():
            st.success(a)

# -------------------------
# RISKS
# -------------------------
with tabs[3]:
    st.header("Risks")

    for r in risks:
        if r.strip():
            st.warning(r)
