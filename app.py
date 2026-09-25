import streamlit as st
import pickle

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="StentGuard AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. DEEP AURORA & WATER RIPPLE CSS (EXACT MATCH WITH REPORT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* 1. STRONG AURORA ANIMATION ON ROOT CONTAINERS */
    .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #e3eeff 0%, #e0c3fc 25%, #8ec5fc 50%, #e0c3fc 75%, #c2e9fb 100%) !important;
        background-size: 400% 400% !important;
        animation: auroraBG 12s ease infinite !important;
        font-family: 'Outfit', sans-serif !important;
        color: #1e293b !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    @keyframes auroraBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    #MainMenu, footer {visibility: hidden;}
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 4rem !important;
        max-width: 950px !important;
    }

    /* 2. FLOATING GLASS HEADER */
    .header-container {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 24px !important;
        text-align: center;
        margin-bottom: 3.5rem;
        padding: 2.5rem 2rem;
        box-shadow: 0 10px 40px 0 rgba(142, 197, 252, 0.3) !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .header-icon {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .main-title {
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        letter-spacing: -0.04em !important;
        line-height: 1.1 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .sub-title {
        color: #475569 !important; 
        font-size: 1.2rem !important;
        font-weight: 500 !important;
    }

    /* 3. FROSTED GLASS INPUT BOXES */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > div, 
    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.7) !important; 
        backdrop-filter: blur(15px) !important;
        border: 2px solid rgba(255, 255, 255, 0.9) !important; 
        border-radius: 16px !important;
        box-shadow: inset 0 2px 4px 0 rgba(255, 255, 255, 0.9), 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    input, div[data-baseweb="select"] div {
        color: #0f172a !important; 
        -webkit-text-fill-color: #0f172a !important; 
        font-weight: 600 !important;
    }
    
    /* 4. THE WATER RIPPLE PULSE EFFECT */
    @keyframes waterRipple {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.6), inset 0 2px 4px 0 rgba(255, 255, 255, 0.9); }
        70% { box-shadow: 0 0 0 15px rgba(102, 126, 234, 0), inset 0 2px 4px 0 rgba(255, 255, 255, 0.9); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0), inset 0 2px 4px 0 rgba(255, 255, 255, 0.9); }
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="base-input"] > div:focus-within, 
    div[data-baseweb="select"] > div:focus-within {
        border-color: #667eea !important; 
        background: #ffffff !important;
        animation: waterRipple 1.2s infinite ease-out !important;
        transform: translateY(-2px);
    }

    button[title="Step up"], button[title="Step down"], 
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        background-color: transparent !important; 
        color: #475569 !important;
        border-left: 1px solid rgba(0, 0, 0, 0.1) !important;
    }
    
    /* DROPDOWN POP-UP MENU */
    div[role="listbox"], ul[data-baseweb="menu"] {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 2px solid #8ec5fc !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 40px -10px rgba(102, 126, 234, 0.3) !important;
    }
    li[role="option"] {
        color: #0f172a !important;
        font-weight: 500;
        padding: 12px 15px !important;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background: linear-gradient(135deg, #e3eeff 0%, #c2e9fb 100%) !important;
        color: #0f172a !important;
        border-radius: 8px;
        font-weight: 700 !important;
    }
    
    /* Floating Labels */
    label {
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        font-weight: 800 !important;
        color: #334155 !important; 
        margin-bottom: 0.6rem !important;
        margin-left: 0.2rem !important;
    }

    /* 5. GRADIENT SUBMIT BUTTON WITH RIPPLE */
    div.stButton > button {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
        margin-top: 2.5rem !important;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 20px 35px -5px rgba(15, 23, 42, 0.5) !important;
    }
    div.stButton > button:active {
        animation: waterRipple 0.5s ease-out !important;
    }
    
    /* Result Alerts */
    .alert-safe {
        background: rgba(255, 255, 255, 0.85); 
        backdrop-filter: blur(20px);
        border: 2px solid #34d399; 
        border-left: 8px solid #10b981;
        color: #064e3b; 
        padding: 1.5rem;
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.1rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
    .alert-danger {
        background: rgba(255, 255, 255, 0.85); 
        backdrop-filter: blur(20px);
        border: 2px solid #fb7185;
        border-left: 8px solid #e11d48; 
        color: #881337; 
        padding: 1.5rem;
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.1rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(225, 29, 72, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. FLOATING HEADER ---
st.markdown("""
<div class="header-container">
    <div class="header-icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
        </svg>
    </div>
    <div class="main-title">StentGuard AI</div>
    <div class="sub-title">Advanced Predictive Intelligence for Cardiology</div>
</div>
""", unsafe_allow_html=True)

# --- 4. SECURE MODEL LOADING ---
@st.cache_resource
def load_model():
    with open('stent_predictive_model.pkl', 'rb') as file:
        return pickle.load(file)
model = load_model()

# --- 5. CLEAN GRID LAYOUT (2 COLUMNS) ---
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

# --- 6. EXECUTE BUTTON ---
submit_button = st.button("RUN PREDICTIVE ANALYSIS", use_container_width=True)

# --- 7. PROCESSING LOGIC ---
if submit_button:
    # Feature Mapping
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
    
    # Prediction
    prediction = model.predict(features)
    
    # Output Rendering with Animated Glass Alerts
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    if prediction[0] == 1:
        st.markdown("""
        <div class='alert-danger'>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            <strong>Critical Alert:</strong> High-risk predictive parameters detected. Immediate clinical review advised.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='alert-safe'>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            <strong>Optimal:</strong> Patient vitals align with stable cardiac parameters. No immediate risk detected.
        </div>
        """, unsafe_allow_html=True)
