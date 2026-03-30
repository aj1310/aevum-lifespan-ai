import streamlit as st
import pandas as pd
import sqlite3
import re
from datetime import datetime
from openai import OpenAI

st.set_page_config(page_title="Aevum Lifespan AI", layout="wide")

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
# LOGIN
# -------------------------
st.sidebar.header("Login")

username = st.sidebar.text_input("Username")

if username:
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", (username, str(datetime.now())))
    conn.commit()
    st.sidebar.success(f"Logged in: {username}")

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
# TABS
# -------------------------
tabs = st.tabs(["Summary", "Trends", "Recommendations", "Risks", "Uploads"])

# -------------------------
# UPLOAD
# -------------------------
with tabs[4]:
    st.header("Upload Report")

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

        st.success("Saved")
        st.write(data)

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
# TRENDS
# -------------------------
with tabs[1]:
    st.header("Health Trends")

    if not df.empty:
        st.line_chart(df[["cholesterol", "ldl", "glucose"]])

# -------------------------
# AI ENGINE
# -------------------------
def ai(data):
    latest = data.iloc[-1]

    prompt = f"""
    Biomarkers:
    Cholesterol {latest['cholesterol']}
    LDL {latest['ldl']}
    HDL {latest['hdl']}
    Glucose {latest['glucose']}

    Give:
    Summary, Risks, Recommendations
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content

output = ai(df) if not df.empty else ""

# -------------------------
# PARSE
# -------------------------
def parse(text):
    s, r, a = [], [], []
    for line in text.split("\n"):
        if "risk" in line.lower():
            r.append(line)
        elif "recommend" in line.lower():
            a.append(line)
        else:
            s.append(line)
    return s, r, a

summary, risks, actions = parse(output)

# -------------------------
# SUMMARY
# -------------------------
with tabs[0]:
    st.header("Summary")
    for i in summary:
        st.write(i)

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
    st.header("Risks")
    for r in risks:
        st.warning(r)
