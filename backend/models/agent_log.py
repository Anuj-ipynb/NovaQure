from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base
from backend.models.base_model import TimestampMixin, UUIDMixin


class AgentLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_logs"

    experiment_id: Mapped[str] = mapped_column(
        ForeignKey("experiments.id"),
        nullable=False,
    )

    agent_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    log_level: Mapped[str] = mapped_column(
        String(20),
        default="INFO",
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    experiment = relationship(
        "Experiment",
        back_populates="agent_logs",
    )
