export interface Reliability {
  id: string;

  overall_reliability: number;
  ai_confidence: number;
  quantum_noise: number;
  aqkc_corrections: number;

  confidence_calibration: number;
  noise_compensation: number;
  prediction_stability: number;

  reliability_engine_status: string;
  noise_estimator_status: string;
  aqkc_module_status: string;
  calibration_layer_status: string;

  created_at: string;
  updated_at: string;
}
