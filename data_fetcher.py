"""
Data Fetcher — pulls data from EnergyEta API directly into Pandas DataFrames.
Uses the synchronous API client (no FastAPI needed).

Usage:
    from data_fetcher import EnergyEtaDataFetcher
    fetcher = EnergyEtaDataFetcher()
    df = fetcher.get_machines("65eea4893ca87cc2c6a63429")
"""

from __future__ import annotations

import pandas as pd
from api_client import sync_get
from config import DEFAULT_CLIENT_ID


class EnergyEtaDataFetcher:
    """High-level wrapper that returns Pandas DataFrames for every EnergyEta endpoint."""

    def __init__(self, client_id: str | None = None):
        self.client_id = client_id or DEFAULT_CLIENT_ID

    # ──────────────────────────────────────────
    # Machine endpoints
    # ──────────────────────────────────────────

    def get_machines(self, client_id: str | None = None) -> pd.DataFrame:
        """Fetch all machines for a client → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get("/machine/getMachines", params={"clientId": cid})
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_machine_data(
        self,
        machine_id: str,
        start_time: str,
        end_time: str,
        table: str = "MinutePrimary",
        order: int = -1,
        sort_by: str = "timestamp",
    ) -> pd.DataFrame:
        """Fetch machine data for a time range → DataFrame."""
        data = sync_get(
            f"/machine/getMachineData/{machine_id}",
            params={"startTime": start_time, "endTime": end_time, "table": table, "order": order, "sortBy": sort_by},
        )
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_machine_data_with_display_name(
        self,
        machine_id: str,
        start_time: str | None = None,
        end_time: str | None = None,
        table: str = "HourlyPrimary",
        order: int = -1,
        sort_by: str = "timestamp",
        get_latest: bool = False,
    ) -> pd.DataFrame:
        """Fetch machine data with display names → DataFrame."""
        params: dict = {"table": table}
        if get_latest:
            params["getLatestData"] = "true"
        else:
            if start_time:
                params["startTime"] = start_time
            if end_time:
                params["endTime"] = end_time
            params["order"] = order
            params["sortBy"] = sort_by
        data = sync_get(f"/machine/getMachineDataWithDisplayName/{machine_id}", params=params)
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_latest_data(self, machine_id: str, table: str = "HourlyPrimary") -> pd.DataFrame:
        """Fetch latest data point for a machine → DataFrame."""
        data = sync_get(f"/machine/getLatestData/{machine_id}/{table}")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_latest_data_by_client(self, client_id: str | None = None, table: str = "MinutePrimary") -> pd.DataFrame:
        """Fetch latest data for all machines of a client → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(f"/machine/getLatestDataByClientId/{cid}/{table}")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_all_machine_data(
        self,
        start_time: str,
        end_time: str,
        client_id: str | None = None,
        table: str = "DailyPrimary",
        sort_by: str = "timestamp",
        order: int = 1,
    ) -> pd.DataFrame:
        """Fetch all machine data for a client in a time range → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(
            "/machine/getAllMachineData",
            params={"clientId": cid, "table": table, "startTime": start_time, "endTime": end_time, "sortBy": sort_by, "order": order},
        )
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_top_energy_machines(self, start_time: str, end_time: str, client_id: str | None = None) -> pd.DataFrame:
        """Top energy contributing machines → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(
            f"/machine/getTopEnergyContributedMachines/{cid}",
            params={"startTime": start_time, "endTime": end_time},
        )
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_top_power_machines(self, client_id: str | None = None) -> pd.DataFrame:
        """Top power contributing machines → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(f"/machine/getTopPowerContributedMachines/{cid}")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_energy_sum_by_group(
        self, start_time: str, end_time: str, client_id: str | None = None, table: str = "DailyPrimary"
    ) -> pd.DataFrame:
        """Sum of electrical energy by group → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(
            f"/machine/getElectricalEnergySumByGroupId/{cid}/{table}",
            params={"startTime": start_time, "endTime": end_time},
        )
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_group_energy_timeline(
        self,
        start_time: str,
        end_time: str,
        client_id: str | None = None,
        table: str = "DailyPrimary",
        group_name: str | None = None,
    ) -> pd.DataFrame:
        """Group-level electrical energy timeline → DataFrame."""
        cid = client_id or self.client_id
        params: dict = {"startTime": start_time, "endTime": end_time}
        if group_name:
            params["groupName"] = group_name
        data = sync_get(f"/machine/getGroupLevelElectricalEnergyTimeline/{cid}/{table}", params=params)
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_electricity_cost(self, start_time: str, end_time: str, client_id: str | None = None) -> pd.DataFrame:
        """Electricity cost for machines → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(
            "/machine/getMachinesElectricityCost",
            params={"clientId": cid, "startTime": start_time, "endTime": end_time},
        )
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_peak_hour_demand_trends(self, start_time: str, end_time: str, client_id: str | None = None) -> pd.DataFrame:
        """Peak hour demand trends → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(
            "/machine/peakHourDemandTrends",
            params={"clientId": cid, "startTime": start_time, "endTime": end_time},
        )
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_mean_plot(self, machine_id: str, client_id: str | None = None) -> pd.DataFrame:
        """Mean plot data → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(f"/machine/getMeanPlot/{cid}/{machine_id}")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_machine_groups(self) -> pd.DataFrame:
        """All machine groups → DataFrame."""
        data = sync_get("/machine/getMachineGroups")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_machine_types(self, client_id: str | None = None) -> pd.DataFrame:
        """Machine types for a client → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get("/machine/getMachineTypes", params={"clientId": cid})
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    # ──────────────────────────────────────────
    # Alert endpoints
    # ──────────────────────────────────────────

    def get_alert_by_id(self, alert_id: str, client_id: str | None = None) -> pd.DataFrame:
        """Get a specific alert → DataFrame."""
        cid = client_id or self.client_id
        data = sync_get(f"/alert/getAlertById/{alert_id}/client/{cid}")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_all_alert_types(self) -> pd.DataFrame:
        """All alert types → DataFrame."""
        data = sync_get("/alert/getAllAlertTypes")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_all_labels(self) -> pd.DataFrame:
        """All alert labels → DataFrame."""
        data = sync_get("/alert/getAllLabels")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    def get_data_not_coming(self) -> pd.DataFrame:
        """Machines where data is not coming → DataFrame."""
        data = sync_get("/alert/dataNotComing")
        records = data.get("data", data) if isinstance(data, dict) else data
        return pd.json_normalize(records) if isinstance(records, list) else pd.DataFrame([records])

    # ──────────────────────────────────────────
    # Convenience — fetch all key datasets
    # ──────────────────────────────────────────

    def fetch_all_datasets(self, start_time: str, end_time: str) -> dict[str, pd.DataFrame]:
        """
        Pull the most commonly needed datasets in one call.
        Returns a dict of DataFrames keyed by dataset name.
        """
        datasets: dict[str, pd.DataFrame] = {}

        print("📡 Fetching machines...")
        datasets["machines"] = self.get_machines()

        print("📡 Fetching all machine data (DailyPrimary)...")
        datasets["all_machine_data"] = self.get_all_machine_data(start_time, end_time)

        print("📡 Fetching top energy machines...")
        datasets["top_energy_machines"] = self.get_top_energy_machines(start_time, end_time)

        print("📡 Fetching top power machines...")
        datasets["top_power_machines"] = self.get_top_power_machines()

        print("📡 Fetching electricity cost...")
        datasets["electricity_cost"] = self.get_electricity_cost(start_time, end_time)

        print("📡 Fetching peak hour demand trends...")
        datasets["peak_demand_trends"] = self.get_peak_hour_demand_trends(start_time, end_time)

        print("📡 Fetching machine groups...")
        datasets["machine_groups"] = self.get_machine_groups()

        print("📡 Fetching machine types...")
        datasets["machine_types"] = self.get_machine_types()

        print("📡 Fetching all alert types...")
        datasets["alert_types"] = self.get_all_alert_types()

        print("📡 Fetching alert labels...")
        datasets["alert_labels"] = self.get_all_labels()

        print("📡 Fetching data-not-coming alerts...")
        datasets["data_not_coming"] = self.get_data_not_coming()

        print(f"\n✅ Fetched {len(datasets)} datasets successfully!")
        return datasets
