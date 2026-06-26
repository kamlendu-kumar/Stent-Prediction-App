import streamlit as st
import pickle

# 1. Page Config - Clean and Minimal
st.set_page_config(page_title="StentGuard AI", layout="wide", initial_sidebar_state="collapsed")

# 2. Premium CSS Injection (Apple/Minimalist Aesthetic)
st.markdown("""
<style>
    /* Global Minimalist Theme */
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Hide Streamlit Clutter */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Premium Header Card */
    .header-card {
        background: linear-gradient(145deg, #1f2833, #151b22);
        border-left: 5px solid #66fcf1;
        border-radius: 12px;
        padding: 2.5rem;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .header-icon {
        font-size: 3rem;
        color: #45a29e;
    }
    .header-title-container h1 {
        color: #ffffff;
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: -0.5px;
        margin: 0;
        padding: 0;
    }
    .header-title-container p {
        color: #66fcf1;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 5px;
        opacity: 0.9;
    }

    /* Input Field Styling - Clean & Rounded */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: #1f2833 !important;
        border: 1px solid #2a3644 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        transition: all 0.2s ease;
    }
    div[data-baseweb="input"] > div:hover, 
    div[data-baseweb="select"] > div:hover {
        border-color: #45a29e !important;
    }
    
    /* Label Styling */
    label {
        color: #c5c6c7 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px !important;
    }

    /* The 'Apple' Button */
    div.stButton > button {
        background-color: #66fcf1;
        color: #0b0c10;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 700;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        width: 100%;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(102, 252, 241, 0.2);
    }
    div.stButton > button:hover {
        background-color: #45a29e;
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(102, 252, 241, 0.4);
    }
    
    /* Prediction Result Cards */
    .result-card-safe {
        background: rgba(46, 204, 113, 0.1);
        border-left: 4px solid #2ecc71;
        padding: 1.5rem;
        border-radius: 8px;
        color: #2ecc71;
        font-weight: 600;
    }
    .result-card-danger {
        background: rgba(231, 76, 60, 0.1);
        border-left: 4px solid #e74c3c;
        padding: 1.5rem;
        border-radius: 8px;
        color: #e74c3c;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. Premium Header (No Emoji, SVG-like Icon)
st.markdown("""
<div class="header-card">
    <div class="header-icon">⚕️</div>
    <div class="header-title-container">
        <h1>StentGuard AI</h1>
        <p>Predictive Intelligence for Cardiac Risk Management</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Model Loading
@st.cache_resource
def load_model():
    with open('stent_predictive_model.pkl', 'rb') as file:
        return pickle.load(file)
model = load_model()

# 5. Structured & User-Friendly Input Layout
st.markdown("<h3 style='color: #ffffff; margin-bottom: 1.5rem; font-weight: 600;'>Patient Clinical Data</h3>", unsafe_allow_html=True)

# Grouping inputs logically
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age (Years)", 20, 100, 50)
    sex = st.selectbox("Biological Sex", ["Male", "Female"])
    chest_pain = st.selectbox("Chest Pain Category", ["ATA (Atypical Angina)", "NAP (Non-Anginal)", "ASY (Asymptomatic)", "TA (Typical Angina)"])
    resting_bp = st.number_input("Resting Blood Pressure (mmHg)", 50, 200, 120)

with col2:
    cholesterol = st.number_input("Serum Cholesterol (mg/dl)", 100, 600, 200)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["No", "Yes"])
    resting_ecg = st.selectbox("Resting ECG Results", ["Normal", "ST-T wave abnormality", "Left Ventricular Hypertrophy (LVH)"])
    max_hr = st.number_input("Maximum Heart Rate Achieved", 60, 220, 140)

with col3:
    exercise_angina = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
    oldpeak = st.number_input("Oldpeak (ST Depression)", -3.0, 7.0, 0.0, 0.1)
    st_slope = st.selectbox("Slope of Peak Exercise ST Segment", ["Upsloping", "Flat", "Downsloping"])
    
    # Placeholder for alignment
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

# 6. Logic Processing
if st.button("EXECUTE ANALYSIS"):
    with st.spinner('Processing parameters through neural network...'):
        # Data conversion mapping
        sex_m = 1 if sex == "Male" else 0
        cpt_ata = 1 if "ATA" in chest_pain else 0
        cpt_nap = 1 if "NAP" in chest_pain else 0
        cpt_ta = 1 if "TA" in chest_pain else 0
        ecg_normal = 1 if resting_ecg == "Normal" else 0
        ecg_st = 1 if "ST-T" in resting_ecg else 0
        angina_y = 1 if exercise_angina == "Yes" else 0
        slope_flat = 1 if st_slope == "Flat" else 0
        slope_up = 1 if st_slope == "Upsloping" else 0
        bs_val = 1 if fasting_bs == "Yes" else 0
        
        features = [[age, resting_bp, cholesterol, bs_val, max_hr, oldpeak, 
                     sex_m, cpt_ata, cpt_nap, cpt_ta, ecg_normal, ecg_st, angina_y, slope_flat, slope_up]]
        
        prediction = model.predict(features)
        
        st.markdown("---")
        if prediction[0] == 1:
            st.markdown("<div class='result-card-danger'>⚠️ HIGH RISK DETECTED: Parameters indicate significant likelihood of cardiac event or stent complication. Recommend immediate clinical intervention.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-card-safe'>✅ OPTIMAL PROFILE: Patient parameters are currently stable. No immediate predictive risk detected.</div>", unsafe_allow_html=True)
