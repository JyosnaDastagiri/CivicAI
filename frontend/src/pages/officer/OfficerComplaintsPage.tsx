import React, { useEffect, useState } from "react";
import { listComplaints } from "../../services/complaints";
import type { Complaint } from "../../types";
import { StatusBadge, PriorityBadge } from "../../components/StatusBadge";
import { LoadingState } from "../../components/LoadingState";
import { EmptyState } from "../../components/EmptyState";

export const OfficerComplaintsPage: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[] | null>(null);
  useEffect(() => { listComplaints().then(setComplaints); }, []);
  if (!complaints) return <LoadingState />;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold text-slate-800">Assigned Complaints</h1>
      {complaints.length === 0 ? (
        <div className="card"><EmptyState title="No complaints assigned yet" /></div>
      ) : (
        <div className="card overflow-x-auto p-0">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500 border-b border-slate-100">
                <th className="py-3 px-4">ID</th><th className="py-3 px-4">Category</th><th className="py-3 px-4">Priority</th>
                <th className="py-3 px-4">Assigned</th><th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {complaints.map((c) => (
                <tr key={c.id} className="border-b border-slate-50 hover:bg-slate-50 cursor-pointer" onClick={() => (window.location.href = `/officer/complaints/${c.id}`)}>
                  <td className="py-3 px-4 text-slate-400">#{c.id}</td>
                  <td className="py-3 px-4">{c.category}</td>
                  <td className="py-3 px-4"><PriorityBadge priority={c.priority} /></td>
                  <td className="py-3 px-4 text-slate-400">{new Date(c.created_at).toLocaleDateString()}</td>
                  <td className="py-3 px-4"><StatusBadge status={c.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
