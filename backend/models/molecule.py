from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base
from backend.models.base_model import TimestampMixin, UUIDMixin


class Molecule(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "molecules"

    experiment_id: Mapped[str] = mapped_column(
        ForeignKey("experiments.id"),
        nullable=False,
    )

    smiles: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    selfies: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
    )

    score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    experiment = relationship(
        "Experiment",
        back_populates="molecules",
    )

    evaluation = relationship(
        "Evaluation",
        back_populates="molecule",
        uselist=False,
        cascade="all, delete-orphan",
    )

    ranking = relationship(
        "Ranking",
        back_populates="molecule",
        uselist=False,
        cascade="all, delete-orphan",
    )
