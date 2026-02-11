import requests
from typing import Any, Dict, Optional

from core.config import API_BASE_URL

TIMEOUT = 15


def _url(path: str) -> str:
    return f"{API_BASE_URL}{path}"


def health() -> Dict[str, Any]:
    r = requests.get(_url("/health"), timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


# ----------------------------
# Leads
# ----------------------------
def list_leads(active_only: Optional[bool] = None) -> list[dict]:
    params = {}
    if active_only is True:
        params["active_only"] = "true"
    elif active_only is False:
        params["active_only"] = "false"

    r = requests.get(_url("/leads/"), params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def create_lead(payload: dict) -> dict:
    r = requests.post(_url("/leads/"), json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def update_lead(lead_id: int, payload: dict) -> dict:
    r = requests.patch(_url(f"/leads/{lead_id}"), json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()
