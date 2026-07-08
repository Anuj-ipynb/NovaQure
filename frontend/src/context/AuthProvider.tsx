import {
  useEffect,
  useState,
  ReactNode,
} from "react";

import { AuthContext } from "./AuthContext";

import {
  login as loginRequest,
  getCurrentUser,
} from "../api/services/auth/authService";

import type {
  User,
  RegisterRequest,
} from "../types/auth/auth";

type Props = {
  children: ReactNode;
};

export default function AuthProvider({
  children,
}: Props) {
  const [user, setUser] =
    useState<User | null>(null);

  const [token, setToken] =
    useState<string | null>(
      localStorage.getItem(
        "novaqure_token"
      )
    );

  const [loading, setLoading] =
    useState(true);

  const login = async (
    email: string,
    password: string,
  ) => {
    const response =
      await loginRequest({
        email,
        password,
      });

    localStorage.setItem(
      "novaqure_token",
      response.access_token,
    );

    setToken(
      response.access_token
    );

    const currentUser =
      await getCurrentUser();

    setUser(currentUser);
  };

  const register = async (
    _payload: RegisterRequest,
  ) => {
    console.log(
      "Registration UI coming in 9D-4",
    );
  };

  const logout = () => {
    localStorage.removeItem(
      "novaqure_token"
    );

    setToken(null);
    setUser(null);
  };

  useEffect(() => {
    const loadUser =
      async () => {
        try {
          const savedToken =
            localStorage.getItem(
              "novaqure_token"
            );

          if (!savedToken) {
            setLoading(false);
            return;
          }

          const currentUser =
            await getCurrentUser();

          setUser(currentUser);
        } catch {
          localStorage.removeItem(
            "novaqure_token"
          );

          setUser(null);
        } finally {
          setLoading(false);
        }
      };

    loadUser();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated:
          !!user,

        login,

        register,

        logout,

        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
