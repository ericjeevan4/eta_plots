"""
FastAPI router — Machine endpoints.
Proxies all 16 GET endpoints from the Machine folder to the upstream EnergyEta API.
"""

from __future__ import annotations

from fastapi import APIRouter, Query
from api_client import async_get

router = APIRouter(prefix="/machine", tags=["Machine"])


# ──────────────────────────────────────────────
# 1. getMachines
# ──────────────────────────────────────────────
@router.get("/getMachines", summary="Get all machines for a client")
async def get_machines(clientId: str = Query(..., description="Client ID")):
    return await async_get("/machine/getMachines", params={"clientId": clientId})


# ──────────────────────────────────────────────
# 2. getMachineData
# ──────────────────────────────────────────────
@router.get("/getMachineData/{machineId}", summary="Get machine data with time range")
async def get_machine_data(
    machineId: str,
    startTime: str = Query(..., description="ISO 8601 start time"),
    endTime: str = Query(..., description="ISO 8601 end time"),
    table: str = Query("MinutePrimary", description="Table: MinutePrimary | HourlyPrimary | DailyPrimary"),
    order: int = Query(-1, description="Sort order: 1 (asc) or -1 (desc)"),
    sortBy: str = Query("timestamp", description="Field to sort by"),
):
    return await async_get(
        f"/machine/getMachineData/{machineId}",
        params={"startTime": startTime, "endTime": endTime, "table": table, "order": order, "sortBy": sortBy},
    )


# ──────────────────────────────────────────────
# 3. getMachineDataWithDisplayName
# ──────────────────────────────────────────────
@router.get("/getMachineDataWithDisplayName/{machineId}", summary="Get machine data with display names")
async def get_machine_data_with_display_name(
    machineId: str,
    startTime: str = Query(None, description="ISO 8601 start time"),
    endTime: str = Query(None, description="ISO 8601 end time"),
    table: str = Query("HourlyPrimary", description="Table: MinutePrimary | HourlyPrimary | DailyPrimary"),
    order: int = Query(-1, description="Sort order"),
    sortBy: str = Query("timestamp", description="Sort field"),
    getLatestData: bool = Query(False, description="If true, return only latest data"),
):
    params: dict = {"table": table}
    if getLatestData:
        params["getLatestData"] = "true"
    else:
        if startTime:
            params["startTime"] = startTime
        if endTime:
            params["endTime"] = endTime
        params["order"] = order
        params["sortBy"] = sortBy
    return await async_get(f"/machine/getMachineDataWithDisplayName/{machineId}", params=params)


# ──────────────────────────────────────────────
# 4. getLatestData
# ──────────────────────────────────────────────
@router.get("/getLatestData/{machineId}/{table}", summary="Get latest data for a machine")
async def get_latest_data(machineId: str, table: str):
    return await async_get(f"/machine/getLatestData/{machineId}/{table}")


# ──────────────────────────────────────────────
# 5. getLatestDataByClientId
# ──────────────────────────────────────────────
@router.get("/getLatestDataByClientId/{clientId}/{table}", summary="Get latest data by client ID")
async def get_latest_data_by_client_id(clientId: str, table: str):
    return await async_get(f"/machine/getLatestDataByClientId/{clientId}/{table}")


# ──────────────────────────────────────────────
# 6. getAllMachineData
# ──────────────────────────────────────────────
@router.get("/getAllMachineData", summary="Get all machine data for a client")
async def get_all_machine_data(
    clientId: str = Query(...),
    table: str = Query("DailyPrimary"),
    startTime: str = Query(...),
    endTime: str = Query(...),
    sortBy: str = Query("timestamp"),
    order: int = Query(1),
):
    return await async_get(
        "/machine/getAllMachineData",
        params={"clientId": clientId, "table": table, "startTime": startTime, "endTime": endTime, "sortBy": sortBy, "order": order},
    )


# ──────────────────────────────────────────────
# 7. getTopEnergyContributedMachines
# ──────────────────────────────────────────────
@router.get("/getTopEnergyContributedMachines/{clientId}", summary="Top energy contributing machines")
async def get_top_energy_contributed_machines(
    clientId: str,
    startTime: str = Query(...),
    endTime: str = Query(...),
):
    return await async_get(
        f"/machine/getTopEnergyContributedMachines/{clientId}",
        params={"startTime": startTime, "endTime": endTime},
    )


# ──────────────────────────────────────────────
# 8. getTopPowerContributedMachines
# ──────────────────────────────────────────────
@router.get("/getTopPowerContributedMachines/{clientId}", summary="Top power contributing machines")
async def get_top_power_contributed_machines(clientId: str):
    return await async_get(f"/machine/getTopPowerContributedMachines/{clientId}")


# ──────────────────────────────────────────────
# 9. getElectricalEnergySumByGroupId
# ──────────────────────────────────────────────
@router.get("/getElectricalEnergySumByGroupId/{clientId}/{table}", summary="Sum of electrical energy by group")
async def get_electrical_energy_sum_by_group_id(
    clientId: str,
    table: str,
    startTime: str = Query(...),
    endTime: str = Query(...),
):
    return await async_get(
        f"/machine/getElectricalEnergySumByGroupId/{clientId}/{table}",
        params={"startTime": startTime, "endTime": endTime},
    )


# ──────────────────────────────────────────────
# 10. getGroupLevelElectricalEnergyTimeline
# ──────────────────────────────────────────────
@router.get("/getGroupLevelElectricalEnergyTimeline/{clientId}/{table}", summary="Group-level energy timeline")
async def get_group_level_electrical_energy_timeline(
    clientId: str,
    table: str,
    startTime: str = Query(...),
    endTime: str = Query(...),
    groupName: str = Query(None, description="Optional group name filter"),
):
    params: dict = {"startTime": startTime, "endTime": endTime}
    if groupName:
        params["groupName"] = groupName
    return await async_get(f"/machine/getGroupLevelElectricalEnergyTimeline/{clientId}/{table}", params=params)


# ──────────────────────────────────────────────
# 11. getMachinesElectricityCost
# ──────────────────────────────────────────────
@router.get("/getMachinesElectricityCost", summary="Get electricity cost for machines")
async def get_machines_electricity_cost(
    clientId: str = Query(...),
    startTime: str = Query(...),
    endTime: str = Query(...),
):
    return await async_get(
        "/machine/getMachinesElectricityCost",
        params={"clientId": clientId, "startTime": startTime, "endTime": endTime},
    )


# ──────────────────────────────────────────────
# 12. peakHourDemandTrends
# ──────────────────────────────────────────────
@router.get("/peakHourDemandTrends", summary="Peak hour demand trends")
async def peak_hour_demand_trends(
    clientId: str = Query(...),
    startTime: str = Query(...),
    endTime: str = Query(...),
):
    return await async_get(
        "/machine/peakHourDemandTrends",
        params={"clientId": clientId, "startTime": startTime, "endTime": endTime},
    )


# ──────────────────────────────────────────────
# 13. getMeanPlot
# ──────────────────────────────────────────────
@router.get("/getMeanPlot/{clientId}/{machineId}", summary="Get mean plot data")
async def get_mean_plot(clientId: str, machineId: str):
    return await async_get(f"/machine/getMeanPlot/{clientId}/{machineId}")


# ──────────────────────────────────────────────
# 14. getMachineGroups
# ──────────────────────────────────────────────
@router.get("/getMachineGroups", summary="Get all machine groups")
async def get_machine_groups():
    return await async_get("/machine/getMachineGroups")


# ──────────────────────────────────────────────
# 15. getMachineTypes
# ──────────────────────────────────────────────
@router.get("/getMachineTypes", summary="Get machine types for a client")
async def get_machine_types(clientId: str = Query(...)):
    return await async_get("/machine/getMachineTypes", params={"clientId": clientId})
