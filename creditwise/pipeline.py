"""ML pipeline for CreditWise, rebuilt from CreditWiseLoanApprovalSystem.ipynb.

Mirrors the notebook's preprocessing so the website behaves like the original project:
  - numeric nulls  -> mean (SimpleImputer)
  - category nulls -> most frequent (SimpleImputer)
  - Education_Level -> label-encoded (Graduate=0, Not Graduate=1), like LabelEncoder
  - other categoricals -> OneHotEncoder(drop="first", handle_unknown="ignore")
  - StandardScaler
  - models: LogisticRegression and KNeighborsClassifier(n_neighbors=5)

Unlike the notebook, every step is fitted on the training split only (no leakage),
and rows with a missing target are dropped instead of being filled with "No".
"""
from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

TARGET = "Loan_Approved"

NUMERIC = [
    "Applicant_Income", "Coapplicant_Income", "Age", "Dependents", "Credit_Score",
    "Existing_Loans", "DTI_Ratio", "Savings", "Collateral_Value", "Loan_Amount", "Loan_Term",
]
LABEL_ENCODED = ["Education_Level"]
ONE_HOT = ["Employment_Status", "Marital_Status", "Loan_Purpose", "Property_Area", "Gender", "Employer_Category"]
FEATURES = NUMERIC + LABEL_ENCODED + ONE_HOT

# Allowed values (from loan_approval_data.csv) - used by the website's dropdowns.
CHOICES = {
    "Employment_Status": ["Salaried", "Self-employed", "Contract", "Unemployed"],
    "Marital_Status": ["Married", "Single"],
    "Loan_Purpose": ["Home", "Car", "Education", "Personal", "Business"],
    "Property_Area": ["Urban", "Semiurban", "Rural"],
    "Education_Level": ["Graduate", "Not Graduate"],
    "Gender": ["Male", "Female"],
    "Employer_Category": ["Private", "Government", "MNC", "Business", "Unemployed"],
}

MODELS = {
    "Logistic Regression": lambda: LogisticRegression(max_iter=1000),
    "KNN (k=5)": lambda: KNeighborsClassifier(n_neighbors=5),
}

# Supabase uses snake_case lower-case column names.
DB_COLUMNS = {c: c.lower() for c in ["Applicant_ID", *FEATURES, TARGET]}


def build_pipeline(model_name: str) -> Pipeline:
    pre = ColumnTransformer([
        ("num", SimpleImputer(strategy="mean"), NUMERIC),
        ("edu", Pipeline([
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("enc", OrdinalEncoder(categories=[CHOICES["Education_Level"]],
                                   handle_unknown="use_encoded_value", unknown_value=-1)),
        ]), LABEL_ENCODED),
        ("ohe", Pipeline([
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("enc", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")),
        ]), ONE_HOT),
    ])
    return Pipeline([("pre", pre), ("scale", StandardScaler()), ("model", MODELS[model_name]())])


def prepare(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Accepts the CSV layout or the Supabase (lower-case) layout."""
    reverse = {v: k for k, v in DB_COLUMNS.items()}
    df = df.rename(columns=reverse)
    df = df[df[TARGET].notna()].copy()
    y = df[TARGET].map({"Yes": 1, "No": 0, True: 1, False: 0, 1: 1, 0: 0}).astype(int)
    return df[FEATURES], y
