import {
  useQuery,
} from "@tanstack/react-query";

import {
  getExperiments,
} from "../../api/services/experimentService";

export function useExperiments() {
  return useQuery({
    queryKey: [
      "experiments",
    ],

    queryFn:
      getExperiments,
  });
}
