import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

# Longevity narrative
st.markdown("""
**Longevity Interpretation:**  
You are currently in a *moderate optimization zone*. Improvements in sleep consistency and cardiovascular fitness 
can significantly enhance long-term health outcomes.
""")

# Trends
st.header("Health Trends")

hrv = [48, 50, 52, 51, 53, 54, 55]
st.line_chart({"HRV Trend": hrv})

# AI Insight (REAL AI)
st.header("AI Insight")

if demo:
    try:
        prompt = f"""
        You are a medical AI assistant focused on preventive health and longevity.

        User profile:
        Age: {age}
        Activity level: {activity}

        Wearable data:
        - Heart rate: 72
        - HRV: 55
        - Sleep: 6.5 hours

        Provide output in 3 sections:
        1. Key Insights
        2. Risk Indicators
        3. Actionable Recommendations

        Keep it concise and structured using bullet points.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a health intelligence AI."},
                {"role": "user", "content": prompt}
            ]
        )

        ai_output = response.choices[0].message.content

        # Parse response into sections
        sections = ai_output.split("\n")

        insights = []
        risks = []
        actions = []

        for line in sections:
            line_lower = line.lower()

            if "risk" in line_lower:
                risks.append(line)
            elif "recommend" in line_lower or "should" in line_lower:
                actions.append(line)
            else:
                insights.append(line)

        # Display sections
        st.subheader("🧠 Key Insights")
        for i in insights:
            if i.strip():
                st.markdown(f"- {i}")

        st.subheader("⚠️ Risk Signals")
        for r in risks:
            if r.strip():
                st.warning(r)

        st.subheader("✅ Action Plan")
        for a in actions:
            if a.strip():
                st.success(a)

    except Exception as e:
        st.error("AI service unavailable. Please check API key or try again.")
        st.info("""
        Sample Insight:
        Your improving sleep consistency is positively impacting HRV, indicating better recovery.
        Focus on cardiovascular activity to further improve heart health.
        """)

else:
    st.info("Upload a report to generate insights.")

# Static Risk Signals (backup framing)
st.header("Baseline Risk Signals")

st.warning("""
Elevated LDL cholesterol combined with low activity levels may increase cardiovascular risk over time.

Suggested Action:
- 150 mins/week moderate cardio
- Reduce processed fats
""")

# Future vision
st.header("What Aevum will do next")

st.markdown("""
In future versions, Aevum will:

- Continuously track your health across time  
- Predict potential risks before they emerge  
- Recommend personalized lifestyle interventions  
- Enable doctor collaboration with AI-assisted summaries  
""")
