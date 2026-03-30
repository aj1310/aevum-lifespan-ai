import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Aevum Lifespan AI", layout="wide")

# Title section
st.title("Aevum Lifespan AI")
st.caption("The intelligence layer for human longevity")
st.markdown("### Your health, decoded across biology, behavior, and time.")

# Sidebar (User Profile)
st.sidebar.header("User Profile")

age = st.sidebar.slider("Age", 25, 60, 38)
activity = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

# Demo mode toggle
demo = st.sidebar.checkbox("Enable Demo Mode", value=True)

if demo:
    st.sidebar.success("Demo Mode Active")

# Upload section
st.header("Upload Medical Report")
file = st.file_uploader("Upload your report (PDF/Image)")

if file or demo:
    st.success("Report processed successfully")

    st.subheader("AI Summary")
    st.write("""
    - Cholesterol slightly elevated  
    - Vitamin D deficiency  
    - Recommend increased activity and sunlight exposure  
    """)

# Wearable Data
st.header("Wearable Data (Simulated)")

data = pd.DataFrame({
    "Metric": ["Heart Rate", "HRV", "Sleep"],
    "Value": [72, 55, 6.5]
})

st.table(data)

# Health Score
st.header("Health Score")
st.metric(label="Overall Score", value="78", delta="+5")
st.caption("Based on sleep quality, HRV trends, and activity levels")

# Trends
st.header("Health Trends")

days = list(range(1, 8))
hrv = [48, 50, 52, 51, 53, 54, 55]

st.line_chart({"HRV Trend": hrv})

# AI Insight
st.header("AI Insight")

st.info("""
Your improving sleep consistency (+18% over the last 2 weeks) has positively impacted your HRV, 
indicating better recovery and reduced physiological stress.

However, your resting heart rate remains slightly elevated, suggesting an opportunity 
to improve cardiovascular fitness through consistent moderate-intensity activity.
""")

# Risk Signals
st.header("Risk Signals")

st.warning("""
Elevated LDL cholesterol combined with low activity levels may increase cardiovascular risk over time.

Suggested Action:
- 150 mins/week moderate cardio
- Reduce processed fats
""")
