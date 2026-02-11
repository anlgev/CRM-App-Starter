import requests
from core.config import API_BASE_URL

def health():
    r = requests.get(f"{API_BASE_URL}/health", timeout=10)
    r.raise_for_status()
    return r.json()
