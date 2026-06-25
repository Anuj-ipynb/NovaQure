"""
Central SQLAlchemy Base.

Every model in NovaQure must inherit
from this Base class.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# Import all models here.
#
# This ensures SQLAlchemy knows every table
# before metadata.create_all() is executed.
# ---------------------------------------------------------

from backend.models.agent_log import AgentLog
from backend.models.evaluation import Evaluation
from backend.models.experiment import Experiment
from backend.models.molecule import Molecule
from backend.models.project import Project
from backend.models.ranking import Ranking
from backend.models.user import User

__all__ = [
    "Base",
    "User",
    "Project",
    "Experiment",
    "Molecule",
    "Evaluation",
    "Ranking",
    "AgentLog",
]
