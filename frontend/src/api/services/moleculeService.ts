import api from "../client";

import type {
    Molecule,
} from "../../types/models/molecule";

export async function getMolecules():
Promise<Molecule[]> {

    const response =
        await api.get(
            "/api/v1/molecules"
        );

    return response.data;
}

export async function getMolecule(
    moleculeId: string,
): Promise<Molecule> {

    const response =
        await api.get(
            `/api/v1/molecules/${moleculeId}`
        );

    return response.data;
}
