import streamlit as st
import pickle
import pandas as pd

# 1. Page Config (Wide Layout)
st.set_page_config(page_title="StentGuard AI", page_icon="🫀", layout="wide", initial_sidebar_state="collapsed")

# 2. Heavy Custom CSS & HTML Injection
st.markdown("""
<style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #ffffff;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Header Container */
    .header-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 2rem;
    }
    .header-title {
        background: -webkit-linear-gradient(45deg, #00d4ff, #00ff87);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 0;
    }
    .header-subtitle {
        color: #a0aec0;
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* Input Styling */
    .stNumberInput > div > div > input, 
    .stSelectbox > div > div > select {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #00d4ff !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* Custom Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00d4ff 0%, #0072ff 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2rem;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px -10px rgba(0, 212, 255, 0.7);
        width: 100%;
        margin-top: 1.5rem;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 25px -10px rgba(0, 212, 255, 0.9);
        color: white;
    }
    
    /* Labels */
    label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Render Custom Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🫀 StentGuard AI</h1>
    <p class="header-subtitle">Advanced Cardiac Risk & Stent Monitoring Engine</p>
</div>
""", unsafe_allow_html=True)

# 4. Load Model securely
@st.cache_resource
def load_model():
    with open('stent_predictive_model.pkl', 'rb') as file:
        return pickle.load(file)
model = load_model()

# 5. Clean Layout for Inputs
st.markdown("### 📊 Patient Vitals Profile")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Patient Age", 20, 100, 50)
    resting_bp = st.number_input("Resting BP (mmHg)", 50, 200, 120)
    max_hr = st.number_input("Max Heart Rate", 60, 220, 140)
    sex = st.selectbox("Biological Sex", ["Male", "Female"])

with col2:
    cholesterol = st.number_input("Cholesterol Level", 100, 600, 200)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120", ["No (0)", "Yes (1)"])
    chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "ASY", "TA"])
    st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

with col3:
    oldpeak = st.number_input("Oldpeak (ST Depression)", -3.0, 7.0, 0.0, 0.1)
    resting_ecg = st.selectbox("Resting ECG Result", ["Normal", "ST", "LVH"])
    exercise_angina = st.selectbox("Exercise Induced Angina", ["No (N)", "Yes (Y)"])

# 6. Logic Processing
if st.button("RUN PREDICTIVE ANALYSIS"):
    with st.spinner('Analyzing complex cardiac parameters...'):
        # Data conversion
        sex_m = 1 if sex == "Male" else 0
        cpt_ata = 1 if chest_pain == "ATA" else 0
        cpt_nap = 1 if chest_pain == "NAP" else 0
        cpt_ta = 1 if chest_pain == "TA" else 0
        ecg_normal = 1 if resting_ecg == "Normal" else 0
        ecg_st = 1 if resting_ecg == "ST" else 0
        angina_y = 1 if exercise_angina == "Yes (Y)" else 0
        slope_flat = 1 if st_slope == "Flat" else 0
        slope_up = 1 if st_slope == "Up" else 0
        bs_val = 1 if fasting_bs == "Yes (1)" else 0
        
        features = [[age, resting_bp, cholesterol, bs_val, max_hr, oldpeak, 
                     sex_m, cpt_ata, cpt_nap, cpt_ta, ecg_normal, ecg_st, angina_y, slope_flat, slope_up]]
        
        prediction = model.predict(features)
        
        st.markdown("---")
        if prediction[0] == 1:
            st.error("🚨 **CRITICAL ALERT:** High probability of cardiac risk or stent complication detected. Immediate clinical review advised.")
        else:
            st.success("✨ **ALL CLEAR:** Patient parameters are optimal. No immediate risk detected.")
