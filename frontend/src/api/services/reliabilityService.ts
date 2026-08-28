import api from "../client";

import type {
  Reliability,
} from "../../types/models/reliability";

export async function getReliability():
Promise<Reliability[]> {

  const response =
    await api.get(
      "/api/v1/reliability"
    );

  return response.data;
}
