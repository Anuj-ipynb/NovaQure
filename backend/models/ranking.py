from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base
from backend.models.base_model import TimestampMixin, UUIDMixin


class Ranking(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "rankings"

    molecule_id: Mapped[str] = mapped_column(
        ForeignKey("molecules.id"),
        nullable=False,
        unique=True,
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    molecule = relationship(
        "Molecule",
        back_populates="ranking",
    )
