import React, { useEffect, useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import {
  LayoutDashboard, FileText, PlusCircle, Bell, User as UserIcon, LogOut,
  Users, Building2, Settings, ScrollText, AlertTriangle, BarChart3, ClipboardList,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { listNotifications } from "../services/notifications";

interface NavItem { to: string; label: string; icon: React.ReactNode; }

const NAV_BY_ROLE: Record<string, NavItem[]> = {
  CITIZEN: [
    { to: "/dashboard", label: "Dashboard", icon: <LayoutDashboard className="w-4 h-4" /> },
    { to: "/complaints", label: "My Complaints", icon: <FileText className="w-4 h-4" /> },
    { to: "/complaints/new", label: "Report Issue", icon: <PlusCircle className="w-4 h-4" /> },
    { to: "/notifications", label: "Notifications", icon: <Bell className="w-4 h-4" /> },
    { to: "/profile", label: "Profile", icon: <UserIcon className="w-4 h-4" /> },
  ],
  OFFICER: [
    { to: "/officer/dashboard", label: "Dashboard", icon: <LayoutDashboard className="w-4 h-4" /> },
    { to: "/officer/complaints", label: "Assigned Complaints", icon: <ClipboardList className="w-4 h-4" /> },
    { to: "/notifications", label: "Notifications", icon: <Bell className="w-4 h-4" /> },
  ],
  DEPARTMENT_HEAD: [
    { to: "/head/dashboard", label: "Dashboard", icon: <LayoutDashboard className="w-4 h-4" /> },
    { to: "/head/complaints", label: "Department Complaints", icon: <FileText className="w-4 h-4" /> },
    { to: "/head/escalations", label: "Escalations", icon: <AlertTriangle className="w-4 h-4" /> },
    { to: "/head/analytics", label: "Analytics", icon: <BarChart3 className="w-4 h-4" /> },
    { to: "/notifications", label: "Notifications", icon: <Bell className="w-4 h-4" /> },
  ],
  ADMIN: [
    { to: "/admin/dashboard", label: "Dashboard", icon: <LayoutDashboard className="w-4 h-4" /> },
    { to: "/admin/users", label: "Users", icon: <Users className="w-4 h-4" /> },
    { to: "/admin/departments", label: "Departments", icon: <Building2 className="w-4 h-4" /> },
    { to: "/admin/complaints", label: "All Complaints", icon: <FileText className="w-4 h-4" /> },
    { to: "/admin/escalations", label: "Escalations", icon: <AlertTriangle className="w-4 h-4" /> },
    { to: "/admin/analytics", label: "Analytics", icon: <BarChart3 className="w-4 h-4" /> },
    { to: "/admin/settings", label: "Settings", icon: <Settings className="w-4 h-4" /> },
    { to: "/admin/audit-logs", label: "Audit Logs", icon: <ScrollText className="w-4 h-4" /> },
  ],
};

const ROLE_LABEL: Record<string, string> = {
  CITIZEN: "Citizen Portal", OFFICER: "Officer Console", DEPARTMENT_HEAD: "Department Head Console", ADMIN: "Admin Console",
};

export const AppLayout: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [unread, setUnread] = useState(0);

  useEffect(() => {
    if (!user) return;
    listNotifications(true).then((n) => setUnread(n.length)).catch(() => {});
  }, [user]);

  if (!user) return null;
  const items = NAV_BY_ROLE[user.role] || [];

  return (
    <div className="min-h-screen flex bg-slate-50">
      <aside className="w-64 bg-civic-900 text-white flex flex-col shrink-0">
        <div className="p-5 border-b border-civic-800">
          <p className="text-lg font-bold tracking-tight">CivicAI</p>
          <p className="text-xs text-civic-200 mt-0.5">{ROLE_LABEL[user.role]}</p>
        </div>
        <nav className="flex-1 py-4 space-y-1 px-3">
          {items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
                  isActive ? "bg-civic-700 text-white" : "text-civic-100 hover:bg-civic-800"
                } ${item.to === "/notifications" && unread > 0 ? "relative" : ""}`
              }
            >
              {item.icon}
              {item.label}
              {item.to === "/notifications" && unread > 0 && (
                <span className="ml-auto bg-red-500 text-white text-[10px] rounded-full px-1.5 py-0.5">{unread}</span>
              )}
            </NavLink>
          ))}
        </nav>
        <div className="p-3 border-t border-civic-800">
          <div className="px-3 py-2 text-xs text-civic-200 truncate">{user.name} &middot; {user.email}</div>
          <button
            onClick={() => { logout(); navigate("/login"); }}
            className="w-full flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-civic-100 hover:bg-civic-800"
          >
            <LogOut className="w-4 h-4" /> Sign out
          </button>
        </div>
      </aside>
      <main className="flex-1 min-w-0">
        <div className="max-w-6xl mx-auto p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
