import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Aevum Lifespan AI", layout="wide")

# -------------------------
# SESSION STATE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "data" not in st.session_state:
    st.session_state.data = {}

# -------------------------
# LANDING PAGE (PUBLIC)
# -------------------------
def landing_page():
    st.markdown("""
    <style>
    .hero {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        padding: 60px;
        border-radius: 20px;
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hero">', unsafe_allow_html=True)

    st.title("Aevum Lifespan AI")
    st.subheader("The Intelligence Layer for Your Health")

    st.markdown("""
    Combine your **medical reports + wearable data + lifestyle**  
    into one intelligent system that tells you:

    - What matters  
    - What to fix  
    - How to improve  
    """)

    st.markdown("### 🚀 Built for longevity, performance, and clarity")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## Why Aevum?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📊 Unified Health Data")

    with col2:
        st.info("🧠 Smart Insights")

    with col3:
        st.info("⚡ Actionable Recommendations")

    st.markdown("---")

    name = st.text_input("Enter your name to begin")

    if st.button("Get Started"):
        if name:
            st.session_state.user = name
            st.rerun()

# -------------------------
# BIOMARKER EXTRACTION
# -------------------------
def extract(text):
    def find(p):
        m = re.search(p, text, re.I)
        return float(m.group(1)) if m else None

    return {
        "cholesterol": find(r"cholesterol.*?(\d+)"),
        "ldl": find(r"ldl.*?(\d+)"),
        "hdl": find(r"hdl.*?(\d+)"),
        "vitamin_d": find(r"vitamin\s*d.*?(\d+)"),
        "glucose": find(r"glucose.*?(\d+)")
    }

# -------------------------
# INSIGHTS ENGINE
# -------------------------
def insights(data, hr, hrv, sleep):
    summary = []
    actions = []
    risks = []

    # Clinical
    if data.get("cholesterol") and data["cholesterol"] > 200:
        summary.append("High cholesterol detected")
        risks.append("Cardiovascular risk")
        actions.append("Improve diet and increase activity")

    if data.get("vitamin_d") and data["vitamin_d"] < 30:
        summary.append("Low Vitamin D")
        actions.append("Increase sunlight exposure")

    # Wearable
    if hrv < 40:
        summary.append("Low recovery (HRV)")
        actions.append("Prioritize rest and recovery")

    if sleep < 6:
        summary.append("Poor sleep detected")
        actions.append("Improve sleep schedule")

    if not summary:
        summary.append("Your health looks stable")

    return summary, actions, risks

# -------------------------
# PRODUCT APP
# -------------------------
def app():
    st.sidebar.title(f"Welcome {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.title("Your Health Dashboard")

    # -------------------------
    # ONBOARDING SECTION
    # -------------------------
    st.header("Step 1: Upload Health Data")

    report = st.text_area("Paste your medical report")

    if st.button("Extract Data"):
        data = extract(report)
        st.session_state.data.update(data)
        st.success("Data extracted")

    st.header("Step 2: Connect Wearable")

    hr = st.slider("Heart Rate", 50, 100, 72)
    hrv = st.slider("HRV", 20, 100, 55)
    sleep = st.slider("Sleep Hours", 4.0, 9.0, 6.5)

    st.header("Step 3: Your Insights")

    if st.session_state.data:
        summary, actions, risks = insights(st.session_state.data, hr, hrv, sleep)

        st.subheader("🧠 Insights")
        for s in summary:
            st.write(f"- {s}")

        st.subheader("⚠️ Risks")
        for r in risks:
            st.warning(r)

        st.subheader("✅ Actions")
        for a in actions:
            st.success(a)

    else:
        st.info("Upload your report to see insights")

# -------------------------
# ROUTER
# -------------------------
if st.session_state.user is None:
    landing_page()
else:
    app()
