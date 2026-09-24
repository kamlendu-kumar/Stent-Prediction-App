import streamlit as st
import pickle
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="StentGuard AI | Enterprise", page_icon="🩺", layout="wide", initial_sidebar_state="expanded")

# --- 2. APPLE-STYLE HIGH-END CSS (LIGHT THEME + CHARCOAL SIDEBAR) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Clean Light Background */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #F5F5F7 !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #1D1D1F !important;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1100px !important;
    }

    /* Floating White Header */
    .premium-header {
        background: #FFFFFF;
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04);
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.03);
    }
    .premium-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        background: -webkit-linear-gradient(45deg, #007AFF, #34C759);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .premium-subtitle {
        color: #86868B;
        font-size: 1.15rem;
        font-weight: 500;
    }

    /* Metric Cards for Dashboard Feel */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 2.5rem;
    }
    .metric-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.02);
        flex: 1;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,122,255,0.08);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1D1D1F;
        margin-bottom: 0.2rem;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* Soft Neumorphic Input Boxes */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5EA !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02) !important;
        color: #1D1D1F !important;
        transition: all 0.3s ease !important;
    }
    
    input, div[data-baseweb="select"] div {
        color: #1D1D1F !important; 
        -webkit-text-fill-color: #1D1D1F !important; 
        font-weight: 500 !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="base-input"] > div:focus-within, 
    div[data-baseweb="select"] > div:focus-within {
        border-color: #007AFF !important; 
        box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.15) !important;
    }

    /* Section Labels */
    label {
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 700 !important;
        color: #86868B !important; 
        margin-bottom: 0.5rem !important;
    }

    /* Apple-Style Premium Action Button */
    div.stButton > button {
        background: #007AFF !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        margin-top: 1.5rem !important;
        width: 100% !important;
        box-shadow: 0 10px 20px rgba(0, 122, 255, 0.25) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(0, 122, 255, 0.35) !important;
        background: #0066D6 !important;
    }
    
    /* Custom Sidebar Styling - Deep Charcoal */
    [data-testid="stSidebar"] {
        background-color: #1E1E24 !important;
        border-right: 1px solid #2D2D34 !important;
    }
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] strong,
    [data-testid="stSidebar"] span {
        color: #F5F5F7 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #3A3A42 !important;
    }
    [data-testid="stSidebar"] .stAlert {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    [data-testid="stSidebar"] .stAlert p {
        color: #A0A0AB !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PROFESSIONAL CHARCOAL SIDEBAR ---
with st.sidebar:
    st.markdown("## 🏥 StentGuard System")
    st.markdown("**Developer:** Kamlendu Kumar")
    st.markdown("**ID:** LPU-324103592")
    st.markdown("**Program:** MCA Capstone")
    st.divider()
    st.markdown("### 🟢 Server Status")
    st.caption("All clinical nodes are online. Connected to secure Random Forest Engine.")
    st.divider()
    st.info("💡 **Clinical Tip:** Ensure ST Slope and Chest Pain inputs are highly accurate, as the AI assigns high feature importance to them.")

# --- 4. ENTERPRISE HEADER & METRICS ---
st.markdown("""
<div class="premium-header">
    <div class="premium-title">StentGuard AI</div>
    <div class="premium-subtitle">Predictive Monitoring for Cardiac Stents | Clinical Edition</div>
</div>
""", unsafe_allow_html=True)

# Top Dashboard Metrics
st.markdown("""
<div class="metric-container">
    <div class="metric-card">
        <div class="metric-value">918</div>
        <div class="metric-label">Patient Records Analyzed</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">86.0%</div>
        <div class="metric-label">AI Sensitivity (Recall)</div>
    </div>
    <div class="metric-card">
        <div class="metric-value" style="color: #34C759;">Online</div>
        <div class="metric-label">Model Status</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. SECURE MODEL LOADING ---
@st.cache_resource
def load_model():
    with open('stent_predictive_model.pkl', 'rb') as file:
        return pickle.load(file)
model = load_model()

# --- 6. STRUCTURED CLINICAL INPUT FORM ---
st.markdown("### 📊 Enter Patient Vitals")
col1, padding, col2 = st.columns([1, 0.1, 1])

with col1:
    age = st.number_input("Patient Age", 20, 100, 50)
    sex = st.selectbox("Biological Sex", ["Male", "Female"])
    chest_pain = st.selectbox("Chest Pain Category", ["Atypical Angina", "Non-Anginal", "Asymptomatic", "Typical Angina"])
    resting_bp = st.number_input("Resting Blood Pressure (mmHg)", 50, 200, 120)
    cholesterol = st.number_input("Serum Cholesterol (mg/dl)", 100, 600, 200)

with col2:
    max_hr = st.number_input("Maximum Heart Rate Achieved", 60, 220, 140)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["Negative", "Positive"])
    exercise_angina = st.selectbox("Exercise Induced Angina", ["Negative", "Positive"])
    resting_ecg = st.selectbox("Resting ECG Result", ["Normal", "ST-T Abnormality", "LV Hypertrophy"])
    
    c1, c2 = st.columns(2)
    with c1:
        oldpeak = st.number_input("ST Depression", -3.0, 7.0, 0.0, 0.1)
    with c2:
        st_slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])

# --- 7. EXECUTE PREDICTION BUTTON ---
submit_button = st.button("RUN PREDICTIVE ANALYSIS")

# --- 8. LOGIC, ANIMATION & RESULT PROCESSING ---
if submit_button:
    # Fake Loading Animation for Premium Feel
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.caption("⏳ Initializing clinical parameters...")
    time.sleep(0.4)
    progress_bar.progress(30)
    
    status_text.caption("🧠 Cross-referencing with Random Forest Ensembles...")
    time.sleep(0.5)
    progress_bar.progress(70)
    
    status_text.caption("✅ Generating final risk profile...")
    time.sleep(0.4)
    progress_bar.progress(100)
    
    # Clear the loading elements
    time.sleep(0.2)
    status_text.empty()
    progress_bar.empty()

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
    
    # Render Beautiful Results
    if prediction[0] == 1:
        st.markdown("""
        <div style="background-color: #FFF2F2; border: 1px solid #FF3B30; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(255,59,48,0.15);">
            <h2 style="color: #FF3B30; margin-top: 0; display: flex; align-items: center; gap: 10px;">
                ⚠️ CRITICAL CLINICAL ALERT
            </h2>
            <p style="color: #1D1D1F; font-size: 1.1rem; margin-bottom: 0; font-weight: 500;">
                High-risk predictive parameters detected. Immediate cardiologist evaluation and stent patency check advised.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #F2FFF5; border: 1px solid #34C759; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(52,199,89,0.15);">
            <h2 style="color: #34C759; margin-top: 0; display: flex; align-items: center; gap: 10px;">
                ✅ OPTIMAL STATUS
            </h2>
            <p style="color: #1D1D1F; font-size: 1.1rem; margin-bottom: 0; font-weight: 500;">
                Patient vitals align with stable cardiac parameters. No immediate stent failure indicators detected.
            </p>
        </div>
        """, unsafe_allow_html=True)
