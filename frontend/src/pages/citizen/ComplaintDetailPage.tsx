import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { MapPin, ShieldAlert, Copy, Clock } from "lucide-react";
import { getComplaint } from "../../services/complaints";
import type { ComplaintDetail } from "../../types";
import { StatusBadge, PriorityBadge } from "../../components/StatusBadge";
import { LoadingState } from "../../components/LoadingState";
import { Timeline } from "../../components/Timeline";
import { ComplaintMap } from "../../components/ComplaintMap";
import { formatDateTime } from "../../utils/format";

export const ComplaintDetailPage: React.FC = () => {
  const { id } = useParams();
  const [detail, setDetail] = useState<ComplaintDetail | null>(null);

  useEffect(() => {
    if (id) getComplaint(Number(id)).then(setDetail);
  }, [id]);

  if (!detail) return <LoadingState />;
  const { complaint, location, priorityAnalysis, assignment, duplicates, escalations, resolution, timeline, images } = detail;

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-3 flex-wrap">
          <h1 className="text-xl font-semibold text-slate-800">#{complaint.id} {complaint.title}</h1>
          <StatusBadge status={complaint.status} />
          <PriorityBadge priority={complaint.priority} />
        </div>
        <p className="text-sm text-slate-500 mt-1">Reported {formatDateTime(complaint.created_at)}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <h2 className="font-semibold text-slate-800 mb-2">Description</h2>
            <p className="text-sm text-slate-600">{complaint.description}</p>
            <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
              <div><p className="text-slate-400">Category</p><p className="font-medium">{complaint.category}</p></div>
              <div><p className="text-slate-400">Severity</p><p className="font-medium">{complaint.severity}</p></div>
              <div className="flex items-center gap-1"><ShieldAlert className="w-4 h-4 text-amber-500" /><p>{complaint.safety_risk ? "Safety risk" : "No safety risk"}</p></div>
            </div>
            {images.length > 0 && (
              <div className="mt-4 flex gap-2 flex-wrap">
                {images.map((img, i) => (
                  <img key={i} src={img.storage_url} className="w-32 h-32 object-cover rounded-lg border border-slate-200" />
                ))}
              </div>
            )}
          </div>

          {priorityAnalysis && (
            <div className="card">
              <h2 className="font-semibold text-slate-800 mb-2">Priority Explanation</h2>
              <p className="text-sm text-slate-600 mb-3">{priorityAnalysis.explanation}</p>
              <div className="grid grid-cols-5 gap-2 text-xs text-center">
                {[
                  ["Severity", priorityAnalysis.severity_score],
                  ["Safety", priorityAnalysis.safety_score],
                  ["Location", priorityAnalysis.location_score],
                  ["Recurrence", priorityAnalysis.recurrence_score],
                  ["Urgency", priorityAnalysis.urgency_score],
                ].map(([label, score]) => (
                  <div key={label as string} className="rounded-lg bg-slate-50 p-2">
                    <p className="text-slate-400">{label}</p>
                    <p className="font-semibold text-civic-700">{score}</p>
                  </div>
                ))}
              </div>
              <p className="text-sm mt-3">Final Score: <span className="font-semibold">{priorityAnalysis.final_score}/100</span></p>
            </div>
          )}

          {duplicates.length > 0 && (
            <div className="card border-amber-200 bg-amber-50">
              <h2 className="font-semibold text-amber-800 mb-2 flex items-center gap-2"><Copy className="w-4 h-4" /> Similar complaint(s) found nearby</h2>
              {duplicates.map((d, i) => (
                <p key={i} className="text-sm text-amber-700">
                  Complaint #{d.similar_complaint_id} — similarity {Math.round(d.text_similarity * 100)}%, distance {Math.round(d.distance_meters)}m
                </p>
              ))}
            </div>
          )}

          {location && (
            <div className="card">
              <h2 className="font-semibold text-slate-800 mb-2 flex items-center gap-2"><MapPin className="w-4 h-4" /> Location</h2>
              <ComplaintMap complaints={[{ id: complaint.id, title: complaint.title, latitude: location.latitude, longitude: location.longitude, priority: complaint.priority, status: complaint.status }]} height="280px" />
              {location.address && <p className="text-sm text-slate-500 mt-2">{location.address}</p>}
            </div>
          )}

          {resolution && (
            <div className="card border-green-200 bg-green-50">
              <h2 className="font-semibold text-green-800 mb-2">Resolution</h2>
              <p className="text-sm text-green-700">{resolution.description}</p>
              {resolution.evidence_url && <img src={resolution.evidence_url} className="w-40 h-40 object-cover rounded-lg mt-2" />}
              <p className="text-xs text-green-600 mt-1">{formatDateTime(resolution.created_at)}</p>
            </div>
          )}
        </div>

        <div className="space-y-6">
          {assignment && (
            <div className="card">
              <h2 className="font-semibold text-slate-800 mb-2 flex items-center gap-2"><Clock className="w-4 h-4" /> Assignment</h2>
              <p className="text-sm text-slate-500">Status: <span className="font-medium text-slate-700">{assignment.assignment_status}</span></p>
              <p className="text-sm text-slate-500 mt-1">Acknowledgement deadline: {formatDateTime(assignment.acknowledgement_deadline)}</p>
              {assignment.acknowledged_at ? (
                <p className="text-sm text-green-600 mt-1">✓ Received & Acknowledged {formatDateTime(assignment.acknowledged_at)}</p>
              ) : (
                <p className="text-sm text-amber-600 mt-1">Awaiting acknowledgement</p>
              )}
              {assignment.resolution_deadline && <p className="text-sm text-slate-500 mt-1">Resolution deadline: {formatDateTime(assignment.resolution_deadline)}</p>}
            </div>
          )}

          {escalations.length > 0 && (
            <div className="card border-red-200 bg-red-50">
              <h2 className="font-semibold text-red-800 mb-2">Escalations</h2>
              {escalations.map((e, i) => (
                <div key={i} className="mb-2 last:mb-0">
                  <p className="text-sm text-red-700">{e.reason}</p>
                  <p className="text-xs text-red-500">{formatDateTime(e.escalated_at)} — {e.status}</p>
                </div>
              ))}
            </div>
          )}

          <div className="card">
            <h2 className="font-semibold text-slate-800 mb-3">Timeline</h2>
            <Timeline events={timeline} />
          </div>
        </div>
      </div>
    </div>
  );
};
