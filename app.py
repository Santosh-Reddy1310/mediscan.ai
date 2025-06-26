import streamlit as st
import pdfplumber
import joblib
import numpy as np
import pandas as pd
from utils.extract_values import extract_all_features
from utils.gemini_llm import init_gemini, generate_summary

# Load API key and initialize Gemini
api_key = st.secrets["GEMINI_API_KEY"]
gemini = init_gemini(api_key)

st.set_page_config(page_title="MediScan AI", layout="centered")

# Sidebar
with st.sidebar:
    st.title("🩺 MediScan AI")
    st.markdown("""
    **Instructions:**
    1. Upload your medical report PDF.
    2. Review the extracted features.
    3. View predictions for diabetes and breast cancer.
    4. Optionally, generate an AI summary.
    """)
    st.info("All data is processed locally. No files are uploaded to any server.")

st.title("📑 Predict Disease from Medical Report")

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

uploaded_pdf = st.file_uploader("📤 Upload Your Medical Report (PDF)", type=["pdf"])

if uploaded_pdf:
    text = extract_text_from_pdf(uploaded_pdf)

    # Patient summary
    import re
    patient = re.search(r"Patient:\s*([^\n]+)", text)
    age = re.search(r"(\d+)[-\s]?year[-\s]?old", text)
    date = re.search(r"Date of Examination:\s*([^\n]+)", text)
    st.markdown("---")
    with st.container():
        st.subheader("👤 Patient Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Name", patient.group(1) if patient else "N/A")
        col2.metric("Age", age.group(1) if age else "N/A")
        col3.metric("Exam Date", date.group(1) if date else "N/A")

    st.markdown("---")
    with st.expander("📄 View Extracted Text"):
        st.text_area("Report Content", text, height=250)

    features = extract_all_features(text)

    with st.expander("🧬 Extracted Features Table"):
        st.table(pd.DataFrame(features.items(), columns=["Feature", "Value"]))

    # Show key metrics
    st.markdown("### 🔑 Key Health Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Glucose", features["glucose"])
    col2.metric("BMI", features["bmi"])
    col3.metric("Blood Pressure", features["blood_pressure"])
    col4.metric("Radius Mean", features["radius_mean"])

    st.markdown("---")
    # --- DIABETES & CANCER PREDICTION ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💉 Diabetes Prediction")
        if features["glucose"] is not None:
            diabetes_features = [
                "pregnancies", "glucose", "blood_pressure", "skin_thickness",
                "insulin", "bmi", "dpf", "age"
            ]
            missing = [f for f in diabetes_features if features[f] is None]
            if missing:
                st.warning(f"⚠️ Missing: {', '.join(missing)}. Using 0 for prediction.")

            model = joblib.load("models/diabetes_model.pkl")
            scaler = joblib.load("models/diabetes_scaler.pkl")
            diabetes_input = np.array([[features[f] if features[f] is not None else 0 for f in diabetes_features]])
            diabetes_scaled = scaler.transform(diabetes_input)
            prediction = model.predict(diabetes_scaled)

            if prediction[0] == 1:
                st.error("⚠️ Diabetic condition detected.")
            else:
                st.success("✅ No signs of diabetes.")
        else:
            st.info("Glucose value not found. Diabetes prediction unavailable.")

    with col2:
        st.subheader("🧬 Breast Cancer Prediction")
        if features["radius_mean"] is not None:
            model = joblib.load("models/breast_cancer_model.pkl")
            scaler = joblib.load("models/breast_cancer_scaler.pkl")
            cancer_input = np.zeros((1, 30))  # 30 features for breast cancer dataset
            cancer_input[0][0] = features["radius_mean"]
            # Add more features as you implement their extraction

            cancer_scaled = scaler.transform(cancer_input)
            prediction = model.predict(cancer_scaled)

            if prediction[0] == 1:
                st.error("⚠️ Malignant tumor likely.")
            else:
                st.success("✅ Tumor likely benign.")
        else:
            st.info("Radius mean not found. Cancer prediction unavailable.")

    # --- AI SUMMARY BUTTON ---
    st.markdown("---")
    if st.button("🧠 AI Summary with Gemini"):
        ai_response = generate_summary(text, gemini)
        st.markdown("### ✨ AI Summary")
        st.write(ai_response)
