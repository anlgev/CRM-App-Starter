import os
from pathlib import Path
from dotenv import load_dotenv

# Streamlit app root: frontend/streamlit_app/
APP_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = APP_ROOT / ".env"

# Load .env if exists
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
