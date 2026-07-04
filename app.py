import streamlit as st
import pickle

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="StentGuard AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. ADVANCED CSS (SMART LUXURY LIGHT THEME) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Premium Background */
    .stApp {
        background-color: #FDFCF8 !important; /* Warm Ivory / Cream */
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #2D2A26 !important; /* Deep Charcoal instead of harsh black */
    }
    
    #MainMenu, header, footer {visibility: hidden;}
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 4rem !important;
        max-width: 950px !important;
    }

    /* Header Styling with SVG Icon */
    .header-container {
        text-align: center;
        margin-bottom: 3.5rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid #EBE4D8; 
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .header-icon {
        margin-bottom: 1rem;
    }

    .main-title {
        color: #1A1A1A;
        font-weight: 800;
        font-size: 3.2rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #8C857B; 
        font-size: 1.15rem;
        font-weight: 500;
        letter-spacing: -0.01em;
    }

    /* PREMIUM INPUT BOXES */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important; 
        border: 1px solid #EBE4D8 !important; 
        border-radius: 12px !important; /* Apple style rounded corners */
        box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.2s ease;
    }
    
    /* Text inside inputs */
    input, div[data-baseweb="select"] div {
        color: #2D2A26 !important; 
        -webkit-text-fill-color: #2D2A26 !important; 
        font-weight: 500 !important;
    }
    
    /* Focus effects (Soft Gold/Warm Halo) */
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="base-input"] > div:focus-within, 
    div[data-baseweb="select"] > div:focus-within {
        border-color: #C8BCA7 !important; 
        box-shadow: 0 0 0 3px rgba(200, 188, 167, 0.2) !important;
    }

    /* +/- BUTTONS FIX for Number Inputs */
    button[title="Step up"], button[title="Step down"], 
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        background-color: #F7F5F0 !important; 
        color: #2D2A26 !important;
        border-left: 1px solid #EBE4D8 !important;
    }
    
    /* DROPDOWN POP-UP MENU */
    div[role="listbox"], ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EBE4D8 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1) !important;
    }
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #2D2A26 !important;
        font-weight: 500;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #FDFCF8 !important;
        color: #B59A6D !important; /* Subtle Gold highlight */
    }
    
    /* Labels */
    label {
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 700 !important;
        color: #8C857B !important; 
        margin-bottom: 0.4rem !important;
    }

    /* LUXURY FULL-WIDTH SUBMIT BUTTON */
    div.stButton > button {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.85rem 2rem !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        margin-top: 2.5rem !important;
        box-shadow: 0 8px 20px -6px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #333333 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Beautiful Result Alerts */
    .alert-safe {
        background-color: #F0FDF4; 
        border: 1px solid #BBF7D0; 
        border-left: 6px solid #22C55E;
        color: #166534; 
        padding: 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.05);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
    .alert-danger {
        background-color: #FEF2F2; 
        border: 1px solid #FECACA;
        border-left: 6px solid #EF4444; 
        color: #991B1B; 
        padding: 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.05);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER UI WITH SVG ICON ---
st.markdown("""
<div class="header-container">
    <div class="header-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#B59A6D" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.42 4.58a5.4 5.4 0 0 0-7.65 0l-.77.78-.77-.78a5.4 5.4 0 0 0-7.65 0C1.46 6.7 1.33 10.28 4 13l8 8 8-8c2.67-2.72 2.54-6.3.42-8.42z"></path>
            <path d="M3.5 12h5l1.5-3 3 7 1.5-4h4.5"></path>
        </svg>
    </div>
    <div class="main-title">StentGuard AI</div>
    <div class="sub-title">Predictive Intelligence for Cardiac Risk Management.</div>
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
    
    # Output Rendering with SVGs inline
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if prediction[0] == 1:
        st.markdown("""
        <div class='alert-danger'>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            Alert: Critical predictive parameters detected. Immediate clinical review advised.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='alert-safe'>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            Optimal: Patient vitals align with stable cardiac parameters. No immediate risk detected.
        </div>
        """, unsafe_allow_html=True)
