"""
NovaQure API Routes

Every FastAPI router is registered here
before being imported by main.py
"""

from .auth import router as auth_router
from .health import router as health_router
from .projects import router as project_router
from .experiments import router as experiment_router
from .molecules import router as molecule_router
from .rankings import router as ranking_router


__all__ = [
    "auth_router",
    "health_router",
    "project_router",
    "experiment_router",
    "molecule_router",
    "ranking_router",
]
