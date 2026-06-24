from fastapi import FastAPI

from backend.api.health import router as health_router

app = FastAPI(
    title="NovaQure API",
    version="1.0"
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)
