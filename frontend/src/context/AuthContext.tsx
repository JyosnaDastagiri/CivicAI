import React, { createContext, useContext, useEffect, useState } from "react";
import type { User } from "../types";
import * as authApi from "../services/auth";

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<User>;
  register: (name: string, email: string, password: string) => Promise<User>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("civicai_token");
    const cachedUser = localStorage.getItem("civicai_user");
    if (token && cachedUser) {
      setUser(JSON.parse(cachedUser));
    }
    setLoading(false);
  }, []);

  const persist = (token: string, u: User) => {
    localStorage.setItem("civicai_token", token);
    localStorage.setItem("civicai_user", JSON.stringify(u));
    setUser(u);
  };

  const login = async (email: string, password: string) => {
    const { access_token, user: u } = await authApi.login(email, password);
    persist(access_token, u);
    return u;
  };

  const register = async (name: string, email: string, password: string) => {
    const { access_token, user: u } = await authApi.register(name, email, password);
    persist(access_token, u);
    return u;
  };

  const logout = () => {
    localStorage.removeItem("civicai_token");
    localStorage.removeItem("civicai_user");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
