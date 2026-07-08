import {
    useQuery,
} from "@tanstack/react-query";

import {
    getProjects,
} from "../../api/services/projectService";

import {
    queryKeys,
} from "../../api/queryKeys";

export function useProjects() {

    return useQuery({
        queryKey:
            queryKeys.projects,

        queryFn:
            getProjects,
    });
}
