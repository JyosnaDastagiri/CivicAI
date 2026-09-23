import React from "react";
import { CheckCircle2, Circle, AlertTriangle, ArrowUpRight } from "lucide-react";

interface TimelineEvent { status: string; description: string | null; created_at: string; }

const ESCALATION_EVENTS = ["ACKNOWLEDGEMENT_DEADLINE_EXCEEDED", "RESOLUTION_DEADLINE_EXCEEDED"];
const ESCALATED_EVENTS = ["COMPLAINT_ESCALATED"];

function humanize(status: string): string {
  return status
    .replace(/_/g, " ")
    .toLowerCase()
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export const Timeline: React.FC<{ events: TimelineEvent[] }> = ({ events }) => {
  if (events.length === 0) {
    return <p className="text-sm text-slate-400">No timeline events yet.</p>;
  }
  return (
    <ol className="relative border-l border-slate-200 ml-2">
      {events.map((e, idx) => {
        const isWarning = ESCALATION_EVENTS.includes(e.status);
        const isEscalated = ESCALATED_EVENTS.includes(e.status);
        const Icon = isWarning ? AlertTriangle : isEscalated ? ArrowUpRight : CheckCircle2;
        const color = isWarning ? "text-amber-500" : isEscalated ? "text-red-500" : "text-green-600";
        return (
          <li key={idx} className="mb-5 ml-4">
            <span className={`absolute -left-[9px] flex items-center justify-center w-4 h-4 rounded-full bg-white ${color}`}>
              <Icon className="w-4 h-4" />
            </span>
            <p className="text-sm font-medium text-slate-700">{humanize(e.status)}</p>
            {e.description && <p className="text-xs text-slate-500 mt-0.5">{e.description}</p>}
            <time className="text-xs text-slate-400">{new Date(e.created_at).toLocaleString()}</time>
          </li>
        );
      })}
    </ol>
  );
};
