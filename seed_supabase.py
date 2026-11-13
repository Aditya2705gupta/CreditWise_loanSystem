"""Upload loan_approval_data.csv into the Supabase table loan_applications (run once)."""
import math

import pandas as pd

from creditwise.db import get_client
from creditwise.pipeline import DB_COLUMNS


def clean(v):
    return None if v is None or (isinstance(v, float) and math.isnan(v)) else v


def main():
    client = get_client(admin=True)
    if client is None:
        raise SystemExit("Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env first")
    existing = client.table("loan_applications").select("id", count="exact").limit(1).execute().count
    if existing:
        raise SystemExit(f"loan_applications already has {existing} rows; not uploading twice")
    df = pd.read_csv("loan_approval_data.csv").rename(columns=DB_COLUMNS)
    df["applicant_id"] = df["applicant_id"].astype("Int64")
    rows = [{k: clean(v) for k, v in r.items()} for r in df.astype(object).to_dict("records")]
    rows = [{k: (int(v) if k == "applicant_id" and v is not None else v) for k, v in r.items()} for r in rows]
    for i in range(0, len(rows), 500):
        client.table("loan_applications").insert(rows[i:i + 500]).execute()
    print(f"Uploaded {len(rows)} rows to loan_applications")


if __name__ == "__main__":
    main()
