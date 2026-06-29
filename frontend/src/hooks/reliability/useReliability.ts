import {
  useQuery,
} from "@tanstack/react-query";

import {
  getReliability,
} from "../../api/services/reliabilityService";

export function useReliability() {

  return useQuery({
    queryKey: [
      "reliability",
    ],

    queryFn:
      getReliability,
  });
}
