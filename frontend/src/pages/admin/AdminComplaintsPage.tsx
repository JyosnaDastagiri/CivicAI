import React, { useEffect, useState } from "react";
import { listComplaints } from "../../services/complaints";
import type { Complaint } from "../../types";
import { StatusBadge, PriorityBadge } from "../../components/StatusBadge";
import { LoadingState } from "../../components/LoadingState";
import { ComplaintMap } from "../../components/ComplaintMap";
import { getComplaint } from "../../services/complaints";

export const AdminComplaintsPage: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[] | null>(null);
  const [mapPoints, setMapPoints] = useState<any[]>([]);

  useEffect(() => {
    listComplaints().then(async (items) => {
      setComplaints(items);
      const points: any[] = [];
      for (const c of items.slice(0, 30)) {
        try {
          const d = await getComplaint(c.id);
          if (d.location) points.push({ id: c.id, title: c.title, latitude: d.location.latitude, longitude: d.location.longitude, priority: c.priority, status: c.status });
        } catch { /* ignore */ }
      }
      setMapPoints(points);
    });
  }, []);

  if (!complaints) return <LoadingState />;

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold text-slate-800">All Complaints</h1>
      {mapPoints.length > 0 && (
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Complaint Locations</h2>
          <ComplaintMap complaints={mapPoints} />
        </div>
      )}
      <div className="card overflow-x-auto p-0">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b border-slate-100">
              <th className="py-3 px-4">ID</th><th className="py-3 px-4">Title</th><th className="py-3 px-4">Category</th>
              <th className="py-3 px-4">Priority</th><th className="py-3 px-4">Status</th>
            </tr>
          </thead>
          <tbody>
            {complaints.map((c) => (
              <tr key={c.id} className="border-b border-slate-50 hover:bg-slate-50 cursor-pointer" onClick={() => (window.location.href = `/complaints/${c.id}`)}>
                <td className="py-3 px-4 text-slate-400">#{c.id}</td>
                <td className="py-3 px-4 font-medium">{c.title}</td>
                <td className="py-3 px-4">{c.category}</td>
                <td className="py-3 px-4"><PriorityBadge priority={c.priority} /></td>
                <td className="py-3 px-4"><StatusBadge status={c.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
