import { api } from "./api";
import type { Notification } from "../types";

export async function listNotifications(unreadOnly = false) {
  const res = await api.get("/api/notifications", { params: { unread_only: unreadOnly } });
  return res.data.data as Notification[];
}

export async function markNotificationRead(id: number) {
  return api.post(`/api/notifications/${id}/read`);
}
