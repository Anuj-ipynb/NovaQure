"""
API Route Package
"""

from .health import router as health_router
from .projects import router as project_router

__all__ = [
    "health_router",
    "project_router",
]
