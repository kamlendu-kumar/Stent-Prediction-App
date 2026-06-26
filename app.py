import streamlit as st
import pickle

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="StentGuard AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. ADVANCED CSS (TAILWIND/ZINC DARK THEME + BUG FIXES) ---
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

    /* INPUT BOXES & TEXT COLOR FIX */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: #18181b !important; 
        border: 1px solid #27272a !important; 
        border-radius: 8px !important;
    }
    
    /* Force Platinum text everywhere */
    input, div[data-baseweb="select"] div {
        color: #e2e8f0 !important; 
        -webkit-text-fill-color: #e2e8f0 !important; 
    }
    
    /* Focus effects */
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="base-input"] > div:focus-within, 
    div[data-baseweb="select"] > div:focus-within {
        border-color: #52525b !important; 
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
    }

    /* THE STUBBORN +/- BUTTONS FIX */
    button[title="Step up"], button[title="Step down"], 
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        background-color: #27272a !important; 
        color: #fafafa !important;
    }
    button[title="Step up"]:hover, button[title="Step down"]:hover,
    [data-testid="stNumberInputStepUp"]:hover, [data-testid="stNumberInputStepDown"]:hover {
        background-color: #3f3f46 !important;
    }
    
    /* DROPDOWN POP-UP MENU FIX (The White Box Bug) */
    div[role="listbox"], ul[data-baseweb="menu"] {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
    }
    li[role="option"] {
        background-color: #18181b !important;
        color: #e2e8f0 !important;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #27272a !important;
        color: #ffffff !important;
    }
    
    /* Labels */
    label {
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-weight: 600 !important;
        color: #71717a !important; 
        margin-bottom: 0.3rem !important;
    }

    /* Full-Width Submit Button */
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
    
    /* Result Alerts */
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

# --- 3. HEADER UI ---
st.markdown("""
<div class="header-container">
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
    
    # Output Rendering
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if prediction[0] == 1:
        st.markdown("<div class='alert-danger'>Alert: Critical predictive parameters detected. Immediate clinical review advised.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-safe'>Optimal: Patient vitals align with stable cardiac parameters. No immediate risk detected.</div>", unsafe_allow_html=True)
