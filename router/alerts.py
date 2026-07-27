"""
FastAPI router — Alert endpoints.
Proxies all 4 GET endpoints from the Alerts folder to the upstream EnergyEta API.
"""

from __future__ import annotations

from fastapi import APIRouter
from api_client import async_get

router = APIRouter(prefix="/alert", tags=["Alerts"])


# ──────────────────────────────────────────────
# 1. getAlertById
# ──────────────────────────────────────────────
@router.get("/getAlertById/{alertId}/client/{clientId}", summary="Get alert by ID for a client")
async def get_alert_by_id(alertId: str, clientId: str):
    return await async_get(f"/alert/getAlertById/{alertId}/client/{clientId}")


# ──────────────────────────────────────────────
# 2. getAllAlertTypes
# ──────────────────────────────────────────────
@router.get("/getAllAlertTypes", summary="Get all alert types")
async def get_all_alert_types():
    return await async_get("/alert/getAllAlertTypes")


# ──────────────────────────────────────────────
# 3. getAllLabels
# ──────────────────────────────────────────────
@router.get("/getAllLabels", summary="Get all alert labels")
async def get_all_labels():
    return await async_get("/alert/getAllLabels")


# ──────────────────────────────────────────────
# 4. dataNotComing
# ──────────────────────────────────────────────
@router.get("/dataNotComing", summary="Get machines where data is not coming")
async def data_not_coming():
    return await async_get("/alert/dataNotComing")
