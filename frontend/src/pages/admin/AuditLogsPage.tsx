import React, { useEffect, useState } from "react";
import { ScrollText } from "lucide-react";
import { listAuditLogs } from "../../services/admin";
import { LoadingState } from "../../components/LoadingState";
import { formatDateTime } from "../../utils/format";

export const AuditLogsPage: React.FC = () => {
  const [logs, setLogs] = useState<any[] | null>(null);
  useEffect(() => { listAuditLogs().then(setLogs); }, []);
  if (!logs) return <LoadingState />;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold text-slate-800 flex items-center gap-2"><ScrollText className="w-5 h-5" /> Audit Logs</h1>
      <div className="card overflow-x-auto p-0">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b border-slate-100">
              <th className="py-3 px-4">Time</th><th className="py-3 px-4">Complaint</th><th className="py-3 px-4">Event</th><th className="py-3 px-4">Description</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((l) => (
              <tr key={l.id} className="border-b border-slate-50">
                <td className="py-3 px-4 text-slate-400 whitespace-nowrap">{formatDateTime(l.created_at)}</td>
                <td className="py-3 px-4">{l.complaint_id ? `#${l.complaint_id}` : "—"}</td>
                <td className="py-3 px-4 font-medium">{l.event_type}</td>
                <td className="py-3 px-4 text-slate-500">{l.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
