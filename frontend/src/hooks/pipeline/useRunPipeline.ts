import { useMutation, useQueryClient } from "@tanstack/react-query";
import { runPipeline } from "../../api/services/pipelineService";
import type { PipelineParams } from "../../api/services/pipelineService";

export function useRunPipeline() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["runPipeline"],
    mutationFn: (params: PipelineParams) => runPipeline(params),
    onMutate: () => {
      try {
        localStorage.setItem("novaqure_pipeline_is_running", "true");
        localStorage.setItem("novaqure_pipeline_start_time", Date.now().toString());
      } catch {}
    },
    onSuccess: (data) => {
      try {
        localStorage.removeItem("novaqure_pipeline_is_running");
        localStorage.setItem("novaqure_last_pipeline_results", JSON.stringify(data));
      } catch {}
      queryClient.setQueryData(["latest_pipeline_run"], data);
      // Invalidate queries to reload dynamic molecule, experiment, and ranking lists
      queryClient.invalidateQueries({ queryKey: ["molecules"] });
      queryClient.invalidateQueries({ queryKey: ["rankings"] });
      queryClient.invalidateQueries({ queryKey: ["experiments"] });
    },
    onError: () => {
      try {
        localStorage.removeItem("novaqure_pipeline_is_running");
      } catch {}
    }
  });
}
