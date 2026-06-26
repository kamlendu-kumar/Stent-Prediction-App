import streamlit as st
import pickle

# 1. Page Config
st.set_page_config(page_title="StentGuard AI", layout="wide", initial_sidebar_state="collapsed")

# 2. Dual-Tone & Pattern CSS (The 'Awwwards' Level Design)
st.markdown("""
<style>
    /* Dark Patterned Background (Tech/Matrix Vibe) */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(#334155 1.5px, transparent 1.5px);
        background-size: 30px 30px;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Hide Default Clutter */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* The Floating Premium White Card */
    .block-container {
        background-color: #ffffff;
        border-radius: 24px;
        padding: 3rem 4rem !important;
        margin-top: 4rem !important;
        margin-bottom: 4rem !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
        max-width: 950px !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Header Styling inside the Card */
    .main-header {
        color: #0f172a;
        font-weight: 900;
        font-size: 2.8rem;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2.5rem;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 1.5rem;
    }

    /* Input Fields - Soft & Accessible */
    .stNumberInput > div > div > input, 
    .stSelectbox > div > div > select {
        background-color: #f8fafc !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-weight: 500;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    .stNumberInput > div > div > input:focus, 
    .stSelectbox > div > div > select:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
    }
    
    /* Micro-Typography for Labels */
    label {
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 700 !important;
        color: #475569 !important;
        margin-bottom: 6px !important;
    }

    /* Vibrant Gradient Action Button */
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 0;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        width: 100%;
        margin-top: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 25px -5px rgba(79, 70, 229, 0.4);
    }
    
    /* Custom Results Cards */
    .safe-card {
        background: linear-gradient(to right, #f0fdf4, #dcfce7);
        border-left: 5px solid #22c55e;
        padding: 1.5rem;
        border-radius: 12px;
        color: #166534;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .danger-card {
        background: linear-gradient(to right, #fef2f2, #fee2e2);
        border-left: 5px solid #ef4444;
        padding: 1.5rem;
        border-radius: 12px;
        color: #991b1b;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# 3. Clean Header inside the Card
st.markdown("""
<div class="main-header">StentGuard AI</div>
<div class="sub-header">Advanced Predictive Analytics & Cardiac Monitoring</div>
""", unsafe_allow_html=True)

# 4. Model Loading
@st.cache_resource
def load_model():
    with open('stent_predictive_model.pkl', 'rb') as file:
        return pickle.load(file)
model = load_model()

# 5. Form Layout - 2 Columns
col1, padding, col2 = st.columns([1, 0.05, 1])

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

# 6. Execute Button & Spacing
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
submit_button = st.button("RUN PREDICTIVE ANALYSIS")

# 7. Processing Logic
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
        st.markdown("<div class='danger-card'>🚨 <b>CRITICAL ALERT:</b> Predictive parameters indicate a high probability of cardiac risk. Immediate clinical review advised.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='safe-card'>✅ <b>OPTIMAL PROFILE:</b> Patient vitals align with stable cardiac parameters. No immediate risk detected.</div>", unsafe_allow_html=True)
