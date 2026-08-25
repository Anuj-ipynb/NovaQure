from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import (
    generation_router,
    evaluation_router,
    pipeline_router
)

from backend.api.routes import (
    auth_router,
    health_router,
    project_router,
    experiment_router,
    molecule_router,
    ranking_router,
    reliability_router,
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# ---------------------------------------------------------
# Reliability Routes
# ---------------------------------------------------------

app.include_router(
    reliability_router,
    prefix="/api/v1",
)
app.include_router(
    generation_router,
    prefix="/api/v1",
)

app.include_router(
    evaluation_router,
    prefix="/api/v1",
)
app.include_router(
    pipeline_router,
    prefix="/api/v1",
)