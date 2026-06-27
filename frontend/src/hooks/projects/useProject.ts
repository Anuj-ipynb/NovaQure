import {
    useQuery,
} from "@tanstack/react-query";

import {
    getProject,
} from "../../api/services/projectService";

import {
    queryKeys,
} from "../../api/queryKeys";

export function useProject(
    projectId: string,
) {
    return useQuery({
        queryKey:
            queryKeys.project(
                projectId,
            ),

        queryFn: () =>
            getProject(
                projectId,
            ),

        enabled:
            !!projectId,
    });
}
