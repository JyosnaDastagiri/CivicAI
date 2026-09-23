import { api } from "./api";
import type { Complaint, ComplaintDetail } from "../types";

export interface CreateComplaintPayload {
  title: string;
  description: string;
  category: string;
  severity: string;
  safety_risk: boolean;
  location: { latitude: number; longitude: number; address?: string };
  image_url?: string;
}

export async function createComplaint(payload: CreateComplaintPayload) {
  const res = await api.post("/api/complaints", payload);
  return res.data.data as Complaint;
}

export async function listComplaints(params?: { status_filter?: string }) {
  const res = await api.get("/api/complaints", { params });
  return res.data.data as Complaint[];
}

export async function getComplaint(id: number) {
  const res = await api.get(`/api/complaints/${id}`);
  return res.data.data as ComplaintDetail;
}

export async function changeStatus(id: number, status: string, description?: string) {
  const res = await api.post(`/api/complaints/${id}/status`, { status, description });
  return res.data.data as Complaint;
}

export async function acknowledgeComplaint(id: number, note?: string) {
  const res = await api.post(`/api/complaints/${id}/acknowledge`, { note });
  return res.data.data;
}

export async function resolveComplaint(id: number, description: string, evidence_url?: string) {
  const res = await api.post(`/api/complaints/${id}/resolve`, { description, evidence_url });
  return res.data.data;
}

export async function closeComplaint(id: number) {
  const res = await api.post(`/api/complaints/${id}/close`);
  return res.data;
}

export async function reassignComplaint(id: number, new_officer_id: number, reason?: string) {
  const res = await api.post(`/api/complaints/${id}/reassign`, { new_officer_id, reason });
  return res.data.data;
}

export async function analyzeImage(image_url: string, description?: string) {
  const res = await api.post("/api/ai/analyze-image", { image_url, description });
  return res.data.data;
}

export async function generateComplaintText(
  citizen_description: string, category: string, severity: string, safety_risk: boolean, address?: string
) {
  const res = await api.post("/api/ai/generate-complaint", { citizen_description, category, severity, safety_risk, address });
  return res.data.data;
}

export async function uploadImage(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post("/api/uploads/image", formData, { headers: { "Content-Type": "multipart/form-data" } });
  return res.data.data as { url: string };
}
