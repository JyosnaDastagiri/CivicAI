import React from "react";
import { UserCircle } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  if (!user) return null;
  return (
    <div className="max-w-lg space-y-4">
      <h1 className="text-xl font-semibold text-slate-800 flex items-center gap-2"><UserCircle className="w-5 h-5" /> Profile</h1>
      <div className="card space-y-3">
        <div><p className="text-xs text-slate-400">Name</p><p className="text-sm font-medium">{user.name}</p></div>
        <div><p className="text-xs text-slate-400">Email</p><p className="text-sm font-medium">{user.email}</p></div>
        <div><p className="text-xs text-slate-400">Role</p><p className="text-sm font-medium">{user.role.replace("_", " ")}</p></div>
      </div>
    </div>
  );
};
