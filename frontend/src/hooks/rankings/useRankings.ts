import {
    useQuery,
} from "@tanstack/react-query";

import {
    getRankings,
} from "../../api/services/rankingService";

export function useRankings() {

    return useQuery({
        queryKey: [
            "rankings",
        ],

        queryFn:
            getRankings,
    });
}
