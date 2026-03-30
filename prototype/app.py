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

# Health score
st.header("Health Score")
st.metric(label="Overall Score", value="78", delta="+5")

# Insight
st.header("AI Insight")
st.info("Improved sleep consistency has positively impacted your HRV.")
