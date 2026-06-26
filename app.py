import streamlit as st
import pickle

# 1. Page Config - Centered for that clean web-app feel
st.set_page_config(page_title="StentGuard AI", layout="centered", initial_sidebar_state="collapsed")

# 2. Ultra-Minimalist CSS (Stripe / Vercel Aesthetic)
st.markdown("""
<style>
    /* Pure Minimalist Canvas */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #111827;
    }
    
    /* Hide Streamlit Clutter Completely */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Clean Typography Header */
    .premium-header {
        padding: 3rem 0 2rem 0;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 3rem;
    }
    .premium-header h1 {
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        color: #111827;
        margin: 0;
        line-height: 1.2;
    }
    .premium-header p {
        color: #6B7280;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Flat, Sleek Inputs */
    .stNumberInput > div > div > input, 
    .stSelectbox > div > div > select {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        color: #111827 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease-in-out;
    }
    /* Sharp Focus State */
    .stNumberInput > div > div > input:focus, 
    .stSelectbox > div > div > select:focus {
        border-color: #111827 !important;
        box-shadow: 0 0 0 1px #111827 !important;
    }
    
    /* Micro-Typography for Labels */
    label {
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600 !important;
        color: #4B5563 !important;
        margin-bottom: 0.25rem !important;
    }

    /* The 'Execute' Button - Pitch Black & Solid */
    div.stButton > button {
        background-color: #111827;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-size: 0.95rem;
        font-weight: 600;
        width: 100%;
        margin-top: 2rem;
        transition: background-color 0.2s ease;
        letter-spacing: 0.02em;
    }
    div.stButton > button:hover {
        background-color: #374151;
        color: #FFFFFF;
    }
    
    /* Minimalist Alert Cards */
    .alert-safe {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        color: #166534;
        padding: 1.25rem;
        border-radius: 6px;
        font-weight: 500;
        text-align: center;
    }
    .alert-danger {
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        color: #991B1B;
        padding: 1.25rem;
        border-radius: 6px;
        font-weight: 500;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 3. Clinical & Sharp Header
st.markdown("""
<div class="premium-header">
    <h1>StentGuard</h1>
    <p>Clinical Intelligence & Cardiac Risk Analytics.</p>
</div>
""", unsafe_allow_html=True)

# 4. Secure Model Loading
@st.cache_resource
def load_model():
    with open('stent_predictive_model.pkl', 'rb') as file:
        return pickle.load(file)
model = load_model()

# 5. Clean Grid Layout (2 Columns for elegance)
col1, padding, col2 = st.columns([1, 0.1, 1])

with col1:
    age = st.number_input("Patient Age", 20, 100, 50)
    sex = st.selectbox("Biological Sex", ["Male", "Female"])
    chest_pain = st.selectbox("Chest Pain Category", ["Atypical Angina", "Non-Anginal", "Asymptomatic", "Typical Angina"])
    resting_bp = st.number_input("Resting BP (mmHg)", 50, 200, 120)
    cholesterol = st.number_input("Serum Cholesterol", 100, 600, 200)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120", ["Negative", "Positive"])

with col2:
    resting_ecg = st.selectbox("Resting ECG Result", ["Normal", "ST-T Abnormality", "LV Hypertrophy"])
    max_hr = st.number_input("Maximum Heart Rate", 60, 220, 140)
    exercise_angina = st.selectbox("Exercise Induced Angina", ["Negative", "Positive"])
    oldpeak = st.number_input("ST Depression (Oldpeak)", -3.0, 7.0, 0.0, 0.1)
    st_slope = st.selectbox("ST Segment Slope", ["Upsloping", "Flat", "Downsloping"])
    
    # Run Button inside the right column for a tighter layout
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    submit_button = st.button("RUN ANALYSIS")

# 6. Silent Processing
if submit_button:
    # Logic Mapping
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
        st.markdown("<div class='alert-danger'><b>Attention Required:</b> Predictive models indicate an elevated probability of cardiac complications.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-safe'><b>Status Normal:</b> Patient vitals currently align with stable cardiac parameters.</div>", unsafe_allow_html=True)
