import { api } from "./api";

export async function getCitizenDashboard() {
  return (await api.get("/api/dashboard/citizen")).data.data;
}
export async function getOfficerDashboard() {
  return (await api.get("/api/dashboard/officer")).data.data;
}
export async function getDepartmentDashboard() {
  return (await api.get("/api/dashboard/department")).data.data;
}
export async function getAdminDashboard() {
  return (await api.get("/api/dashboard/admin")).data.data;
}
export async function getAnalytics(path: string) {
  return (await api.get(`/api/analytics/${path}`)).data.data;
}
