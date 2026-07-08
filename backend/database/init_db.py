"""
Database initialization.

Imports every model before creating tables.
"""

from backend.database.base import Base
from backend.database.session import engine

# -------------------------------
# Import every model here
# -------------------------------

from backend.models.user import User
from backend.models.project import Project
from backend.models.experiment import Experiment
from backend.models.molecule import Molecule
from backend.models.evaluation import Evaluation
from backend.models.ranking import Ranking
from backend.models.agent_log import AgentLog
from backend.models.reliability import ReliabilityMetric


def initialize_database():
    """
    Creates all database tables that have
    been registered with SQLAlchemy metadata.
    """

    Base.metadata.create_all(
        bind=engine,
    )
