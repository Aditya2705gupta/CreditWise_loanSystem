"""CreditWise - loan approval checker (Streamlit)."""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from postgrest.types import ReturnMethod

from creditwise.db import get_client
from creditwise.pipeline import CHOICES, DB_COLUMNS

st.set_page_config(page_title="CreditWise Loan Checker", page_icon="🏦", layout="centered")


@st.cache_resource
def load_model():
    return joblib.load(Path(__file__).parent / "models" / "creditwise_model.joblib")


@st.cache_resource
def supabase():
    try:
        return get_client(admin=False)
    except Exception:
        return None


bundle = load_model()
pipe = bundle["pipeline"]

st.title("🏦 CreditWise Loan Checker")
st.write("Enter your details to see whether your loan is likely to be **approved**, "
         "based on a machine-learning model trained on past loan applications.")

with st.form("applicant"):
    st.subheader("About you")
    c1, c2 = st.columns(2)
    age = c1.number_input("Age", 18, 75, 30)
    gender = c2.selectbox("Gender", CHOICES["Gender"])
    marital = c1.selectbox("Marital status", CHOICES["Marital_Status"])
    dependents = c2.number_input("Dependents", 0, 10, 0)
    education = c1.selectbox("Education", CHOICES["Education_Level"])
    area = c2.selectbox("Property area", CHOICES["Property_Area"])

    st.subheader("Work and income")
    c1, c2 = st.columns(2)
    employment = c1.selectbox("Employment status", CHOICES["Employment_Status"])
    employer = c2.selectbox("Employer category", CHOICES["Employer_Category"])
    income = c1.number_input("Your monthly income (₹)", 0, 10_000_000, 12000, step=1000)
    co_income = c2.number_input("Co-applicant monthly income (₹)", 0, 10_000_000, 0, step=1000)

    st.subheader("Credit profile")
    c1, c2 = st.columns(2)
    credit_score = c1.slider("Credit score", 300, 900, 700)
    existing_loans = c2.number_input("Existing loans running", 0, 20, 0)
    dti = c1.slider("Debt-to-income ratio", 0.0, 1.0, 0.30, 0.01,
                    help="Total monthly EMIs ÷ monthly income. 0.30 means 30% of income goes to EMIs.")
    savings = c2.number_input("Savings (₹)", 0, 100_000_000, 10000, step=1000)

    st.subheader("Loan you want")
    c1, c2 = st.columns(2)
    purpose = c1.selectbox("Purpose", CHOICES["Loan_Purpose"])
    amount = c2.number_input("Loan amount (₹)", 1000, 100_000_000, 20000, step=1000)
    term = c1.selectbox("Term (months)", [12, 24, 36, 48, 60, 72, 84], index=3)
    collateral = c2.number_input("Collateral value (₹)", 0, 100_000_000, 25000, step=1000)

    consent = st.checkbox("Save my (anonymous) inputs to help improve the model", value=True)
    submitted = st.form_submit_button("Check my loan", type="primary", use_container_width=True)

if submitted:
    applicant = {
        "Applicant_Income": income, "Coapplicant_Income": co_income, "Employment_Status": employment,
        "Age": age, "Marital_Status": marital, "Dependents": dependents, "Credit_Score": credit_score,
        "Existing_Loans": existing_loans, "DTI_Ratio": dti, "Savings": savings,
        "Collateral_Value": collateral, "Loan_Amount": amount, "Loan_Term": term,
        "Loan_Purpose": purpose, "Property_Area": area, "Education_Level": education,
        "Gender": gender, "Employer_Category": employer,
    }
    X = pd.DataFrame([applicant])[bundle["features"]]
    prob = float(pipe.predict_proba(X)[0, 1])
    approved = prob >= 0.5

    st.divider()
    if approved:
        st.success(f"### ✅ Likely to be APPROVED\nApproval probability: **{prob:.0%}**")
    else:
        st.error(f"### ❌ Likely to be REJECTED\nApproval probability: **{prob:.0%}**")
    st.progress(prob)

    tips = []
    if dti > 0.4:
        tips.append("Your debt-to-income ratio is high; paying down EMIs helps most.")
    if credit_score < 650:
        tips.append("A credit score above 650 improves your chances.")
    if existing_loans >= 3:
        tips.append("Closing some running loans before applying may help.")
    if tips:
        st.markdown("**What could improve your chances:**\n" + "\n".join(f"- {t}" for t in tips))

    if consent:
        client = supabase()
        if client:
            row = {DB_COLUMNS[k]: v for k, v in applicant.items()}
            row.update(predicted_approved=bool(approved), approval_probability=round(prob, 4),
                       model_name=bundle["model_name"], model_version=bundle["version"])
            try:
                client.table("predictions").insert(row, returning=ReturnMethod.minimal).execute()  # anon may insert, not read back
            except Exception:
                st.caption("Note: your result could not be saved this time.")

with st.expander("About the model"):
    m = bundle["metrics"][bundle["model_name"]]
    st.write(f"Model: **{bundle['model_name']}** (version {bundle['version']}), selected by F1 score "
             f"over KNN and Logistic Regression.")
    st.write(f"Test-set accuracy {m['accuracy']:.1%} · precision {m['precision']:.1%} · "
             f"recall {m['recall']:.1%} · F1 {m['f1']:.1%}")
    st.caption("Trained on the CreditWise dataset (1,000 historical applications). "
               "Its incomes range from about ₹2,000 to ₹20,000 a month, so results outside that range are less reliable. "
               "This is a student project for learning purposes, not financial advice or a real credit decision.")
