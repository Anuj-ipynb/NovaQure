"""
Database initialization utilities.

Responsible for creating tables during
development.

Production environments should use
Alembic migrations.
"""

from backend.database.base import Base
from backend.database.session import engine


def initialize_database() -> None:
    """
    Create all registered tables.

    This is intended for local development.
    """

    Base.metadata.create_all(bind=engine)
