import api from "../../client";

import type {
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    User,
} from "../../../types/auth/auth";

export async function login(
    payload: LoginRequest,
): Promise<TokenResponse> {

    const response = await api.post(
        "/api/v1/auth/login",
        payload,
    );

    return response.data;
}

export async function register(
    payload: RegisterRequest,
): Promise<void> {

    await api.post(
        "/api/v1/auth/register",
        payload,
    );
}

export async function getCurrentUser(
): Promise<User> {

    const response = await api.get(
        "/api/v1/auth/me",
    );

    return response.data;
}
