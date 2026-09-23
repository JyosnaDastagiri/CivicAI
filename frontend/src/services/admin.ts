import { api } from "./api";
import type { User, Department, SystemSetting } from "../types";

export async function listUsers() {
  return (await api.get("/api/admin/users")).data.data as User[];
}
export async function createUser(payload: { name: string; email: string; password: string; role: string; department_id?: number | null }) {
  return (await api.post("/api/admin/users", payload)).data.data as User;
}
export async function updateUser(id: number, payload: Partial<{ name: string; role: string; department_id: number | null; is_active: boolean }>) {
  return (await api.put(`/api/admin/users/${id}`, payload)).data.data as User;
}
export async function listDepartments() {
  return (await api.get("/api/admin/departments")).data.data as Department[];
}
export async function createDepartment(payload: { name: string; description?: string }) {
  return (await api.post("/api/admin/departments", payload)).data.data as Department;
}
export async function listSettings() {
  return (await api.get("/api/settings")).data.data as SystemSetting[];
}
export async function updateSetting(key: string, value: string) {
  return (await api.put(`/api/settings/${key}`, { value })).data.data as SystemSetting;
}
export async function listAuditLogs(complaint_id?: number) {
  return (await api.get("/api/audit-logs", { params: { complaint_id } })).data.data;
}
export async function listEscalations() {
  return (await api.get("/api/escalations")).data.data;
}
export async function acknowledgeEscalation(id: number) {
  return api.post(`/api/escalations/${id}/acknowledge`);
}
