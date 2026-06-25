from contextlib import asynccontextmanager

from fastapi import FastAPI
from backend.api.routes import (
    health_router,
    project_router,
)
from backend.database.init_db import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan.

    Runs once during startup and once during shutdown.
    """

    # Initialize database (Development)
    initialize_database()

    yield

    # Shutdown logic can be added here later


app = FastAPI(
    title="NovaQure API",
    description="Noise-Adaptive Hybrid AI–Quantum Drug Discovery Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------
# Health Routes
# ---------------------------------------------------------

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

# ---------------------------------------------------------
# Project Routes
# ---------------------------------------------------------

app.include_router(
    project_router,
    prefix="/api/v1",
)

# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get(
    "/",
    tags=["Root"],
)
def root():
    """
    Root endpoint.
    """

    return {
        "project": "NovaQure",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }
