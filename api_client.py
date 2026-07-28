"""
Async HTTP client for the EnergyEta upstream API.
Used by both FastAPI routes (proxy) and the data_fetcher (data science pipeline).
"""

from __future__ import annotations

import httpx
from config import BASE_URL, ENERGYETA_TOKEN


def _build_headers() -> dict[str, str]:
    """Return default headers with Bearer token."""
    headers = {"Content-Type": "application/json"}
    if ENERGYETA_TOKEN:
        headers["Authorization"] = f"Bearer {ENERGYETA_TOKEN}"
    return headers


# ---------------------------------------------------------------------------
# Async client (used by FastAPI routes)
# ---------------------------------------------------------------------------

_async_client: httpx.AsyncClient | None = None


async def get_async_client() -> httpx.AsyncClient:
    """Return a shared async client; create one if needed."""
    global _async_client
    if _async_client is None or _async_client.is_closed:
        _async_client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers=_build_headers(),
            timeout=30.0,
        )
    return _async_client


async def close_async_client() -> None:
    """Shut down the shared async client."""
    global _async_client
    if _async_client and not _async_client.is_closed:
        await _async_client.aclose()
        _async_client = None


async def async_get(path: str, params: dict | None = None) -> dict:
    """
    Perform an async GET to the upstream API and return the JSON response.
    Raises httpx.HTTPStatusError on non-2xx responses.
    """
    client = await get_async_client()
    response = await client.get(path, params=params)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Sync client (used by data_fetcher.py / scripts)
# ---------------------------------------------------------------------------

def sync_get(path: str, params: dict | None = None) -> dict:
    """
    Perform a synchronous GET to the upstream API and return JSON.
    Convenient for Jupyter notebooks, scripts, and data pipelines.
    """
    url = f"{BASE_URL}{path}"
    response = httpx.get(url, headers=_build_headers(), params=params, timeout=30.0)
    response.raise_for_status()
    return response.json()
