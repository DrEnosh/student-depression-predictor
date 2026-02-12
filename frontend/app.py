"""
Streamlit frontend for the Student Depression Prediction system.
Provides an interactive UI that calls the FastAPI /predict endpoint.

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
    page_title="Student Depression Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    .prediction-positive {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
    }
    .prediction-negative {
        background: linear-gradient(135deg, #26de81, #20bf6b);
        color: white;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="main-header">🧠 Student Depression Risk Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Enter student lifestyle data to predict depression risk using our ML model</div>',
    unsafe_allow_html=True,
)

# --- Sidebar: API Status ---
with st.sidebar:
    st.header("⚙️ System Status")
    try:
        health_resp = requests.get(f"{API_URL}/health", timeout=5)
        if health_resp.status_code == 200:
            health = health_resp.json()
            st.success(f"API: {health['status'].upper()}")
            st.info(f"Model Loaded: {'✅' if health['model_loaded'] else '❌'}")
            st.info(f"Version: {health['version']}")
        else:
            st.error("API returned non-200 status")
    except requests.ConnectionError:
        st.error("❌ API Offline — Start the FastAPI server first")
    except Exception as e:
        st.error(f"Error: {e}")

    st.divider()
    st.header("ℹ️ About")
    st.markdown("""
    This app predicts the risk of depression in students
    based on their lifestyle factors. The model was trained
    on 100,000 student records using a Random Forest classifier.

    **Features used:**
    - Age, Gender, Department
    - CGPA, Sleep, Study Hours
    - Social Media, Physical Activity
    - Stress Level
    """)

# --- Input Form ---
st.header("📋 Student Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Demographics")
    age = st.slider("Age", min_value=15, max_value=30, value=20, step=1)
    gender = st.selectbox("Gender", options=["Male", "Female"])
    department = st.selectbox(
        "Department",
        options=["Science", "Engineering", "Medical", "Arts", "Business"],
    )

with col2:
    st.subheader("📚 Academics")
    cgpa = st.slider("CGPA", min_value=0.0, max_value=4.0, value=3.0, step=0.01)
    study_hours = st.slider("Study Hours (daily)", min_value=0.0, max_value=15.0, value=4.0, step=0.1)
    sleep_duration = st.slider("Sleep Duration (hours)", min_value=0.0, max_value=15.0, value=7.0, step=0.1)

with col3:
    st.subheader("🏃 Lifestyle")
    social_media_hours = st.slider("Social Media Hours (daily)", min_value=0.0, max_value=15.0, value=3.0, step=0.1)
    physical_activity = st.slider("Physical Activity Score", min_value=0, max_value=200, value=80, step=1)
    stress_level = st.slider("Stress Level", min_value=0, max_value=10, value=5, step=1)

st.divider()

# --- Predict Button ---
if st.button("🔮 Predict Depression Risk", use_container_width=True):
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
        with st.spinner("Analyzing student data..."):
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()

            st.header("🎯 Prediction Result")

            # Prediction display
            if result["prediction"] == 1:
                st.markdown(
                    f"""<div class="prediction-box prediction-positive">
                        <h2>⚠️ {result['label']}</h2>
                        <p style="font-size: 1.2rem;">
                            Confidence: {result['probability_depression']:.1%}
                        </p>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""<div class="prediction-box prediction-negative">
                        <h2>✅ {result['label']}</h2>
                        <p style="font-size: 1.2rem;">
                            Confidence: {result['probability_no_depression']:.1%}
                        </p>
                    </div>""",
                    unsafe_allow_html=True,
                )

            # Detailed metrics
            st.subheader("📊 Detailed Probabilities")
            mc1, mc2, mc3 = st.columns(3)

            with mc1:
                st.metric(
                    label="No Depression Probability",
                    value=f"{result['probability_no_depression']:.2%}",
                )
            with mc2:
                st.metric(
                    label="Depression Probability",
                    value=f"{result['probability_depression']:.2%}",
                )
            with mc3:
                st.metric(
                    label="Model Version",
                    value=result['model_version'],
                )

            # Input summary
            with st.expander("📝 Input Summary"):
                st.json(payload)

        elif response.status_code == 503:
            st.error("⚠️ Model not loaded. Please train the model first.")
        else:
            st.error(f"API Error: {response.status_code} — {response.text}")

    except requests.ConnectionError:
        st.error("❌ Cannot connect to the API. Make sure FastAPI is running on " + API_URL)
    except Exception as e:
        st.error(f"Error: {e}")

# --- Footer ---
st.divider()
st.markdown(
    "<p style='text-align: center; color: #6c757d;'>"
    "Student Depression Prediction System | Built with FastAPI + Streamlit + scikit-learn"
    "</p>",
    unsafe_allow_html=True,
)
