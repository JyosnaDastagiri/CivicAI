import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { PlusCircle } from "lucide-react";
import { listComplaints } from "../../services/complaints";
import type { Complaint } from "../../types";
import { StatusBadge, PriorityBadge } from "../../components/StatusBadge";
import { LoadingState } from "../../components/LoadingState";
import { EmptyState } from "../../components/EmptyState";

export const ComplaintsListPage: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[] | null>(null);

  useEffect(() => {
    listComplaints().then(setComplaints);
  }, []);

  if (!complaints) return <LoadingState />;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-slate-800">My Complaints</h1>
        <Link to="/complaints/new" className="btn-primary"><PlusCircle className="w-4 h-4" /> Report an Issue</Link>
      </div>

      {complaints.length === 0 ? (
        <div className="card"><EmptyState title="No complaints yet" description="Report your first civic issue to get started." /></div>
      ) : (
        <div className="card overflow-x-auto p-0">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500 border-b border-slate-100">
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Title</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Priority</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Reported</th>
              </tr>
            </thead>
            <tbody>
              {complaints.map((c) => (
                <tr key={c.id} className="border-b border-slate-50 hover:bg-slate-50 cursor-pointer" onClick={() => (window.location.href = `/complaints/${c.id}`)}>
                  <td className="py-3 px-4 text-slate-400">#{c.id}</td>
                  <td className="py-3 px-4 font-medium text-slate-700">{c.title}</td>
                  <td className="py-3 px-4">{c.category}</td>
                  <td className="py-3 px-4"><PriorityBadge priority={c.priority} /></td>
                  <td className="py-3 px-4"><StatusBadge status={c.status} /></td>
                  <td className="py-3 px-4 text-slate-400">{new Date(c.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
