"""
Streamlit frontend for the Student Depression Prediction system.
Premium Apple-inspired design with glassmorphism and animations.

Usage:
    streamlit run frontend/app.py
"""
import os
import sys

import requests
import streamlit as st

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# --- Configuration ---
API_URL = os.getenv("API_URL", "http://localhost:8000")

# --- Page Config ---
st.set_page_config(
    page_title="NeuroSense — Depression Risk AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Premium CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global Reset */
    .stApp {
        background: linear-gradient(160deg, #0a0a1a 0%, #1a1a3e 40%, #0d0d2b 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide default header/footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Dark scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 3px; }

    /* Hero Section */
    .hero {
        text-align: center;
        padding: 2rem 0 1rem;
        position: relative;
    }
    .hero-icon {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        display: block;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa, #818cf8, #6366f1, #818cf8);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 4s ease infinite;
        margin: 0;
        letter-spacing: -0.02em;
    }
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-sub {
        color: rgba(255,255,255,0.5);
        font-size: 1.05rem;
        font-weight: 400;
        margin-top: 0.4rem;
        letter-spacing: 0.02em;
    }
    .hero-line {
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #818cf8, #a78bfa);
        border-radius: 2px;
        margin: 1.2rem auto 0;
    }

    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin: 0.8rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(255, 255, 255, 0.12);
        transform: translateY(-2px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    .card-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: rgba(255,255,255,0.4);
        margin-bottom: 1rem;
    }
    .card-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }

    /* Section Header */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
        margin: 2rem 0 1rem;
        letter-spacing: -0.01em;
    }

    /* Streamlit overrides */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #a78bfa) !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border-color: rgba(255,255,255,0.1) !important;
        color: #fff !important;
    }
    label, .stSlider label, .stSelectbox label {
        color: rgba(255,255,255,0.75) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #fff !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.5) !important;
    }

    /* Predict Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa) !important;
        background-size: 200% 200% !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        letter-spacing: 0.02em !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
    }
    .stButton > button:hover {
        background-position: right center !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.6) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Result Boxes */
    .result-safe {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(16, 185, 129, 0.08));
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        animation: fadeInUp 0.6s ease-out;
    }
    .result-risk {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(248, 113, 113, 0.08));
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        animation: fadeInUp 0.6s ease-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-icon { font-size: 3rem; margin-bottom: 0.5rem; display: block; }
    .result-label {
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0.3rem 0;
        letter-spacing: -0.01em;
    }
    .result-safe .result-label { color: #22c55e; }
    .result-risk .result-label { color: #ef4444; }
    .result-conf {
        font-size: 1rem;
        color: rgba(255,255,255,0.5);
        font-weight: 400;
    }
    .result-conf span {
        font-weight: 700;
        color: rgba(255,255,255,0.85);
    }

    /* Probability Bar */
    .prob-container {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .prob-label {
        color: rgba(255,255,255,0.7);
        font-weight: 500;
        font-size: 0.9rem;
    }
    .prob-value {
        color: #fff;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .prob-bar-bg {
        flex: 1;
        height: 6px;
        background: rgba(255,255,255,0.08);
        border-radius: 3px;
        margin: 0 1rem;
        overflow: hidden;
    }
    .prob-bar-fill-safe {
        height: 100%;
        background: linear-gradient(90deg, #22c55e, #4ade80);
        border-radius: 3px;
        transition: width 1s ease-out;
    }
    .prob-bar-fill-risk {
        height: 100%;
        background: linear-gradient(90deg, #ef4444, #f87171);
        border-radius: 3px;
        transition: width 1s ease-out;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 35, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: rgba(255,255,255,0.7) !important;
    }

    /* Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .status-online {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.25);
    }
    .status-offline {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
    }
    .status-online .status-dot { background: #4ade80; box-shadow: 0 0 6px #4ade80; }
    .status-offline .status-dot { background: #f87171; box-shadow: 0 0 6px #f87171; }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: rgba(255,255,255,0.2);
        font-size: 0.8rem;
        letter-spacing: 0.05em;
    }
    .app-footer a {
        color: rgba(255,255,255,0.35);
        text-decoration: none;
    }

    /* Expander */
    .streamlit-expanderHeader {
        color: rgba(255,255,255,0.7) !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.03) !important;
        border-color: rgba(255,255,255,0.06) !important;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.06) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Header ---
st.markdown("""
<div class="hero">
    <span class="hero-icon">🧬</span>
    <h1>NeuroSense</h1>
    <div class="hero-sub">AI-Powered Student Depression Risk Assessment</div>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚡ System Status")
    try:
        health_resp = requests.get(f"{API_URL}/health", timeout=10)
        if health_resp.status_code == 200:
            health = health_resp.json()
            st.markdown(
                '<span class="status-pill status-online">'
                '<span class="status-dot"></span>API Online</span>',
                unsafe_allow_html=True,
            )
            st.markdown(f"""
            <div style="margin-top: 1rem; color: rgba(255,255,255,0.5); font-size: 0.85rem;">
                <div style="margin-bottom: 6px;">
                    Model: <span style="color: #4ade80;">{'Loaded' if health['model_loaded'] else 'Not Loaded'}</span>
                </div>
                <div>Version: <span style="color: rgba(255,255,255,0.7);">{health['version']}</span></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<span class="status-pill status-offline">'
                '<span class="status-dot"></span>API Error</span>',
                unsafe_allow_html=True,
            )
    except requests.ConnectionError:
        st.markdown(
            '<span class="status-pill status-offline">'
            '<span class="status-dot"></span>API Offline</span>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.markdown(
            '<span class="status-pill status-offline">'
            f'<span class="status-dot"></span>Error</span>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 🧬 About")
    st.markdown("""
    <div style="color: rgba(255,255,255,0.45); font-size: 0.85rem; line-height: 1.7;">
        NeuroSense uses a <b style="color: rgba(255,255,255,0.7);">Random Forest
        classifier</b> trained on <b style="color: rgba(255,255,255,0.7);">100K
        student records</b> to predict depression risk from lifestyle factors.
        <br><br>
        Built with <b style="color: rgba(255,255,255,0.7);">FastAPI</b>,
        <b style="color: rgba(255,255,255,0.7);">scikit-learn</b>, and
        <b style="color: rgba(255,255,255,0.7);">Streamlit</b>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="color: rgba(255,255,255,0.25); font-size: 0.75rem; text-align: center;">
        Student Depression Predictor<br>MTA Advanced Analytics II
    </div>
    """, unsafe_allow_html=True)

# --- Input Form ---
st.markdown(
    '<div class="section-header">📋 Student Profile</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="glass-card">'
        '<div class="card-title"><span class="card-icon">👤</span>Demographics</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    age = st.slider("Age", min_value=15, max_value=30, value=20, step=1)
    gender = st.selectbox("Gender", options=["Male", "Female"])
    department = st.selectbox(
        "Department",
        options=["Science", "Engineering", "Medical", "Arts", "Business"],
    )

with col2:
    st.markdown(
        '<div class="glass-card">'
        '<div class="card-title"><span class="card-icon">📚</span>Academics</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    cgpa = st.slider("CGPA", min_value=0.0, max_value=4.0, value=3.0, step=0.01)
    study_hours = st.slider(
        "Study Hours (daily)", min_value=0.0, max_value=15.0, value=4.0, step=0.1
    )
    sleep_duration = st.slider(
        "Sleep Duration (hrs)", min_value=0.0, max_value=15.0, value=7.0, step=0.1
    )

with col3:
    st.markdown(
        '<div class="glass-card">'
        '<div class="card-title"><span class="card-icon">🏃</span>Lifestyle</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    social_media_hours = st.slider(
        "Social Media (hrs/day)", min_value=0.0, max_value=15.0, value=3.0, step=0.1
    )
    physical_activity = st.slider(
        "Physical Activity", min_value=0, max_value=200, value=80, step=1
    )
    stress_level = st.slider(
        "Stress Level", min_value=0, max_value=10, value=5, step=1
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- Predict Button ---
if st.button("🔮  Analyze Risk", use_container_width=True):
    payload = {
        "Age": age,
        "Gender": gender,
        "Department": department,
        "CGPA": cgpa,
        "Sleep_Duration": sleep_duration,
        "Study_Hours": study_hours,
        "Social_Media_Hours": social_media_hours,
        "Physical_Activity": physical_activity,
        "Stress_Level": stress_level,
    }

    try:
        with st.spinner(""):
            response = requests.post(
                f"{API_URL}/predict", json=payload, timeout=15
            )

        if response.status_code == 200:
            result = response.json()

            st.markdown(
                '<div class="section-header">🎯 Analysis Result</div>',
                unsafe_allow_html=True,
            )

            # Result card
            if result["prediction"] == 1:
                prob = result["probability_depression"]
                st.markdown(
                    f"""<div class="result-risk">
                        <span class="result-icon">⚠️</span>
                        <div class="result-label">Depression Risk Detected</div>
                        <div class="result-conf">Confidence: <span>{prob:.1%}</span></div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                prob = result["probability_no_depression"]
                st.markdown(
                    f"""<div class="result-safe">
                        <span class="result-icon">✅</span>
                        <div class="result-label">Low Risk</div>
                        <div class="result-conf">Confidence: <span>{prob:.1%}</span></div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Probability bars
            no_dep = result["probability_no_depression"]
            dep = result["probability_depression"]

            st.markdown(f"""
            <div class="prob-container">
                <span class="prob-label">No Depression</span>
                <div class="prob-bar-bg">
                    <div class="prob-bar-fill-safe" style="width: {no_dep * 100}%"></div>
                </div>
                <span class="prob-value">{no_dep:.1%}</span>
            </div>
            <div class="prob-container">
                <span class="prob-label">Depression Risk</span>
                <div class="prob-bar-bg">
                    <div class="prob-bar-fill-risk" style="width: {dep * 100}%"></div>
                </div>
                <span class="prob-value">{dep:.1%}</span>
            </div>
            """, unsafe_allow_html=True)

            # Metrics row
            st.markdown("<br>", unsafe_allow_html=True)
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.metric("No Depression", f"{no_dep:.2%}")
            with mc2:
                st.metric("Depression", f"{dep:.2%}")
            with mc3:
                st.metric("Model Version", result["model_version"])

            # Input summary
            with st.expander("📝 Input Summary"):
                st.json(payload)

        elif response.status_code == 503:
            st.error("⚠️ Model not loaded. Please try again later.")
        else:
            st.error(f"API Error: {response.status_code} — {response.text}")

    except requests.ConnectionError:
        st.error(
            "❌ Cannot connect to API. Make sure FastAPI is running on " + API_URL
        )
    except Exception as e:
        st.error(f"Error: {e}")

# --- Footer ---
st.markdown("""
<div class="app-footer">
    NeuroSense — Student Depression Risk AI &nbsp;·&nbsp;
    Built with FastAPI + Streamlit + scikit-learn
</div>
""", unsafe_allow_html=True)
