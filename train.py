"""Train both notebook models, pick the best by F1, save it, and log the run to Supabase.

Usage:
  python train.py            # read training data from Supabase (falls back to the CSV)
  python train.py --csv      # force the local CSV
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from creditwise.db import fetch_training_data, get_client
from creditwise.pipeline import FEATURES, MODELS, build_pipeline, prepare

ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "models" / "creditwise_model.joblib"


def load_data() -> tuple[pd.DataFrame, str]:
    client = None if "--csv" in sys.argv else get_client(admin=True)
    if client:
        df = fetch_training_data(client)
        if len(df):
            return df, "supabase:loan_applications"
        print("Supabase table is empty, falling back to CSV")
    return pd.read_csv(ROOT / "loan_approval_data.csv"), "csv:loan_approval_data.csv"


def main():
    raw, source = load_data()
    X, y = prepare(raw)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Data: {source} | {len(X)} labelled rows | approval rate {y.mean():.1%}")

    results = {}
    for name in MODELS:
        pipe = build_pipeline(name).fit(X_train, y_train)
        pred = pipe.predict(X_test)
        m = {
            "accuracy": accuracy_score(y_test, pred), "precision": precision_score(y_test, pred),
            "recall": recall_score(y_test, pred), "f1": f1_score(y_test, pred),
            "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        }
        results[name] = (pipe, m)
        print(f"{name:20s} acc={m['accuracy']:.3f} prec={m['precision']:.3f} rec={m['recall']:.3f} f1={m['f1']:.3f}")

    best = max(results, key=lambda n: results[n][1]["f1"])
    version = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    # Refit the winning pipeline on all labelled data before saving.
    final = build_pipeline(best).fit(X, y)
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump({"pipeline": final, "model_name": best, "version": version, "features": FEATURES,
                 "metrics": {n: m for n, (_, m) in results.items()}, "source": source}, MODEL_PATH)
    print(f"Saved best model: {best} (version {version}) -> {MODEL_PATH.relative_to(ROOT)}")

    client = get_client(admin=True)
    if client:
        client.table("model_runs").insert([{
            "version": version, "model_name": n, "is_selected": n == best, "data_source": source,
            "n_rows": int(len(X)), "accuracy": m["accuracy"], "precision": m["precision"],
            "recall": m["recall"], "f1": m["f1"], "confusion_matrix": json.dumps(m["confusion_matrix"]),
        } for n, (_, m) in results.items()]).execute()
        print("Logged run to Supabase table model_runs")


if __name__ == "__main__":
    main()
