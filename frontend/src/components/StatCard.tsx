import React from "react";

export const StatCard: React.FC<{ label: string; value: string | number; icon?: React.ReactNode; accent?: string }> = ({ label, value, icon, accent = "text-civic-600" }) => (
  <div className="card flex items-center justify-between">
    <div>
      <p className="text-sm text-slate-500">{label}</p>
      <p className={`text-2xl font-semibold mt-1 ${accent}`}>{value}</p>
    </div>
    {icon && <div className="text-slate-300">{icon}</div>}
  </div>
);
