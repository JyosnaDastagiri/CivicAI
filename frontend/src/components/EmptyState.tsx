import React from "react";
import { Inbox } from "lucide-react";

export const EmptyState: React.FC<{ title: string; description?: string; icon?: React.ReactNode }> = ({ title, description, icon }) => (
  <div className="flex flex-col items-center justify-center py-16 text-center text-slate-500">
    {icon || <Inbox className="w-10 h-10 mb-3 text-slate-300" />}
    <p className="font-medium text-slate-600">{title}</p>
    {description && <p className="text-sm mt-1 max-w-sm">{description}</p>}
  </div>
);
