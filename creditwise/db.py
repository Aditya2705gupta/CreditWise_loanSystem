"""Supabase helpers. Credentials come from Streamlit secrets or environment variables, never from code."""
from __future__ import annotations

import os

import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # dotenv is optional on Streamlit Cloud
    pass


def _setting(name: str) -> str | None:
    try:
        import streamlit as st
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.getenv(name)


def get_client(admin: bool = False):
    """admin=True uses the service-role key (local scripts only); the website uses the anon key."""
    from supabase import create_client
    url = _setting("SUPABASE_URL")
    # New Supabase key names (secret / publishable) with fallback to the legacy ones.
    names = ("SUPABASE_SECRET_KEY", "SUPABASE_SERVICE_ROLE_KEY") if admin else ("SUPABASE_PUBLISHABLE_KEY", "SUPABASE_ANON_KEY")
    key = next((v for v in map(_setting, names) if v), None)
    if not url or not key:
        return None
    return create_client(url, key)


def fetch_training_data(client) -> pd.DataFrame:
    rows, start, page = [], 0, 1000
    while True:
        batch = client.table("loan_applications").select("*").range(start, start + page - 1).execute().data
        rows += batch
        if len(batch) < page:
            break
        start += page
    return pd.DataFrame(rows)
