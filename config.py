import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Add it to your .env file or Streamlit secrets."
    )