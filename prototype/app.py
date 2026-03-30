import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI

# Optional PDF parsing (safe import)
try:
    import PyPDF2
    PDF_ENABLED = True
except:
    PDF_ENABLED = False

# -------------------------
# INIT
# -------------------------
st.set_page_config(page_title="Aevum Lifespan AI", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------
# SESSION STATE
# -------------------------
if "report_text" not in st.session_state:
    st.session_state.report_text = ""

if "ai_output" not in st.session_state:
    st.session_state.ai_output = ""

# -------------------------
# HEADER
# -------------------------
st.title("Aevum Lifespan AI")
st.caption("The intelligence layer for human longevity")

# -------------------------
# SIDEBAR (INPUTS)
# -------------------------
st.sidebar.header("Your Profile")

age = st.sidebar.slider("Age", 25, 65, 38)
activity = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

st.sidebar.subheader("Lifestyle")
sleep = st.sidebar.slider("Sleep (hrs)", 4.0, 9.0, 6.5)
workouts = st.sidebar.slider("Workouts/week", 0, 7, 3)
diet = st.sidebar.selectbox("Diet Quality", ["Poor", "Average", "Good"])

demo = st.sidebar.checkbox("Demo Mode", value=True)

# -------------------------
# TABS
# -------------------------
tab_summary, tab_reco, tab_risk, tab_integrations, tab_uploads = st.tabs([
    "📊 Your Health Summary",
    "💡 Recommendations",
    "⚠️ Risks",
    "🔗 Integrations",
    "📁 Uploads"
])

# -------------------------
# PDF PARSER
# -------------------------
def extract_pdf(file):
    if not PDF_ENABLED:
        return "PDF parsing not available"
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# -------------------------
# UPLOADS TAB
# -------------------------
with tab_uploads:
    st.header("Upload Medical Reports")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        st.session_state.report_text = extract_pdf(uploaded_file)
        st.success("Report uploaded successfully")

    elif demo:
        st.session_state.report_text = """
        Cholesterol: High
        Vitamin D: Low
        Triglycerides: Slightly elevated
        """
        st.info("Using demo medical report")

# -------------------------
# INTEGRATIONS TAB
# -------------------------
with tab_integrations:
    st.header("Connected Data Sources")

    st.subheader("Wearables")
    st.success("Apple Watch (Simulated Connected)")

    wearable_df = pd.DataFrame({
        "Metric": ["Heart Rate", "HRV", "Sleep"],
        "Value": [72, 55, sleep]
    })

    st.dataframe(wearable_df, use_container_width=True)

    st.subheader("Lifestyle Data")
    st.write(f"Sleep: {sleep} hrs")
    st.write(f"Workouts/week: {workouts}")
    st.write(f"Diet Quality: {diet}")

# -------------------------
# AI ENGINE
# -------------------------
def generate_ai():
    prompt = f"""
    You are a preventive healthcare AI focused on longevity.

    User:
    Age: {age}
    Activity: {activity}
    Sleep: {sleep}
    Workouts: {workouts}
    Diet: {diet}

    Wearables:
    HR: 72
    HRV: 55

    Medical Report:
    {st.session_state.report_text}

    Provide structured output:

    1. Summary
    2. Risks
    3. Recommendations

    Use bullet points.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a medical AI."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Run AI only once per load
if st.session_state.report_text and not st.session_state.ai_output:
    try:
        st.session_state.ai_output = generate_ai()
    except:
        st.session_state.ai_output = "AI temporarily unavailable"

# -------------------------
# PARSE OUTPUT
# -------------------------
def parse_ai(text):
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

summary, risks, recs = parse_ai(st.session_state.ai_output)

# -------------------------
# SUMMARY TAB
# -------------------------
with tab_summary:
    st.header("Your Health Summary")

    st.metric("Health Score", "78", "+5")

    st.markdown("""
    **Longevity Status:**  
    You are in a moderate optimization zone. Improvements in sleep and activity can significantly improve outcomes.
    """)

    st.subheader("Key Insights")
    for s in summary:
        if s.strip():
            st.markdown(f"- {s}")

    st.subheader("Health Trends")

    hrv = [48, 50, 52, 51, 53, 54, 55]
    sleep_trend = [6.0, 6.2, 6.5, 6.3, 6.6, 6.8, sleep]

    trend_df = pd.DataFrame({
        "HRV": hrv,
        "Sleep": sleep_trend
    })

    st.line_chart(trend_df)

# -------------------------
# RECOMMENDATIONS TAB
# -------------------------
with tab_reco:
    st.header("Recommendations")

    for r in recs:
        if r.strip():
            st.success(r)

    st.info("Follow these consistently for 4–6 weeks for measurable improvement")

# -------------------------
# RISKS TAB
# -------------------------
with tab_risk:
    st.header("Risk Signals")

    for r in risks:
        if r.strip():
            st.warning(r)

    st.warning("Baseline: Elevated cholesterol + low activity increases cardiovascular risk")
