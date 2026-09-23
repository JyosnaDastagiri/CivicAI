import React from "react";

const STATUS_STYLES: Record<string, string> = {
  SUBMITTED: "bg-slate-100 text-slate-700",
  AI_ANALYZED: "bg-blue-100 text-blue-700",
  ASSIGNED: "bg-indigo-100 text-indigo-700",
  ACKNOWLEDGED: "bg-cyan-100 text-cyan-700",
  IN_PROGRESS: "bg-amber-100 text-amber-700",
  RESOLVED: "bg-green-100 text-green-700",
  CLOSED: "bg-slate-200 text-slate-600",
  ESCALATED: "bg-red-100 text-red-700",
  REJECTED: "bg-rose-100 text-rose-700",
};

export const StatusBadge: React.FC<{ status: string }> = ({ status }) => (
  <span className={`inline-block rounded-full px-2.5 py-1 text-xs font-medium ${STATUS_STYLES[status] || "bg-slate-100 text-slate-700"}`}>
    {status.replace(/_/g, " ")}
  </span>
);

const PRIORITY_STYLES: Record<string, string> = {
  LOW: "bg-slate-100 text-slate-600",
  MEDIUM: "bg-yellow-100 text-yellow-700",
  HIGH: "bg-orange-100 text-orange-700",
  CRITICAL: "bg-red-100 text-red-700",
};

export const PriorityBadge: React.FC<{ priority: string | null }> = ({ priority }) => {
  if (!priority) return <span className="text-xs text-slate-400">Pending</span>;
  return (
    <span className={`inline-block rounded-full px-2.5 py-1 text-xs font-semibold ${PRIORITY_STYLES[priority] || "bg-slate-100 text-slate-600"}`}>
      {priority}
    </span>
  );
};
