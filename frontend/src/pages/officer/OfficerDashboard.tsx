import React, { useEffect, useState } from "react";
import { ClipboardList, Clock, CheckCircle2, AlertTriangle, PlayCircle, ListChecks, ArrowUpRight } from "lucide-react";
import { StatCard } from "../../components/StatCard";
import { LoadingState } from "../../components/LoadingState";
import { getOfficerDashboard } from "../../services/dashboard";

export const OfficerDashboard: React.FC = () => {
  const [data, setData] = useState<any>(null);
  useEffect(() => { getOfficerDashboard().then(setData); }, []);
  if (!data) return <LoadingState />;

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold text-slate-800">Officer Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Assigned" value={data.assigned} icon={<ClipboardList className="w-8 h-8" />} />
        <StatCard label="Awaiting Acknowledgement" value={data.awaitingAcknowledgement} icon={<Clock className="w-8 h-8" />} accent="text-amber-600" />
        <StatCard label="Acknowledged" value={data.acknowledged} icon={<CheckCircle2 className="w-8 h-8" />} accent="text-cyan-600" />
        <StatCard label="In Progress" value={data.inProgress} icon={<PlayCircle className="w-8 h-8" />} accent="text-blue-600" />
        <StatCard label="Overdue" value={data.overdue} icon={<AlertTriangle className="w-8 h-8" />} accent="text-red-600" />
        <StatCard label="Resolved" value={data.resolved} icon={<ListChecks className="w-8 h-8" />} accent="text-green-600" />
        <StatCard label="Escalated" value={data.escalated} icon={<ArrowUpRight className="w-8 h-8" />} accent="text-red-600" />
      </div>
    </div>
  );
};
