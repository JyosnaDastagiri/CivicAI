import React from "react";
import { Loader2 } from "lucide-react";

export const LoadingState: React.FC<{ label?: string }> = ({ label = "Loading..." }) => (
  <div className="flex flex-col items-center justify-center py-16 text-slate-500">
    <Loader2 className="w-6 h-6 animate-spin mb-2" />
    <span className="text-sm">{label}</span>
  </div>
);
