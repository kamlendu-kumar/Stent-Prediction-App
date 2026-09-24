import streamlit as st
import pickle

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="StentGuard AI | Enterprise Clinical Suite", layout="wide", initial_sidebar_state="collapsed")

# --- 2. APPLE-GRADE DEEP OBSIDIAN & FROSTED GLASS CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* True Dark Obsidian Background */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #09090b !important;
        background-image: radial-gradient(circle at 50% 0%, #181824 0%, #09090b 70%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #f1f5f9 !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    #MainMenu, footer {visibility: hidden;}
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 1050px !important;
    }

    /* Floating Apple-Level Glass Header */
    .header-container {
        background: rgba(24, 24, 32, 0.7) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        text-align: center;
        margin-bottom: 2.5rem;
        padding: 2.2rem 2rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5) !important;
    }
    
    .header-icon {
        color: #38bdf8;
        margin-bottom: 0.8rem;
    }

    .main-title {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 0.3rem !important;
    }
    
    .sub-title {
        color: #94a3b8 !important; 
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.01em;
    }

    /* Dark Mode Frosted Glass Input Panels */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > div, 
    div[data-baseweb="select"] > div {
        background: rgba(30, 30, 42, 0.6) !important; 
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        border-radius: 12px !important;
        color: #f8fafc !important;
        transition: all 0.25s ease !important;
    }
    
    input, div[data-baseweb="select"] div {
        color: #f8fafc !important; 
        -webkit-text-fill-color: #f8fafc !important; 
        font-weight: 500 !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="base-input"] > div:focus-within, 
    div[data-baseweb="select"] > div:focus-within {
        border-color: #38bdf8 !important; 
        background: rgba(30, 30, 42, 0.9) !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }

    /* Dropdown Pop-up Menu Styling */
    div[role="listbox"], ul[data-baseweb="menu"] {
        background: #181824 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important;
    }
    
    li[role="option"] {
        color: #cbd5e1 !important;
        font-weight: 400;
        padding: 10px 14px !important;
    }
    
    li[role="option"]:hover, li[aria-selected="true"] {
        background: #2563eb !important;
        color: #ffffff !important;
        border-radius: 6px;
    }
    
    /* Section Labels */
    label {
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-weight: 700 !important;
        color: #94a3b8 !important; 
        margin-bottom: 0.4rem !important;
    }

    /* Premium Action Button */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        margin-top: 2rem !important;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4) !important;
        transition: all 0.25s ease !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.6) !important;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    }
    
    /* Professional Clinical Alerts */
    .alert-safe, .alert-danger {
        padding: 1.4rem;
        border-radius: 14px;
        font-weight: 600;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 14px;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    
    .alert-safe {
        background: rgba(6, 78, 59, 0.4);
        border: 1px solid #059669;
        border-left: 6px solid #10b981;
        color: #a7f3d0;
    }
    
    .alert-danger {
        background: rgba(136, 19, 55, 0.4);
        border: 1px solid #be123c;
        border-left: 6px solid #f43f5e;
        color: #fecdd3;
    }
    
    /* Expander Styling for Clean Look */
    .streamlit-expanderHeader {
        background: rgba(24, 24, 32, 0.5) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ENTERPRISE HEADER ---
st.markdown("""
<div class="header-container">
    <div class="header-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
        </svg>
    </div>
    <div class="main-title">StentGuard AI</div>
    <div class="sub-title">Clinical Decision Support Suite • Active Stent Monitoring</div>
</div>
""", unsafe_allow_html=True)

# --- 4. SECURE MODEL LOADING ---
@st.cache_resource
def load_model():
    with open('stent_predictive_model.pkl', 'rb') as file:
        return pickle.load(file)
model = load_model()

# --- 5. STRUCTURED CLINICAL INPUT FORM ---
col1, padding, col2 = st.columns([1, 0.15, 1])

with col1:
    st.markdown("### 👤 Primary Vitals")
    age = st.number_input("Patient Age", 20, 100, 50)
    sex = st.selectbox("Biological Sex", ["Male", "Female"])
    chest_pain = st.selectbox("Chest Pain Category", ["Atypical Angina", "Non-Anginal", "Asymptomatic", "Typical Angina"])
    resting_bp = st.number_input("Resting Blood Pressure (mmHg)", 50, 200, 120)
    cholesterol = st.number_input("Serum Cholesterol (mg/dl)", 100, 600, 200)

with col2:
    st.markdown("### ⚡ Hemodynamic Markers")
    max_hr = st.number_input("Maximum Heart Rate Achieved", 60, 220, 140)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["Negative", "Positive"])
    exercise_angina = st.selectbox("Exercise Induced Angina", ["Negative", "Positive"])
    
    # Advanced Vitals inside a clean collapsible block
    with st.expander("🔬 Advanced ECG & Clinical Parameters"):
        resting_ecg = st.selectbox("Resting ECG Result", ["Normal", "ST-T Abnormality", "LV Hypertrophy"])
        col_a, col_b = st.columns(2)
        with col_a:
            oldpeak = st.number_input("ST Depression", -3.0, 7.0, 0.0, 0.1)
        with col_b:
            st_slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])

# --- 6. EXECUTE PREDICTION BUTTON ---
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
submit_button = st.button("RUN PREDICTIVE ANALYSIS", use_container_width=True)

# --- 7. LOGIC & RESULT PROCESSING ---
if submit_button:
    # Feature Mapping for Model
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
        st.markdown("""
        <div class='alert-danger'>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            <div><strong>CRITICAL CLINICAL ALERT:</strong> High-risk predictive parameters detected. Immediate cardiologist evaluation and stent patency check advised.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='alert-safe'>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            <div><strong>OPTIMAL STATUS:</strong> Patient vitals align with stable cardiac parameters. No immediate stent failure indicators detected.</div>
        </div>
        """, unsafe_allow_html=True)
