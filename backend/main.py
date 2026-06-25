from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.health import router as health_router
from backend.database.init_db import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup Events
    """

    initialize_database()

    yield

    """
    Shutdown Events
    """

    return


app = FastAPI(
    title="NovaQure API",
    version="1.0.0",
    description="Noise-Adaptive Hybrid AI-Quantum Drug Discovery Platform",
    lifespan=lifespan,
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)


@app.get("/")
def root():
    return {
        "project": "NovaQure",
        "version": "1.0.0",
        "status": "running",
    }
