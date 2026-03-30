import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aevum Lifespan AI", layout="wide")

st.title("Aevum Lifespan AI")
st.caption("The intelligence layer for human longevity")

st.markdown("### Your health, decoded across biology, behavior, and time.")

# Sidebar
st.sidebar.header("User Profile")
age = st.sidebar.slider("Age", 25, 60, 38)
activity = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

demo = st.sidebar.checkbox("Enable Demo Mode", value=True)

if demo:
    st.success("Demo Mode Active: Showing sample insights")

# Upload report
st.header("Upload Medical Report")
file = st.file_uploader("Upload your report (PDF/Image)")

if file:
    st.success("Report uploaded successfully")
    st.subheader("AI Summary")
    st.write("""
    - Cholesterol slightly elevated  
    - Vitamin D deficiency  
    - Recommend increased activity and sunlight exposure  
    """)

# Simulated wearable data
st.header("Wearable Data (Simulated)")

data = pd.DataFrame({
    "Metric": ["Heart Rate", "HRV", "Sleep"],
    "Value": [72, 55, 6.5]
})

st.table(data)

import numpy as np

st.header("Health Trends")

days = list(range(1, 8))
hrv = [48, 50, 52, 51, 53, 54, 55]

st.line_chart({"HRV Trend": hrv})

# Health score
st.header("Health Score")
st.metric(label="Overall Score", value="78", delta="+5")

st.caption("Based on sleep quality, HRV trends, and activity levels")

st.header("AI Insight")

st.info("""
Your improving sleep consistency (+18% over the last 2 weeks) has positively impacted your HRV, 
indicating better recovery and reduced physiological stress.

However, your resting heart rate remains slightly elevated, suggesting an opportunity 
to improve cardiovascular fitness through consistent moderate-intensity activity.
""")
