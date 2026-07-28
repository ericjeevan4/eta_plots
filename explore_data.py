"""
Explore Data — entry-point script for data science work.

Run:  python explore_data.py

This script:
1. Pulls key datasets from the EnergyEta API into Pandas DataFrames
2. Prints summary info (shape, columns, dtypes)
3. Saves each dataset as a CSV in the data/ folder
"""

from __future__ import annotations

import os
import sys

import pandas as pd

from data_fetcher import EnergyEtaDataFetcher
from config import DEFAULT_CLIENT_ID


def main():
    # ── Time range for data pull ──────────────────────────────────────
    # Adjust these to the range you want to analyse
    START_TIME = "2025-03-01T00:00:00.000Z"
    END_TIME = "2025-03-04T23:59:59.999Z"

    print("=" * 70)
    print("  EnergyEta Data Explorer")
    print(f"  Client ID : {DEFAULT_CLIENT_ID}")
    print(f"  Range     : {START_TIME}  →  {END_TIME}")
    print("=" * 70)

    fetcher = EnergyEtaDataFetcher()

    # Pull all key datasets in one shot
    datasets = fetcher.fetch_all_datasets(start_time=START_TIME, end_time=END_TIME)

    # ── Print summaries ───────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  Dataset Summaries")
    print("=" * 70)

    for name, df in datasets.items():
        print(f"\n📊 {name}")
        print(f"   Shape   : {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"   Columns : {', '.join(df.columns[:10])}", end="")
        if len(df.columns) > 10:
            print(f" ... +{len(df.columns) - 10} more")
        else:
            print()
        print(f"   Dtypes  : {dict(df.dtypes.value_counts())}")

    # ── Save to CSV ───────────────────────────────────────────────────
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    print(f"\n💾 Saving CSVs to {data_dir} ...")
    for name, df in datasets.items():
        path = os.path.join(data_dir, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"   ✅ {name}.csv  ({df.shape[0]} rows)")

    print("\n🎉 Done! Datasets are ready for analysis in the data/ folder.")
    print("   You can now import them in your notebooks / scripts:")
    print('   >>> import pandas as pd')
    print('   >>> machines = pd.read_csv("data/machines.csv")')


if __name__ == "__main__":
    main()
