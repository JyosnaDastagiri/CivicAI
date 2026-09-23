import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { CheckCircle2, PlayCircle, Send } from "lucide-react";
import { getComplaint, acknowledgeComplaint, changeStatus, resolveComplaint, uploadImage } from "../../services/complaints";
import type { ComplaintDetail } from "../../types";
import { StatusBadge, PriorityBadge } from "../../components/StatusBadge";
import { LoadingState } from "../../components/LoadingState";
import { Timeline } from "../../components/Timeline";
import { useToast } from "../../context/ToastContext";
import { apiErrorMessage } from "../../services/api";
import { formatDateTime, timeUntil } from "../../utils/format";

export const OfficerComplaintDetailPage: React.FC = () => {
  const { id } = useParams();
  const [detail, setDetail] = useState<ComplaintDetail | null>(null);
  const [resolutionText, setResolutionText] = useState("");
  const [evidenceFile, setEvidenceFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const { showToast } = useToast();

  const load = () => id && getComplaint(Number(id)).then(setDetail);
  useEffect(() => { load(); }, [id]);

  if (!detail) return <LoadingState />;
  const { complaint, assignment, timeline, location } = detail;

  const doAcknowledge = async () => {
    setBusy(true);
    try {
      await acknowledgeComplaint(complaint.id);
      showToast("Complaint acknowledged", "success");
      load();
    } catch (err) { showToast(apiErrorMessage(err), "error"); } finally { setBusy(false); }
  };

  const startWork = async () => {
    setBusy(true);
    try {
      await changeStatus(complaint.id, "IN_PROGRESS", "Officer started work on the complaint.");
      showToast("Marked as in progress", "success");
      load();
    } catch (err) { showToast(apiErrorMessage(err), "error"); } finally { setBusy(false); }
  };

  const submitResolution = async () => {
    if (!resolutionText.trim()) return showToast("Please describe the resolution.", "error");
    setBusy(true);
    try {
      let evidenceUrl: string | undefined;
      if (evidenceFile) {
        const uploaded = await uploadImage(evidenceFile);
        evidenceUrl = uploaded.url;
      }
      await resolveComplaint(complaint.id, resolutionText, evidenceUrl);
      showToast("Complaint resolved", "success");
      load();
    } catch (err) { showToast(apiErrorMessage(err), "error"); } finally { setBusy(false); }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3 flex-wrap">
        <h1 className="text-xl font-semibold text-slate-800">#{complaint.id} {complaint.title}</h1>
        <StatusBadge status={complaint.status} />
        <PriorityBadge priority={complaint.priority} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <h2 className="font-semibold text-slate-800 mb-2">Description</h2>
            <p className="text-sm text-slate-600">{complaint.description}</p>
            {location?.address && <p className="text-sm text-slate-500 mt-2">📍 {location.address}</p>}
          </div>

          {assignment && !assignment.acknowledged_at && (
            <div className="card border-amber-200 bg-amber-50">
              <h2 className="font-semibold text-amber-800 mb-2">Action required</h2>
              <p className="text-sm text-amber-700 mb-3">Acknowledgement deadline: {formatDateTime(assignment.acknowledgement_deadline)} ({timeUntil(assignment.acknowledgement_deadline)})</p>
              <button className="btn-primary" onClick={doAcknowledge} disabled={busy}>
                <CheckCircle2 className="w-4 h-4" /> Acknowledge Complaint
              </button>
            </div>
          )}

          {assignment?.acknowledged_at && assignment.assignment_status === "ACKNOWLEDGED" && (
            <div className="card">
              <button className="btn-primary" onClick={startWork} disabled={busy}>
                <PlayCircle className="w-4 h-4" /> Start Work
              </button>
            </div>
          )}

          {assignment?.assignment_status === "IN_PROGRESS" && (
            <div className="card">
              <h2 className="font-semibold text-slate-800 mb-2">Submit Resolution</h2>
              <textarea className="input min-h-[100px]" placeholder="Describe how the issue was resolved..." value={resolutionText} onChange={(e) => setResolutionText(e.target.value)} />
              <div className="mt-2">
                <label className="label">Evidence photo (optional)</label>
                <input type="file" accept="image/*" onChange={(e) => e.target.files && setEvidenceFile(e.target.files[0])} />
              </div>
              <button className="btn-primary mt-3" onClick={submitResolution} disabled={busy}>
                <Send className="w-4 h-4" /> Resolve Complaint
              </button>
            </div>
          )}
        </div>

        <div className="space-y-6">
          {assignment && (
            <div className="card">
              <h2 className="font-semibold text-slate-800 mb-2">Assignment</h2>
              <p className="text-sm text-slate-500">Status: <span className="font-medium text-slate-700">{assignment.assignment_status}</span></p>
              {assignment.resolution_deadline && (
                <p className="text-sm text-slate-500 mt-1">Resolution deadline: {formatDateTime(assignment.resolution_deadline)} ({timeUntil(assignment.resolution_deadline)})</p>
              )}
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
