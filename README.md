# CreditWise Loan System

A machine-learning loan approval checker. Applicants enter their details on a Streamlit website and get an instant **Approved / Rejected** prediction with an approval probability. The data and every prediction are stored in **Supabase**.

The original analysis is in [`CreditWiseLoanApprovalSystem.ipynb`](CreditWiseLoanApprovalSystem.ipynb) and the brief is in [`CreditWise Loan System PS.pdf`](CreditWise%20Loan%20System%20PS.pdf).

## How it works

```
loan_approval_data.csv ──seed──▶ Supabase: loan_applications
                                        │
                              train.py  ▼
        impute → encode → scale → Logistic Regression / KNN
                                        │  best model by F1
                                        ▼
                          models/creditwise_model.joblib ──▶ app.py (Streamlit)
                                                                 │
                                       Supabase: predictions ◀───┘
                                       Supabase: model_runs  ◀── train.py metrics
```

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| **Logistic Regression** (selected) | 88.9% | 85.5% | 78.3% | 0.817 |
| KNN (k = 5) | 74.2% | 61.2% | 50.0% | 0.550 |

These are test-set results on a stratified 80/20 split of the 950 labelled rows. The pipeline repeats the notebook's preprocessing:
- mean / most-frequent imputation
- label encoding for Education
- one-hot encoding with `drop="first"` for the other categorical columns
- standard scaling

It also fixes two notebook issues:
- Every step is now fitted on the training split only, so no test data leaks into training.
- Rows with a missing target are dropped instead of being filled with "No".

## Project layout

| Path | Purpose |
|---|---|
| `app.py` | Streamlit website |
| `creditwise/pipeline.py` | Feature lists and the scikit-learn pipeline |
| `creditwise/db.py` | Supabase client |
| `train.py` | Trains both models, saves the best one and logs metrics to `model_runs` |
| `seed_supabase.py` | Uploads the CSV into `loan_applications` (run once) |
| `supabase/schema.sql` | Tables plus Row Level Security policies |

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # add your Supabase URL and keys
python seed_supabase.py           # one-time upload of the dataset
python train.py                   # retrain from Supabase data
streamlit run app.py
```

## Security

- The website uses only the Supabase **publishable** (anon) key.
- Row Level Security lets that key **insert** predictions but not read any table.
- The secret (service-role) key is used only by the local scripts and is kept in `.env`, which git ignores.

*Student project for learning purposes. It is not financial advice or a real credit decision.*
