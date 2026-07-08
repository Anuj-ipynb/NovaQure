import {
    useQuery,
} from "@tanstack/react-query";

import {
    getMolecules,
} from "../../api/services/moleculeService";

export function useMolecules() {

    return useQuery({
        queryKey: [
            "molecules",
        ],

        queryFn:
            getMolecules,
    });
}
