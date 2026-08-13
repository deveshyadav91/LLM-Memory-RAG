import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        import streamlit as st
        API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        API_KEY = None

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Add it to .env locally or Streamlit Secrets when deployed."
    )
