"""
Streamlit frontend for the Student Depression Prediction system.
Clean, premium design inspired by modern tech product pages.

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

# --- Premium Light Theme CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ===== GLOBAL ===== */
    .stApp {
        background: #fafafa;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    #MainMenu, header, footer { visibility: hidden; }

    /* ===== HERO ===== */
    .hero-section {
        text-align: center;
        padding: 3rem 1rem 2rem;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ede9fe, #e0e7ff);
        color: #6366f1;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 6px 16px;
        border-radius: 20px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        color: #111827;
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin: 0;
    }
    .hero-title span {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        color: #6b7280;
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.8rem;
        max-width: 520px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }

    /* ===== CARDS ===== */
    .info-card {
        background: #ffffff;
        border: 1px solid #f0f0f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.25s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .info-card:hover {
        border-color: #e0e0e0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.2rem;
    }
    .card-emoji { font-size: 1.4rem; }
    .card-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #9ca3af;
    }

    /* ===== SECTION TITLES ===== */
    .section-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #111827;
        margin: 2.5rem 0 1rem;
        letter-spacing: -0.02em;
    }
    .section-title span { color: #6366f1; }

    /* ===== STREAMLIT OVERRIDES ===== */
    label, .stSlider label, .stSelectbox label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }
    div[data-testid="stMetricValue"] {
        font-weight: 800 !important;
        color: #111827 !important;
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
        letter-spacing: 0.01em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ===== RESULT CARDS ===== */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-card {
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        animation: slideUp 0.5s ease-out;
    }
    .result-safe {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        border: 1px solid #a7f3d0;
    }
    .result-risk {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border: 1px solid #fecaca;
    }
    .result-icon { font-size: 3rem; display: block; margin-bottom: 0.5rem; }
    .result-label {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }
    .result-safe .result-label { color: #059669; }
    .result-risk .result-label { color: #dc2626; }
    .result-conf {
        font-size: 0.95rem;
        color: #6b7280;
        margin-top: 4px;
    }
    .result-conf b { color: #111827; }

    /* ===== PROBABILITY BARS ===== */
    .prob-row {
        display: flex;
        align-items: center;
        background: #fff;
        border: 1px solid #f0f0f0;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .prob-name {
        min-width: 130px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #374151;
    }
    .prob-track {
        flex: 1;
        height: 8px;
        background: #f3f4f6;
        border-radius: 4px;
        margin: 0 1rem;
        overflow: hidden;
    }
    .prob-fill-green {
        height: 100%;
        background: linear-gradient(90deg, #34d399, #10b981);
        border-radius: 4px;
        transition: width 0.8s ease-out;
    }
    .prob-fill-red {
        height: 100%;
        background: linear-gradient(90deg, #f87171, #ef4444);
        border-radius: 4px;
        transition: width 0.8s ease-out;
    }
    .prob-pct {
        font-weight: 800;
        font-size: 0.95rem;
        color: #111827;
        min-width: 50px;
        text-align: right;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #f0f0f0 !important;
    }

    /* Status indicator */
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
        color: #059669;
        border: 1px solid #a7f3d0;
    }
    .status-down {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }
    .dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-green { background: #10b981; box-shadow: 0 0 6px rgba(16,185,129,0.5); }
    .dot-red { background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,0.5); }

    /* Sidebar text */
    .sidebar-info {
        color: #6b7280;
        font-size: 0.82rem;
        line-height: 1.7;
        margin-top: 0.8rem;
    }
    .sidebar-info b { color: #374151; }

    /* ===== STATS ROW ===== */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .stat-box {
        flex: 1;
        background: #fff;
        border: 1px solid #f0f0f0;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        transition: all 0.25s ease;
    }
    .stat-box:hover {
        border-color: #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #111827;
    }
    .stat-label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9ca3af;
        margin-top: 4px;
    }

    /* ===== FOOTER ===== */
    .app-footer {
        text-align: center;
        padding: 2.5rem 0 1rem;
        color: #d1d5db;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
    }

    /* Divider */
    hr { border-color: #f0f0f0 !important; }

    /* Expander */
    .streamlit-expanderHeader {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ───────────────────────── HERO ─────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🧬 AI-Powered Assessment</div>
    <h1 class="hero-title">Student Depression<br><span>Risk Predictor</span></h1>
    <p class="hero-desc">
        Predict depression risk by analyzing student lifestyle data.
        Powered by machine learning trained on 100K records.
    </p>
</div>
""", unsafe_allow_html=True)

# ───────────────────────── SIDEBAR ─────────────────────────
with st.sidebar:
    st.markdown("### ⚡ System Status")
    api_online = False
    try:
        health_resp = requests.get(f"{API_URL}/health", timeout=10)
        if health_resp.status_code == 200:
            health = health_resp.json()
            api_online = True
            st.markdown(
                '<span class="status-badge status-up">'
                '<span class="dot dot-green"></span>API Online</span>',
                unsafe_allow_html=True,
            )
            st.markdown(f"""
            <div class="sidebar-info">
                Model: <b>{'✅ Loaded' if health['model_loaded'] else '❌ Not loaded'}</b><br>
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
        <b>9 features</b> are analyzed including age, sleep,
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
        '<div class="info-card">'
        '<div class="card-header">'
        '<span class="card-emoji">👤</span>'
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
        '<div class="info-card">'
        '<div class="card-header">'
        '<span class="card-emoji">📚</span>'
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
        '<div class="info-card">'
        '<div class="card-header">'
        '<span class="card-emoji">🏃</span>'
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

            # ── Result Card ──
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

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Probability Bars ──
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

            # ── Stats Row ──
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
            st.error("⚠️ Model not loaded. Please try again shortly.")
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
