import api from "../client";

export interface PipelineParams {
  energy: number;
  variance: number;
  noise: number;
  convergence: number;
}

export async function runPipeline(params: PipelineParams) {
  const response = await api.post("/api/v1/pipeline/run", params);
  return response.data;
}
