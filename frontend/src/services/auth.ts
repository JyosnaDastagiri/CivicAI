import { api } from "./api";
import type { User } from "../types";

export async function login(email: string, password: string) {
  const res = await api.post("/api/auth/login", { email, password });
  return res.data.data as { access_token: string; user: User };
}

export async function register(name: string, email: string, password: string) {
  const res = await api.post("/api/auth/register", { name, email, password });
  return res.data.data as { access_token: string; user: User };
}

export async function fetchMe() {
  const res = await api.get("/api/auth/me");
  return res.data.data as User;
}
