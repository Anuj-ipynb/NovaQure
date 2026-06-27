import api from "../client";

import type {
  Experiment,
} from "../../types/models/experiment";

export async function getExperiments():
Promise<Experiment[]> {

  const response =
    await api.get(
      "/api/v1/experiments"
    );

  return response.data;
}

export async function getExperiment(
  experimentId: string,
): Promise<Experiment> {

  const response =
    await api.get(
      `/api/v1/experiments/${experimentId}`
    );

  return response.data;
}
