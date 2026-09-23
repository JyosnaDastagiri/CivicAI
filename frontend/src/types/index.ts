export type UserRole = "CITIZEN" | "OFFICER" | "DEPARTMENT_HEAD" | "ADMIN";

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  department_id: number | null;
  is_active: boolean;
}

export type ComplaintStatus =
  | "SUBMITTED" | "AI_ANALYZED" | "ASSIGNED" | "ACKNOWLEDGED"
  | "IN_PROGRESS" | "RESOLVED" | "CLOSED" | "ESCALATED" | "REJECTED";

export type Severity = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type Priority = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface Complaint {
  id: number;
  citizen_id: number;
  title: string;
  description: string;
  category: string;
  severity: Severity;
  safety_risk: boolean;
  priority: Priority | null;
  priority_score: number | null;
  status: ComplaintStatus;
  department_id: number | null;
  created_at: string;
  updated_at: string;
  resolved_at: string | null;
}

export interface ComplaintDetail {
  complaint: Complaint;
  location: { latitude: number; longitude: number; address: string | null } | null;
  images: { storage_url: string; file_name: string }[];
  analysis: any[];
  priorityAnalysis: {
    severity_score: number; safety_score: number; location_score: number;
    recurrence_score: number; urgency_score: number; final_score: number;
    priority: string; explanation: string;
  } | null;
  assignment: {
    id: number; assigned_to: number; assigned_at: string; assignment_status: string;
    acknowledgement_deadline: string; acknowledged_at: string | null; acknowledged_by: number | null;
    resolution_deadline: string | null;
  } | null;
  duplicates: {
    similar_complaint_id: number; text_similarity: number; distance_meters: number;
    duplicate_score: number; is_potential_duplicate: boolean;
  }[];
  escalations: { reason: string; escalated_at: string; status: string }[];
  resolution: { description: string; evidence_url: string | null; created_at: string } | null;
  timeline: { status: string; description: string | null; created_at: string }[];
}

export interface Department {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
}

export interface Notification {
  id: number;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
  complaint_id: number | null;
}

export interface SystemSetting {
  key: string;
  value: string;
  description: string | null;
  updated_at: string;
}
