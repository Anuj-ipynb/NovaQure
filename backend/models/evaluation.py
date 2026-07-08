from sqlalchemy import Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base
from backend.models.base_model import TimestampMixin, UUIDMixin


class Evaluation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "evaluations"

    molecule_id: Mapped[str] = mapped_column(
        ForeignKey("molecules.id"),
        nullable=False,
        unique=True,
    )

    qed: Mapped[float] = mapped_column(Float, default=0.0)
    sa_score: Mapped[float] = mapped_column(Float, default=0.0)
    binding_affinity: Mapped[float] = mapped_column(Float, default=0.0)
    lipinski_pass: Mapped[bool] = mapped_column(Boolean, default=False)

    molecule = relationship(
        "Molecule",
        back_populates="evaluation",
    )
