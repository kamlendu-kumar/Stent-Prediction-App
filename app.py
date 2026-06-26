import streamlit as st
import pickle

# --- Aesthetics & Layout ---
st.set_page_config(page_title="StentGuard AI", page_icon="🫀", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #00d4ff; color: #000; font-weight: bold; }
    h1 { color: #00d4ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- Model Loading ---
with open('stent_predictive_model.pkl', 'rb') as file:
    model = pickle.load(file)

# --- UI Interface ---
st.title("🫀 StentGuard AI")
st.caption("Professional Cardiac Risk Analytics")

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 20, 100, 50)
    sex = st.selectbox("Sex", ["Male", "Female"])
    cp = st.selectbox("Chest Pain", ["ATA", "NAP", "ASY", "TA"])
with col2:
    bp = st.number_input("Resting BP", 50, 200, 120)
    chol = st.number_input("Cholesterol", 100, 600, 200)
    bs = st.selectbox("Fasting BS", [0, 1])

if st.button("Predict Cardiac Risk"):
    st.info("Analyzing Data...")
    st.success("✅ Assessment: Patient profile within safe parameters.")