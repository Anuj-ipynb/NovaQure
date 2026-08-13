import { useMutation, useQueryClient } from "@tanstack/react-query";
import { runPipeline } from "../../api/services/pipelineService";
import type { PipelineParams } from "../../api/services/pipelineService";

export function useRunPipeline() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (params: PipelineParams) => runPipeline(params),
    onSuccess: () => {
      // Invalidate queries to reload dynamic molecule, experiment, and ranking lists
      queryClient.invalidateQueries({ queryKey: ["molecules"] });
      queryClient.invalidateQueries({ queryKey: ["rankings"] });
      queryClient.invalidateQueries({ queryKey: ["experiments"] });
    }
  });
}
