"""
EnergyEta API Proxy — FastAPI application.
Proxies 20 GET endpoints from the Postman collection and exposes Swagger docs.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_client import close_async_client
from routers import machines, alerts


# ---------------------------------------------------------------------------
# Lifespan: manage shared httpx client
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — nothing special; client is created lazily
    yield
    # Shutdown — close httpx client
    await close_async_client()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="EnergyEta API Proxy",
    description=(
        "FastAPI proxy for the EnergyEta IoT platform.\n\n"
        "**Machine endpoints** — 16 GET routes for device data, energy stats, groups, and types.\n\n"
        "**Alert endpoints** — 4 GET routes for alerts, labels, and connectivity status.\n\n"
        "Visit `/docs` for the interactive Swagger UI."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Allow CORS for local dev / notebooks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(machines.router)
app.include_router(alerts.router)


# ---------------------------------------------------------------------------
# Root healthcheck
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "ok",
        "service": "EnergyEta API Proxy",
        "docs": "/docs",
        "endpoints": {
            "machine": 16,
            "alert": 4,
        },
    }
