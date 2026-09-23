import React, { useEffect, useState } from "react";
import { AlertTriangle, CheckCircle2 } from "lucide-react";
import { listEscalations, acknowledgeEscalation } from "../../services/admin";
import { LoadingState } from "../../components/LoadingState";
import { EmptyState } from "../../components/EmptyState";
import { formatDateTime } from "../../utils/format";
import { useToast } from "../../context/ToastContext";

export const HeadEscalationsPage: React.FC = () => {
  const [items, setItems] = useState<any[] | null>(null);
  const { showToast } = useToast();

  const load = () => listEscalations().then(setItems);
  useEffect(() => { load(); }, []);

  if (!items) return <LoadingState />;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold text-slate-800 flex items-center gap-2"><AlertTriangle className="w-5 h-5 text-red-600" /> Escalations</h1>
      {items.length === 0 ? (
        <div className="card"><EmptyState title="No escalations" description="No complaints have been escalated to you." /></div>
      ) : (
        <div className="space-y-3">
          {items.map((e) => (
            <div key={e.id} className="card flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-700">Complaint #{e.complaint_id}</p>
                <p className="text-sm text-slate-500">{e.reason}</p>
                <p className="text-xs text-slate-400 mt-1">{formatDateTime(e.escalated_at)} — {e.status}</p>
              </div>
              {e.status === "OPEN" && (
                <button
                  className="btn-secondary"
                  onClick={() => acknowledgeEscalation(e.id).then(() => { showToast("Escalation acknowledged", "success"); load(); })}
                >
                  <CheckCircle2 className="w-4 h-4" /> Acknowledge
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
