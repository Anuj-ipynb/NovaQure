from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReliabilityBase(BaseModel):
    overall_reliability: float
    ai_confidence: float
    quantum_noise: float
    aqkc_corrections: int

    confidence_calibration: float
    noise_compensation: float
    prediction_stability: float

    reliability_engine_status: str
    noise_estimator_status: str
    aqkc_module_status: str
    calibration_layer_status: str


class ReliabilityCreate(ReliabilityBase):
    pass


class ReliabilityUpdate(BaseModel):
    overall_reliability: Optional[float] = None
    ai_confidence: Optional[float] = None
    quantum_noise: Optional[float] = None
    aqkc_corrections: Optional[int] = None

    confidence_calibration: Optional[float] = None
    noise_compensation: Optional[float] = None
    prediction_stability: Optional[float] = None

    reliability_engine_status: Optional[str] = None
    noise_estimator_status: Optional[str] = None
    aqkc_module_status: Optional[str] = None
    calibration_layer_status: Optional[str] = None


class ReliabilityResponse(ReliabilityBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
