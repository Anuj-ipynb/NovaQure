from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base
from backend.models.base_model import TimestampMixin, UUIDMixin


class ReliabilityMetric(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "reliability_metrics"

    overall_reliability: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    ai_confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    quantum_noise: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    aqkc_corrections: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    confidence_calibration: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    noise_compensation: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    prediction_stability: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    reliability_engine_status: Mapped[str] = mapped_column(
        String(50),
        default="Operational",
    )

    noise_estimator_status: Mapped[str] = mapped_column(
        String(50),
        default="Operational",
    )

    aqkc_module_status: Mapped[str] = mapped_column(
        String(50),
        default="Operational",
    )

    calibration_layer_status: Mapped[str] = mapped_column(
        String(50),
        default="Monitoring",
    )
