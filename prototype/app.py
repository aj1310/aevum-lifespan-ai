import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import PyPDF2

# -------------------------
# INIT
# -------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="Aevum Lifespan AI", layout="wide")

# -------------------------
# HEADER
# -------------------------
st.title("Aevum Lifespan AI")
st.caption("The intelligence layer for human longevity")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("User Profile")

age = st.sidebar.slider("Age", 25, 60, 38)
activity = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

st.sidebar.subheader("Lifestyle Inputs")
sleep_hours = st.sidebar.slider("Avg Sleep (hrs)", 4.0, 9.0, 6.5)
workouts = st.sidebar.slider("Workouts / week", 0, 7, 3)
diet = st.sidebar.selectbox("Diet Quality", ["Poor", "Average", "Good"])

demo = st.sidebar.checkbox("Demo Mode", value=True)

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
# STATE
# -------------------------
if "report_text" not in st.session_state:
    st.session_state.report_text = ""

if "ai_output" not in st.session_state:
    st.session_state.ai_output = ""

# -------------------------
# TABS
# -------------------------
tabs = st.tabs([
    "📊 Your Health Summary",
    "💡 Recommendations",
    "⚠️ Risks",
    "🔗 Integrations",
    "📁 Uploads"
])

# -------------------------
# TAB: UPLOADS
# -------------------------
with tabs[4]:
    st.header("Upload Medical Reports")

    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        st.session_state.report_text = extract_text_from_pdf(file)
        st.success("Report uploaded successfully")

    elif demo:
        st.session_state.report_text = "Cholesterol high, Vitamin D low"
        st.info("Demo data loaded")

# -------------------------
# TAB: INTEGRATIONS
# -------------------------
with tabs[3]:
    st.header("Integrations")

    st.markdown("### Wearables")
    st.success("Apple Watch (simulated) connected")

    wearable_data = pd.DataFrame({
        "Metric": ["Heart Rate", "HRV", "Sleep"],
        "Value": [72, 55, sleep_hours]
    })

    st.dataframe(wearable_data, use_container_width=True)

    st.markdown("### Lifestyle Inputs")
    st.write(f"Sleep: {sleep_hours} hrs")
    st.write(f"Workouts/week: {workouts}")
    st.write(f"Diet: {diet}")

# -------------------------
# AI GENERATION FUNCTION
# -------------------------
def generate_ai_output():
    prompt = f"""
    You are a preventive healthcare AI.

    User:
    Age: {age}
    Activity: {activity}
    Sleep: {sleep_hours}
    Workouts: {workouts}
    Diet: {diet}

    Wearables:
    HR: 72
    HRV: 55

    Medical Report:
    {st.session_state.report_text}

    Provide:
    1. Summary
    2. Risks
    3. Recommendations

    Keep concise and structured.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a longevity AI."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# -------------------------
# PROCESS AI OUTPUT
# -------------------------
if st.session_state.report_text:
    try:
        st.session_state.ai_output = generate_ai_output()
    except:
        st.session_state.ai_output = "AI unavailable"

# Split AI output
def parse_output(text):
    lines = text.split("\n")
    summary, risks, recs = [], [], []

    for line in lines:
        l = line.lower()
        if "risk" in l:
            risks.append(line)
        elif "recommend" in l or "should" in l:
            recs.append(line)
        else:
            summary.append(line)

    return summary, risks, recs

summary, risks, recs = parse_output(st.session_state.ai_output)

# -------------------------
# TAB: SUMMARY
# -------------------------
with tabs[0]:
    st.header("Your Health Summary")

    st.metric("Health Score", "78", "+5")

    st.markdown("""
    **Longevity Status:** Moderate optimization zone.  
    Improvements in sleep and cardiovascular fitness can significantly improve outcomes.
    """)

    st.subheader("Key Insights")
    for s in summary:
        if s.strip():
            st.markdown(f"- {s}")

    st.subheader("Trends")
    st.line_chart([48, 50, 52, 51, 53, 54, 55])

# -------------------------
# TAB: RECOMMENDATIONS
# -------------------------
with tabs[1]:
    st.header("Recommendations")

    for r in recs:
        if r.strip():
            st.success(r)

# -------------------------
# TAB: RISKS
# -------------------------
with tabs[2]:
    st.header("Risk Signals")

    for r in risks:
        if r.strip():
            st.warning(r)

    st.warning("""
    Baseline: Elevated LDL + low activity may increase cardiovascular risk
    """)
