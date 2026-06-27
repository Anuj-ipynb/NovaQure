import api from "../client";

import type {
    Ranking,
} from "../../types/models/ranking";

export async function getRankings():
Promise<Ranking[]> {

    const response =
        await api.get(
            "/api/v1/rankings"
        );

    return response.data;
}

export async function getRanking(
    rankingId: string,
): Promise<Ranking> {

    const response =
        await api.get(
            `/api/v1/rankings/${rankingId}`
        );

    return response.data;
}
