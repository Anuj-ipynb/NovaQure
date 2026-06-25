from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base
from backend.models.base_model import TimestampMixin, UUIDMixin


class Experiment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "experiments"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    target_protein: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    iterations: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="queued",
        nullable=False,
    )

    project = relationship(
        "Project",
        back_populates="experiments",
    )

    molecules = relationship(
        "Molecule",
        back_populates="experiment",
        cascade="all, delete-orphan",
    )

    agent_logs = relationship(
        "AgentLog",
        back_populates="experiment",
        cascade="all, delete-orphan",
    )
