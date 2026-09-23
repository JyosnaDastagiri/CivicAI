import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Building2, LogIn } from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import { apiErrorMessage } from "../../services/api";
import { ROLE_HOME } from "../../utils/roleHome";

const DEMO_ACCOUNTS = [
  { label: "Admin", email: "admin@civicai.demo" },
  { label: "Department Head", email: "roads.head@civicai.demo" },
  { label: "Officer", email: "roads.officer@civicai.demo" },
  { label: "Citizen", email: "citizen@civicai.demo" },
];

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const user = await login(email, password);
      showToast("Welcome back!", "success");
      navigate(ROLE_HOME[user.role]);
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
          <h1 className="text-lg font-semibold text-slate-800 mb-1">Sign in</h1>
          <p className="text-sm text-slate-500 mb-5">Access the civic complaint management platform.</p>
          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="label">Email</label>
              <input className="input" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
            </div>
            <div>
              <label className="label">Password</label>
              <input className="input" type="password" required value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
            </div>
            <button className="btn-primary w-full" disabled={loading} type="submit">
              <LogIn className="w-4 h-4" /> {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>
          <p className="text-sm text-slate-500 mt-4 text-center">
            No account? <Link to="/register" className="text-civic-600 font-medium">Register as citizen</Link>
          </p>
        </div>

        <div className="card mt-4">
          <p className="text-xs font-medium text-slate-500 mb-2">Demo accounts (password: Demo@123)</p>
          <div className="grid grid-cols-2 gap-2">
            {DEMO_ACCOUNTS.map((a) => (
              <button
                key={a.email}
                type="button"
                onClick={() => { setEmail(a.email); setPassword("Demo@123"); }}
                className="text-xs text-left rounded-lg border border-slate-200 px-3 py-2 hover:bg-slate-50"
              >
                <span className="font-medium block">{a.label}</span>
                <span className="text-slate-400">{a.email}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
