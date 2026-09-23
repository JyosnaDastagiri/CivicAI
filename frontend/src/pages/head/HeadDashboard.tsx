import React, { useEffect, useState } from "react";
import { FileText, Clock, AlertTriangle, ArrowUpRight, CheckCircle2 } from "lucide-react";
import { StatCard } from "../../components/StatCard";
import { LoadingState } from "../../components/LoadingState";
import { getDepartmentDashboard } from "../../services/dashboard";

export const HeadDashboard: React.FC = () => {
  const [data, setData] = useState<any>(null);
  useEffect(() => { getDepartmentDashboard().then(setData); }, []);
  if (!data) return <LoadingState />;

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold text-slate-800">Department Head Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <StatCard label="Department Complaints" value={data.departmentComplaintCount} icon={<FileText className="w-8 h-8" />} />
        <StatCard label="Pending Acknowledgement" value={data.pendingAcknowledgement} icon={<Clock className="w-8 h-8" />} accent="text-amber-600" />
        <StatCard label="Overdue" value={data.overdue} icon={<AlertTriangle className="w-8 h-8" />} accent="text-red-600" />
        <StatCard label="Escalated" value={data.escalated} icon={<ArrowUpRight className="w-8 h-8" />} accent="text-red-600" />
        <StatCard label="Resolved" value={data.resolved} icon={<CheckCircle2 className="w-8 h-8" />} accent="text-green-600" />
      </div>
      {data.priorityDistribution && (
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Priority Distribution</h2>
          <div className="grid grid-cols-4 gap-3 text-center text-sm">
            {Object.entries(data.priorityDistribution).map(([k, v]: any) => (
              <div key={k} className="rounded-lg bg-slate-50 p-3">
                <p className="text-slate-400">{k}</p>
                <p className="text-lg font-semibold text-civic-700">{v}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
