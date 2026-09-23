import React, { useEffect, useState } from "react";
import { AlertTriangle } from "lucide-react";
import { listEscalations } from "../../services/admin";
import { LoadingState } from "../../components/LoadingState";
import { EmptyState } from "../../components/EmptyState";
import { formatDateTime } from "../../utils/format";

export const AdminEscalationsPage: React.FC = () => {
  const [items, setItems] = useState<any[] | null>(null);
  useEffect(() => { listEscalations().then(setItems); }, []);
  if (!items) return <LoadingState />;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold text-slate-800 flex items-center gap-2"><AlertTriangle className="w-5 h-5 text-red-600" /> All Escalations</h1>
      {items.length === 0 ? (
        <div className="card"><EmptyState title="No escalations recorded" /></div>
      ) : (
        <div className="space-y-3">
          {items.map((e) => (
            <div key={e.id} className="card">
              <p className="text-sm font-medium text-slate-700">Complaint #{e.complaint_id}</p>
              <p className="text-sm text-slate-500">{e.reason}</p>
              <p className="text-xs text-slate-400 mt-1">{formatDateTime(e.escalated_at)} — {e.status}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
