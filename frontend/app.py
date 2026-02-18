"""
Streamlit frontend for the Student Depression Prediction system.
Clean, premium design with explicit light theme.

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

# --- CSS (all text colors explicitly set to dark) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Force all text dark */
    .stApp, .stApp * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stApp {
        background-color: #f8f9fc !important;
    }

    /* Hide chrome */
    #MainMenu, header, footer { visibility: hidden; }

    /* Force ALL text dark */
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    .stText, p, span, div, li, td, th {
        color: #1f2937 !important;
    }

    /* ===== HERO ===== */
    .hero-wrap {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.25);
    }
    .hero-wrap * { color: #fff !important; }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        color: #fff !important;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 5px 14px;
        border-radius: 20px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        backdrop-filter: blur(4px);
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #fff !important;
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin: 0;
    }
    .hero-desc {
        color: rgba(255,255,255,0.85) !important;
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.7rem;
        line-height: 1.6;
    }

    /* ===== SECTION ===== */
    .section-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #111827 !important;
        margin: 1.5rem 0 1rem;
        letter-spacing: -0.01em;
    }
    .section-title span { color: #6366f1 !important; }

    /* ===== INPUT CARDS ===== */
    .input-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        transition: all 0.25s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .input-card:hover {
        border-color: #c7d2fe;
        box-shadow: 0 6px 20px rgba(99,102,241,0.08);
        transform: translateY(-1px);
    }
    .card-head {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-icon { font-size: 1.2rem; }
    .card-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #6366f1 !important;
    }

    /* ===== STREAMLIT WIDGET OVERRIDES ===== */
    /* Labels */
    label, .stSlider label, .stSelectbox label,
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }

    /* Slider track */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }
    /* Slider value */
    .stSlider [data-testid="stTickBarMax"],
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stThumbValue"] {
        color: #374151 !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #ffffff !important;
        border-color: #e5e7eb !important;
        color: #1f2937 !important;
    }
    .stSelectbox > div > div > div {
        color: #1f2937 !important;
    }

    /* Metric */
    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-weight: 600 !important;
    }

    /* ===== BUTTON ===== */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }
    .stButton > button p, .stButton > button span {
        color: #fff !important;
    }

    /* ===== RESULTS ===== */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-card {
        border-radius: 20px;
        padding: 2.2rem 2rem;
        text-align: center;
        animation: slideUp 0.5s ease-out;
        margin-bottom: 1rem;
    }
    .result-safe {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        border: 1.5px solid #6ee7b7;
    }
    .result-risk {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border: 1.5px solid #fca5a5;
    }
    .result-icon { font-size: 2.8rem; display: block; margin-bottom: 0.4rem; }
    .result-label {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }
    .result-safe .result-label { color: #059669 !important; }
    .result-risk .result-label { color: #dc2626 !important; }
    .result-safe .result-conf { color: #065f46 !important; }
    .result-risk .result-conf { color: #991b1b !important; }
    .result-conf {
        font-size: 0.95rem;
        margin-top: 4px;
    }
    .result-conf b { font-weight: 800; }

    /* ===== PROBABILITY BARS ===== */
    .prob-row {
        display: flex;
        align-items: center;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .prob-name {
        min-width: 140px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #374151 !important;
    }
    .prob-track {
        flex: 1;
        height: 10px;
        background: #f3f4f6;
        border-radius: 5px;
        margin: 0 1rem;
        overflow: hidden;
    }
    .prob-fill-green {
        height: 100%;
        background: linear-gradient(90deg, #34d399, #10b981);
        border-radius: 5px;
        transition: width 0.8s ease-out;
    }
    .prob-fill-red {
        height: 100%;
        background: linear-gradient(90deg, #f87171, #ef4444);
        border-radius: 5px;
        transition: width 0.8s ease-out;
    }
    .prob-pct {
        font-weight: 800;
        font-size: 1rem;
        color: #111827 !important;
        min-width: 55px;
        text-align: right;
    }

    /* ===== STATS ROW ===== */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin: 1.2rem 0;
    }
    .stat-box {
        flex: 1;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .stat-box:hover {
        border-color: #c7d2fe;
        box-shadow: 0 4px 12px rgba(99,102,241,0.08);
    }
    .stat-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #111827 !important;
    }
    .stat-label {
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9ca3af !important;
        margin-top: 4px;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
    }
    section[data-testid="stSidebar"] * {
        color: #374151 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #111827 !important;
    }

    /* Status */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .status-up {
        background: #ecfdf5;
        color: #059669 !important;
        border: 1px solid #a7f3d0;
    }
    .status-down {
        background: #fef2f2;
        color: #dc2626 !important;
        border: 1px solid #fecaca;
    }
    .dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-green { background: #10b981; box-shadow: 0 0 6px rgba(16,185,129,0.5); }
    .dot-red { background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,0.5); }

    .sidebar-info {
        color: #6b7280 !important;
        font-size: 0.82rem;
        line-height: 1.7;
        margin-top: 0.8rem;
    }
    .sidebar-info b { color: #374151 !important; }

    /* ===== FOOTER ===== */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
    }
    .app-footer, .app-footer * { color: #d1d5db !important; }

    /* Divider */
    hr { border-color: #e5e7eb !important; }

    /* Expander */
    .streamlit-expanderHeader {
        color: #374151 !important;
        font-weight: 600 !important;
    }

    /* Alerts / toast */
    .stAlert p, .stAlert span { color: inherit !important; }
</style>
""", unsafe_allow_html=True)

# ───────────────────────── HERO ─────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🧬 AI-Powered Assessment</div>
    <div class="hero-title">Student Depression<br>Risk Predictor</div>
    <div class="hero-desc">
        Predict depression risk by analyzing lifestyle data.<br>
        Machine learning model trained on 100,000 student records.
    </div>
</div>
""", unsafe_allow_html=True)

# ───────────────────────── SIDEBAR ─────────────────────────
with st.sidebar:
    st.markdown("### ⚡ System Status")
    try:
        health_resp = requests.get(f"{API_URL}/health", timeout=10)
        if health_resp.status_code == 200:
            health = health_resp.json()
            st.markdown(
                '<span class="status-badge status-up">'
                '<span class="dot dot-green"></span>API Online</span>',
                unsafe_allow_html=True,
            )
            model_status = '✅ Loaded' if health['model_loaded'] else '❌ Not loaded'
            st.markdown(f"""
            <div class="sidebar-info">
                Model: <b>{model_status}</b><br>
                Version: <b>{health['version']}</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<span class="status-badge status-down">'
                '<span class="dot dot-red"></span>API Error</span>',
                unsafe_allow_html=True,
            )
    except Exception:
        st.markdown(
            '<span class="status-badge status-down">'
            '<span class="dot dot-red"></span>API Offline</span>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    <div class="sidebar-info">
        This tool uses a <b>Random Forest classifier</b>
        trained on <b>100,000 student records</b> to assess
        depression risk from lifestyle and academic factors.
        <br><br>
        <b>9 features</b> analyzed including age, sleep,
        stress, CGPA, and physical activity.
        <br><br>
        Built with <b>FastAPI</b> · <b>scikit-learn</b> · <b>Streamlit</b>
    </div>
    """, unsafe_allow_html=True)

# ───────────────────────── INPUT FORM ─────────────────────────
st.markdown(
    '<div class="section-title">📋 Enter <span>Student Details</span></div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="input-card">'
        '<div class="card-head">'
        '<span class="card-icon">👤</span>'
        '<span class="card-label">Demographics</span>'
        '</div></div>',
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
        '<div class="input-card">'
        '<div class="card-head">'
        '<span class="card-icon">📚</span>'
        '<span class="card-label">Academics</span>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    cgpa = st.slider("CGPA", min_value=0.0, max_value=4.0, value=3.0, step=0.01)
    study_hours = st.slider(
        "Study Hours / day", min_value=0.0, max_value=15.0, value=4.0, step=0.1
    )
    sleep_duration = st.slider(
        "Sleep Duration (hrs)", min_value=0.0, max_value=15.0, value=7.0, step=0.1
    )

with col3:
    st.markdown(
        '<div class="input-card">'
        '<div class="card-head">'
        '<span class="card-icon">🏃</span>'
        '<span class="card-label">Lifestyle</span>'
        '</div></div>',
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

# ───────────────────────── PREDICT ─────────────────────────
if st.button("🔮  Analyze Depression Risk", use_container_width=True):
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
        with st.spinner("Analyzing student profile..."):
            response = requests.post(
                f"{API_URL}/predict", json=payload, timeout=15
            )

        if response.status_code == 200:
            result = response.json()

            st.markdown(
                '<div class="section-title">🎯 Analysis <span>Result</span></div>',
                unsafe_allow_html=True,
            )

            # Result Card
            if result["prediction"] == 1:
                prob = result["probability_depression"]
                st.markdown(f"""
                <div class="result-card result-risk">
                    <span class="result-icon">⚠️</span>
                    <div class="result-label">Depression Risk Detected</div>
                    <div class="result-conf">Confidence: <b>{prob:.1%}</b></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                prob = result["probability_no_depression"]
                st.markdown(f"""
                <div class="result-card result-safe">
                    <span class="result-icon">✅</span>
                    <div class="result-label">Low Risk — Healthy</div>
                    <div class="result-conf">Confidence: <b>{prob:.1%}</b></div>
                </div>
                """, unsafe_allow_html=True)

            # Probability Bars
            no_dep = result["probability_no_depression"]
            dep = result["probability_depression"]

            st.markdown(f"""
            <div class="prob-row">
                <span class="prob-name">✅ No Depression</span>
                <div class="prob-track">
                    <div class="prob-fill-green" style="width:{no_dep*100}%"></div>
                </div>
                <span class="prob-pct">{no_dep:.1%}</span>
            </div>
            <div class="prob-row">
                <span class="prob-name">⚠️ Depression</span>
                <div class="prob-track">
                    <div class="prob-fill-red" style="width:{dep*100}%"></div>
                </div>
                <span class="prob-pct">{dep:.1%}</span>
            </div>
            """, unsafe_allow_html=True)

            # Stats Row
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-value">{no_dep:.0%}</div>
                    <div class="stat-label">No Depression</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{dep:.0%}</div>
                    <div class="stat-label">Depression Risk</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{result['model_version']}</div>
                    <div class="stat-label">Model Version</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Input summary
            with st.expander("📝 View Input Summary"):
                st.json(payload)

        elif response.status_code == 503:
            st.error("⚠️ Model not loaded. Try again shortly.")
        else:
            st.error(f"API Error {response.status_code}: {response.text}")

    except requests.ConnectionError:
        st.error(
            "❌ Cannot connect to the API. Ensure FastAPI is running at " + API_URL
        )
    except Exception as e:
        st.error(f"Error: {e}")

# ───────────────────────── FOOTER ─────────────────────────
st.markdown("---")
st.markdown("""
<div class="app-footer">
    NeuroSense · Student Depression Risk Assessment<br>
    FastAPI · scikit-learn · Streamlit · MTA Advanced Analytics II
</div>
""", unsafe_allow_html=True)
