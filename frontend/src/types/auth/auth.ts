export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest {
    email: string;
    password: string;
    full_name: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
    expires_in: number;
}

export interface User {
    id: string;
    email: string;
    full_name: string;
    role: string;
    created_at?: string;
}

export interface AuthContextType {
    user: User | null;

    token: string | null;

    isAuthenticated: boolean;

    login: (
        email: string,
        password: string,
    ) => Promise<void>;

    register: (
        payload: RegisterRequest,
    ) => Promise<void>;

    logout: () => void;

    loading: boolean;
}
