from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.routes import (
    auth_router,
    health_router,
    project_router,
    experiment_router,
    molecule_router,
    ranking_router,
)

from backend.database.init_db import (
    initialize_database,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle handler.
    """

    # Initialize database tables
    initialize_database()

    yield

    # Shutdown logic can be added here later


app = FastAPI(
    title="NovaQure API",
    description=(
        "Noise-Adaptive Hybrid AI–Quantum "
        "Framework for Intelligent Drug Discovery"
    ),
    version="1.0.0",
    lifespan=lifespan,
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


# ---------------------------------------------------------
# Health Routes
# ---------------------------------------------------------

app.include_router(
    health_router,
    prefix="/api/v1",
)

# ---------------------------------------------------------
# Authentication Routes
# ---------------------------------------------------------

app.include_router(
    auth_router,
    prefix="/api/v1",
)

# ---------------------------------------------------------
# Project Routes
# ---------------------------------------------------------

app.include_router(
    project_router,
    prefix="/api/v1",
)

# ---------------------------------------------------------
# Experiment Routes
# ---------------------------------------------------------

app.include_router(
    experiment_router,
    prefix="/api/v1",
)

# ---------------------------------------------------------
# Molecule Routes
# ---------------------------------------------------------

app.include_router(
    molecule_router,
    prefix="/api/v1",
)

# ---------------------------------------------------------
# Ranking Routes
# ---------------------------------------------------------

app.include_router(
    ranking_router,
    prefix="/api/v1",
)
