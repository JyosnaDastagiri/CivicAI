import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Building2, UserPlus } from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import { apiErrorMessage } from "../../services/api";

export const RegisterPage: React.FC = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await register(name, email, password);
      showToast("Registration successful!", "success");
      navigate("/dashboard");
    } catch (err) {
      showToast(apiErrorMessage(err), "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md">
        <div className="flex items-center justify-center gap-2 mb-6">
          <Building2 className="w-7 h-7 text-civic-600" />
          <span className="text-xl font-bold text-civic-800">CivicAI</span>
        </div>
        <div className="card">
          <h1 className="text-lg font-semibold text-slate-800 mb-1">Create a citizen account</h1>
          <p className="text-sm text-slate-500 mb-5">Report civic issues and track their resolution.</p>
          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="label">Full name</label>
              <input className="input" required value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div>
              <label className="label">Email</label>
              <input className="input" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div>
              <label className="label">Password</label>
              <input className="input" type="password" minLength={6} required value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
            <button className="btn-primary w-full" disabled={loading} type="submit">
              <UserPlus className="w-4 h-4" /> {loading ? "Creating account..." : "Create account"}
            </button>
          </form>
          <p className="text-sm text-slate-500 mt-4 text-center">
            Already have an account? <Link to="/login" className="text-civic-600 font-medium">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
};
