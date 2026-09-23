import type { UserRole } from "../types";

export const ROLE_HOME: Record<UserRole, string> = {
  CITIZEN: "/dashboard",
  OFFICER: "/officer/dashboard",
  DEPARTMENT_HEAD: "/head/dashboard",
  ADMIN: "/admin/dashboard",
};
