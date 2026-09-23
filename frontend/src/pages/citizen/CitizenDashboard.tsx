import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { FileText, AlertTriangle, CheckCircle2, ListChecks, PlusCircle } from "lucide-react";
import { StatCard } from "../../components/StatCard";
import { StatusBadge, PriorityBadge } from "../../components/StatusBadge";
import { LoadingState } from "../../components/LoadingState";
import { getCitizenDashboard } from "../../services/dashboard";

export const CitizenDashboard: React.FC = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    getCitizenDashboard().then(setData);
  }, []);

  if (!data) return <LoadingState />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Your Dashboard</h1>
          <p className="text-sm text-slate-500">Overview of the civic issues you've reported.</p>
        </div>
        <Link to="/complaints/new" className="btn-primary"><PlusCircle className="w-4 h-4" /> Report an Issue</Link>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Complaints" value={data.totalComplaints} icon={<FileText className="w-8 h-8" />} />
        <StatCard label="Active" value={data.activeComplaints} icon={<ListChecks className="w-8 h-8" />} accent="text-amber-600" />
        <StatCard label="Resolved" value={data.resolvedComplaints} icon={<CheckCircle2 className="w-8 h-8" />} accent="text-green-600" />
        <StatCard label="Escalated" value={data.escalatedComplaints} icon={<AlertTriangle className="w-8 h-8" />} accent="text-red-600" />
      </div>

      <div className="card">
        <h2 className="font-semibold text-slate-800 mb-3">Recent Complaints</h2>
        {data.recentComplaints.length === 0 ? (
          <p className="text-sm text-slate-400">You haven't reported any issues yet.</p>
        ) : (
          <div className="divide-y divide-slate-100">
            {data.recentComplaints.map((c: any) => (
              <Link key={c.id} to={`/complaints/${c.id}`} className="flex items-center justify-between py-3 hover:bg-slate-50 -mx-2 px-2 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-slate-700">{c.title}</p>
                  <p className="text-xs text-slate-400">{new Date(c.createdAt).toLocaleDateString()}</p>
                </div>
                <div className="flex items-center gap-2">
                  <PriorityBadge priority={c.priority} />
                  <StatusBadge status={c.status} />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
