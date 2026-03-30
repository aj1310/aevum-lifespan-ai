import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import PyPDF2

# Initialize OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Aevum Lifespan AI", layout="wide")

# -------------------------
# HEADER
# -------------------------
st.title("Aevum Lifespan AI")
st.caption("The intelligence layer for human longevity")
st.markdown("### Decode your health across biology, behavior, and time")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("User Profile")

age = st.sidebar.slider("Age", 25, 60, 38)
activity = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

# Lifestyle inputs
st.sidebar.subheader("Lifestyle Inputs")
sleep_hours = st.sidebar.slider("Avg Sleep (hrs)", 4.0, 9.0, 6.5)
workouts = st.sidebar.slider("Workouts / week", 0, 7, 3)
diet_quality = st.sidebar.selectbox("Diet Quality", ["Poor", "Average", "Good"])

# Demo mode
demo = st.sidebar.checkbox("Enable Demo Mode", value=True)

# -------------------------
# PDF PARSER
# -------------------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# -------------------------
# REPORT UPLOAD
# -------------------------
st.header("Medical Report")

file = st.file_uploader("Upload PDF report", type=["pdf"])

report_text = ""

if file:
    report_text = extract_text_from_pdf(file)
    st.success("Report uploaded and processed")

elif demo:
    report_text = "Sample report: Cholesterol elevated, Vitamin D low"
    st.info("Demo mode active – using sample report")

# -------------------------
# WEARABLE DATA
# -------------------------
st.header("Wearable Signals")

data = pd.DataFrame({
    "Metric": ["Heart Rate", "HRV", "Sleep"],
    "Value": [72, 55, sleep_hours]
})

st.dataframe(data, use_container_width=True)

# -------------------------
# HEALTH SCORE
# -------------------------
st.header("Health Score")

score = 78
st.metric("Overall Score", score, "+5")

st.markdown("""
**Longevity Interpretation:**  
You are in a moderate optimization zone. Improvements in sleep and cardiovascular fitness 
can significantly enhance long-term outcomes.
""")

# -------------------------
# TRENDS
# -------------------------
st.header("Trends")

hrv = [48, 50, 52, 51, 53, 54, 55]
st.line_chart(hrv)

# -------------------------
# AI ENGINE
# -------------------------
st.header("AI Health Intelligence")

if report_text:
    try:
        prompt = f"""
You are an expert preventive healthcare AI.

User:
Age: {age}
Activity: {activity}
Sleep: {sleep_hours}
Workouts: {workouts}
Diet: {diet_quality}

Wearables:
HR: 72
HRV: 55

Medical Report:
{report_text}

Provide:

1. Key Insights
2. Risk Signals
3. Action Plan

Keep it concise, structured, and practical.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a longevity-focused medical AI."},
                {"role": "user", "content": prompt}
            ]
        )

        output = response.choices[0].message.content

        # Simple parsing
        lines = output.split("\n")

        insights, risks, actions = [], [], []

        for line in lines:
            l = line.lower()
            if "risk" in l:
                risks.append(line)
            elif "recommend" in l or "should" in l:
                actions.append(line)
            else:
                insights.append(line)

        # Display
        st.subheader("🧠 Insights")
        for i in insights:
            if i.strip():
                st.markdown(f"- {i}")

        st.subheader("⚠️ Risks")
        for r in risks:
            if r.strip():
                st.warning(r)

        st.subheader("✅ Actions")
        for a in actions:
            if a.strip():
                st.success(a)

    except:
        st.error("AI temporarily unavailable")

else:
    st.info("Upload a report to generate insights")

# -------------------------
# FUTURE
# -------------------------
st.header("What Aevum will do next")

st.markdown("""
- Continuous health tracking  
- Predictive risk detection  
- Personalized longevity plans  
- Doctor collaboration  
""")
