"""
Configuration module — loads environment variables from .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "https://test.energyeta.ai")
ENERGYETA_TOKEN: str = os.getenv("ENERGYETA_TOKEN", "")
DEFAULT_CLIENT_ID: str = os.getenv("DEFAULT_CLIENT_ID", "65eea4893ca87cc2c6a63429")

if not ENERGYETA_TOKEN or ENERGYETA_TOKEN == "paste-your-firebase-jwt-here":
    print("⚠️  WARNING: ENERGYETA_TOKEN is not set in .env — API calls will fail with 401.")
