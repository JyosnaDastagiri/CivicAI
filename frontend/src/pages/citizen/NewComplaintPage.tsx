import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, Sparkles, MapPin, FileEdit, ShieldAlert, ListChecks, Send, CheckCircle2, ImageOff } from "lucide-react";
import { LocationPicker } from "../../components/LocationPicker";
import { useToast } from "../../context/ToastContext";
import { apiErrorMessage } from "../../services/api";
import { analyzeImage, createComplaint, generateComplaintText, uploadImage } from "../../services/complaints";
import { CATEGORIES } from "../../utils/format";

const STEPS = [
  "Upload Image", "Description", "Location", "AI Analysis",
  "Generated Complaint", "Review & Edit", "Submit",
];

export const NewComplaintPage: React.FC = () => {
  const [step, setStep] = useState(0);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [description, setDescription] = useState("");
  const [lat, setLat] = useState(17.3850);
  const [lon, setLon] = useState(78.4867);
  const [address, setAddress] = useState("");
  const [analysis, setAnalysis] = useState<any>(null);
  const [generated, setGenerated] = useState<any>(null);
  const [title, setTitle] = useState("");
  const [finalDescription, setFinalDescription] = useState("");
  const [category, setCategory] = useState("");
  const [severity, setSeverity] = useState("MEDIUM");
  const [safetyRisk, setSafetyRisk] = useState(false);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState<any>(null);

  const { showToast } = useToast();
  const navigate = useNavigate();

  const onFileSelected = (file: File) => {
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file));
  };

  const goNext = () => setStep((s) => Math.min(s + 1, STEPS.length - 1));
  const goBack = () => setStep((s) => Math.max(s - 1, 0));

  const runAnalysis = async () => {
    setLoading(true);
    try {
      let url = imageUrl;
      if (imageFile && !url) {
        const uploaded = await uploadImage(imageFile);
        url = uploaded.url;
        setImageUrl(url);
      }
      const result = await analyzeImage(url || "no-image-provided", description);
      setAnalysis(result);
      setCategory(result.category);
      setSeverity(result.severity);
      setSafetyRisk(result.safetyRisk);
      goNext();
    } catch (err) {
      showToast(apiErrorMessage(err), "error");
    } finally {
      setLoading(false);
    }
  };

  const runGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateComplaintText(description, category, severity, safetyRisk, address || undefined);
      setGenerated(result);
      setTitle(result.title);
      setFinalDescription(result.description);
      goNext();
    } catch (err) {
      showToast(apiErrorMessage(err), "error");
    } finally {
      setLoading(false);
    }
  };

  const submit = async () => {
    setLoading(true);
    try {
      const complaint = await createComplaint({
        title, description: finalDescription, category, severity, safety_risk: safetyRisk,
        location: { latitude: lat, longitude: lon, address: address || undefined },
        image_url: imageUrl || undefined,
      });
      setSubmitted(complaint);
      showToast("Complaint submitted successfully!", "success");
      goNext();
    } catch (err) {
      showToast(apiErrorMessage(err), "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-xl font-semibold text-slate-800">Report a Civic Issue</h1>

      {/* Stepper header */}
      <div className="flex items-center gap-1 overflow-x-auto pb-2">
        {STEPS.map((label, idx) => (
          <div key={label} className="flex items-center gap-1 shrink-0">
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-medium ${
              idx < step ? "bg-green-600 text-white" : idx === step ? "bg-civic-600 text-white" : "bg-slate-200 text-slate-500"
            }`}>
              {idx < step ? <CheckCircle2 className="w-4 h-4" /> : idx + 1}
            </div>
            <span className={`text-xs ${idx === step ? "text-civic-700 font-medium" : "text-slate-400"}`}>{label}</span>
            {idx < STEPS.length - 1 && <div className="w-4 h-px bg-slate-200 mx-1" />}
          </div>
        ))}
      </div>

      <div className="card">
        {step === 0 && (
          <div>
            <h2 className="font-semibold text-slate-800 flex items-center gap-2 mb-3"><Upload className="w-5 h-5 text-civic-600" /> Upload an image of the issue</h2>
            <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-300 rounded-xl h-56 cursor-pointer hover:bg-slate-50">
              {imagePreview ? (
                <img src={imagePreview} className="h-full object-contain rounded-xl" />
              ) : (
                <div className="flex flex-col items-center text-slate-400">
                  <ImageOff className="w-10 h-10 mb-2" />
                  <span className="text-sm">Click to select a JPG, PNG, or WEBP image</span>
                </div>
              )}
              <input type="file" accept="image/jpeg,image/png,image/webp" className="hidden" onChange={(e) => e.target.files && onFileSelected(e.target.files[0])} />
            </label>
            <p className="text-xs text-slate-400 mt-2">You can also skip this step and describe the issue in text only.</p>
            <div className="flex justify-end mt-4"><button className="btn-primary" onClick={goNext}>Next</button></div>
          </div>
        )}

        {step === 1 && (
          <div>
            <h2 className="font-semibold text-slate-800 flex items-center gap-2 mb-3"><FileEdit className="w-5 h-5 text-civic-600" /> Describe the issue</h2>
            <textarea
              className="input min-h-[120px]"
              placeholder="e.g. There is a very big pothole near the college entrance and bikes are almost falling into it."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            <div className="flex justify-between mt-4">
              <button className="btn-secondary" onClick={goBack}>Back</button>
              <button className="btn-primary" disabled={description.trim().length < 5} onClick={goNext}>Next</button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div>
            <h2 className="font-semibold text-slate-800 flex items-center gap-2 mb-3"><MapPin className="w-5 h-5 text-civic-600" /> Select the location</h2>
            <LocationPicker latitude={lat} longitude={lon} onChange={(la, lo) => { setLat(la); setLon(lo); }} />
            <div className="mt-3">
              <label className="label">Address / landmark (optional)</label>
              <input className="input" value={address} onChange={(e) => setAddress(e.target.value)} placeholder="e.g. Near college main gate" />
            </div>
            <div className="flex justify-between mt-4">
              <button className="btn-secondary" onClick={goBack}>Back</button>
              <button className="btn-primary" onClick={runAnalysis} disabled={loading}>
                <Sparkles className="w-4 h-4" /> {loading ? "Analyzing..." : "Run AI Analysis"}
              </button>
            </div>
          </div>
        )}

        {step === 3 && analysis && (
          <div>
            <h2 className="font-semibold text-slate-800 flex items-center gap-2 mb-3"><Sparkles className="w-5 h-5 text-civic-600" /> AI Analysis Result</h2>
            {analysis.aiMode === "demo" && (
              <span className="inline-block text-xs bg-amber-100 text-amber-700 rounded-full px-2 py-1 mb-3">Demo AI Mode</span>
            )}
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><p className="text-slate-400">Category</p><p className="font-medium">{analysis.category}</p></div>
              <div><p className="text-slate-400">Severity</p><p className="font-medium">{analysis.severity}</p></div>
              <div><p className="text-slate-400">Safety Risk</p><p className="font-medium">{analysis.safetyRisk ? "Yes" : "No"}</p></div>
              <div><p className="text-slate-400">Confidence</p><p className="font-medium">{Math.round((analysis.confidence || 0) * 100)}%</p></div>
            </div>
            <p className="text-sm text-slate-600 mt-3">{analysis.description}</p>
            <div className="flex justify-between mt-4">
              <button className="btn-secondary" onClick={goBack}>Back</button>
              <button className="btn-primary" onClick={runGenerate} disabled={loading}>
                <FileEdit className="w-4 h-4" /> {loading ? "Generating..." : "Generate Complaint"}
              </button>
            </div>
          </div>
        )}

        {step === 4 && generated && (
          <div>
            <h2 className="font-semibold text-slate-800 flex items-center gap-2 mb-3"><FileEdit className="w-5 h-5 text-civic-600" /> Generated Complaint</h2>
            <p className="text-sm font-medium text-slate-700">{title}</p>
            <p className="text-sm text-slate-600 mt-2">{finalDescription}</p>
            <div className="flex justify-between mt-4">
              <button className="btn-secondary" onClick={goBack}>Back</button>
              <button className="btn-primary" onClick={goNext}>Review & Edit</button>
            </div>
          </div>
        )}

        {step === 5 && (
          <div>
            <h2 className="font-semibold text-slate-800 flex items-center gap-2 mb-3"><ShieldAlert className="w-5 h-5 text-civic-600" /> Review & Edit</h2>
            <div className="space-y-3">
              <div>
                <label className="label">Title</label>
                <input className="input" value={title} onChange={(e) => setTitle(e.target.value)} />
              </div>
              <div>
                <label className="label">Description</label>
                <textarea className="input min-h-[100px]" value={finalDescription} onChange={(e) => setFinalDescription(e.target.value)} />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="label">Category</label>
                  <select className="input" value={category} onChange={(e) => setCategory(e.target.value)}>
                    {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <label className="label">Severity</label>
                  <select className="input" value={severity} onChange={(e) => setSeverity(e.target.value)}>
                    {["LOW", "MEDIUM", "HIGH", "CRITICAL"].map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
              </div>
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" checked={safetyRisk} onChange={(e) => setSafetyRisk(e.target.checked)} />
                This issue poses a safety risk
              </label>
            </div>
            <div className="flex justify-between mt-4">
              <button className="btn-secondary" onClick={goBack}>Back</button>
              <button className="btn-primary" onClick={submit} disabled={loading}>
                <Send className="w-4 h-4" /> {loading ? "Submitting..." : "Submit Complaint"}
              </button>
            </div>
          </div>
        )}

        {step === 6 && submitted && (
          <div className="text-center py-6">
            <CheckCircle2 className="w-12 h-12 text-green-600 mx-auto mb-3" />
            <h2 className="font-semibold text-slate-800 text-lg">Complaint Submitted!</h2>
            <p className="text-sm text-slate-500 mt-1">
              Your complaint #{submitted.id} was analyzed, checked for duplicates, prioritized as{" "}
              <span className="font-medium">{submitted.priority}</span>, and assigned automatically.
            </p>
            <div className="flex gap-3 justify-center mt-5">
              <button className="btn-secondary" onClick={() => navigate("/complaints")}>
                <ListChecks className="w-4 h-4" /> View My Complaints
              </button>
              <button className="btn-primary" onClick={() => navigate(`/complaints/${submitted.id}`)}>View This Complaint</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
