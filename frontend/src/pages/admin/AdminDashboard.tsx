import React, { useEffect, useState } from "react";
import { FileText, Inbox, CheckCircle2, AlertOctagon, ArrowUpRight, Copy } from "lucide-react";
import { StatCard } from "../../components/StatCard";
import { LoadingState } from "../../components/LoadingState";
import { getAdminDashboard } from "../../services/dashboard";

export const AdminDashboard: React.FC = () => {
  const [data, setData] = useState<any>(null);
  useEffect(() => { getAdminDashboard().then(setData); }, []);
  if (!data) return <LoadingState />;

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold text-slate-800">Admin Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <StatCard label="Total Complaints" value={data.totalComplaints} icon={<FileText className="w-8 h-8" />} />
        <StatCard label="Open" value={data.openComplaints} icon={<Inbox className="w-8 h-8" />} accent="text-amber-600" />
        <StatCard label="Resolved" value={data.resolvedComplaints} icon={<CheckCircle2 className="w-8 h-8" />} accent="text-green-600" />
        <StatCard label="Critical" value={data.criticalComplaints} icon={<AlertOctagon className="w-8 h-8" />} accent="text-red-600" />
        <StatCard label="Escalated" value={data.escalatedComplaints} icon={<ArrowUpRight className="w-8 h-8" />} accent="text-red-600" />
        <StatCard label="Duplicates" value={data.duplicateComplaints} icon={<Copy className="w-8 h-8" />} accent="text-slate-500" />
      </div>
    </div>
  );
};
