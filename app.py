import streamlit as st
import pickle

st.set_page_config(page_title="StentGuard AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background-color: #09090b !important;
        font-family: 'Inter', sans-serif !important;
        color: #fafafa !important;
    }
    
    #MainMenu, header, footer {visibility: hidden;}
    
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 4rem !important;
        max-width: 900px !important;
    }

    .header-container {
        text-align: center;
        margin-bottom: 4rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid #27272a; 
    }
    .main-title {
        color: #fafafa;
        font-weight: 800;
        font-size: 3.5rem;
        letter-spacing: -0.04em;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        color: #a1a1aa; 
        font-size: 1.15rem;
        font-weight: 400;
        letter-spacing: -0.01em;
    }

    /* ALL Inputs Uniform Dark Zinc */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: #18181b !important; 
        border: 1px solid #27272a !important; 
        border-radius: 8px !important;
    }
    
    /* FIX: Make the +/- Stepper Buttons Dark to match */
    div[data-baseweb="input"] button {
        background-color: #27272a !important; /* Dark slate for buttons */
        color: #e2e8f0 !important;
    }
    div[data-baseweb="input"] button:hover {
        background-color: #3f3f46 !important; /* Slightly lighter on hover */
    }
    
    /* Premium Platinum/Silver Text Color */
    input {
        color: #e2e8f0 !important; 
        background-color: transparent !important;
        -webkit-text-fill-color: #e2e8f0 !important; 
    }
    div[data-baseweb="select"] span {
        color: #e2e8f0 !important; 
    }
    
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="base-input"] > div:focus-within, 
    div[data-baseweb="select"] > div:focus-within {
        border-color: #52525b !important; 
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
    }
    
    label {
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-weight: 600 !important;
        color: #71717a !important; 
        margin-bottom: 0.3rem !important;
    }

    div.stButton > button {
        background-color: #fafafa;
        color: #09090b;
        border: 1px solid #fafafa;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 2rem;
        box-shadow: 0 4px 6px -1px rgba(255, 255, 255, 0.1);
    }
    div.stButton > button:hover {
        background-color: #e4e4e7;
        transform: translateY(-1px);
    }
    
    .alert-safe {
        background-color: rgba(22, 101, 52, 0.2); 
        border: 1px solid #14532d; 
        color: #4ade80; 
        padding: 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        text-align: center;
    }
    .alert-danger {
        background-color: rgba(153, 27, 27, 0.2); 
        border: 1px solid #7f1d1d; 
        color: #f87171; 
        padding: 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="main-title">StentGuard AI</div>
    <div class="sub-title">Predictive Intelligence for Cardiac Risk Management.</div>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with open('stent_predictive_model.pkl', 'rb') as file:
        return pickle.load(file)
model = load_model()

col1, padding, col2 = st.columns([1, 0.1, 1])

with col1:
    age = st.number_input("Patient Age", 20, 100, 50)
    sex = st.selectbox("Biological Sex", ["Male", "Female"])
    chest_pain = st.selectbox("Chest Pain Category", ["Atypical Angina", "Non-Anginal", "Asymptomatic", "Typical Angina"])
    resting_bp = st.number_input("Resting BP (mmHg)", 50, 200, 120)
    cholesterol = st.number_input("Serum Cholesterol", 100, 600, 200)

with col2:
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120", ["Negative", "Positive"])
    resting_ecg = st.selectbox("Resting ECG Result", ["Normal", "ST-T Abnormality", "LV Hypertrophy"])
    max_hr = st.number_input("Maximum Heart Rate", 60, 220, 140)
    exercise_angina = st.selectbox("Exercise Induced Angina", ["Negative", "Positive"])
    
    col2a, col2b = st.columns(2)
    with col2a:
        oldpeak = st.number_input("ST Depression", -3.0, 7.0, 0.0, 0.1)
    with col2b:
        st_slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])

# FIX: Added use_container_width=True to make the button full width
submit_button = st.button("RUN PREDICTIVE ANALYSIS", use_container_width=True)

if submit_button:
    sex_m = 1 if sex == "Male" else 0
    cpt_ata = 1 if chest_pain == "Atypical Angina" else 0
    cpt_nap = 1 if chest_pain == "Non-Anginal" else 0
    cpt_ta = 1 if chest_pain == "Typical Angina" else 0
    ecg_normal = 1 if resting_ecg == "Normal" else 0
    ecg_st = 1 if resting_ecg == "ST-T Abnormality" else 0
    angina_y = 1 if exercise_angina == "Positive" else 0
    slope_flat = 1 if st_slope == "Flat" else 0
    slope_up = 1 if st_slope == "Upsloping" else 0
    bs_val = 1 if fasting_bs == "Positive" else 0
    
    features = [[age, resting_bp, cholesterol, bs_val, max_hr, oldpeak, 
                 sex_m, cpt_ata, cpt_nap, cpt_ta, ecg_normal, ecg_st, angina_y, slope_flat, slope_up]]
    
    prediction = model.predict(features)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if prediction[0] == 1:
        st.markdown("<div class='alert-danger'>Alert: Critical predictive parameters detected. Immediate clinical review advised.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-safe'>Optimal: Patient vitals align with stable cardiac parameters. No immediate risk detected.</div>", unsafe_allow_html=True)
