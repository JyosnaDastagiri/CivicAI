import React, { useEffect, useState } from "react";
import { Settings as SettingsIcon, Save } from "lucide-react";
import { listSettings, updateSetting } from "../../services/admin";
import type { SystemSetting } from "../../types";
import { LoadingState } from "../../components/LoadingState";
import { useToast } from "../../context/ToastContext";
import { apiErrorMessage } from "../../services/api";

export const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<SystemSetting[] | null>(null);
  const [values, setValues] = useState<Record<string, string>>({});
  const { showToast } = useToast();

  const load = () => listSettings().then((s) => {
    setSettings(s);
    setValues(Object.fromEntries(s.map((x) => [x.key, x.value])));
  });
  useEffect(() => { load(); }, []);

  const save = async (key: string) => {
    try {
      await updateSetting(key, values[key]);
      showToast(`${key} updated`, "success");
      load();
    } catch (err) { showToast(apiErrorMessage(err), "error"); }
  };

  if (!settings) return <LoadingState />;

  return (
    <div className="space-y-4 max-w-3xl">
      <h1 className="text-xl font-semibold text-slate-800 flex items-center gap-2"><SettingsIcon className="w-5 h-5" /> System Settings</h1>
      <div className="card divide-y divide-slate-100 p-0">
        {settings.map((s) => (
          <div key={s.key} className="p-4 flex items-center justify-between gap-4">
            <div className="flex-1">
              <p className="text-sm font-medium text-slate-700">{s.key}</p>
              <p className="text-xs text-slate-400">{s.description}</p>
            </div>
            <input
              className="input w-40"
              value={values[s.key] ?? ""}
              onChange={(e) => setValues({ ...values, [s.key]: e.target.value })}
            />
            <button className="btn-secondary" onClick={() => save(s.key)}><Save className="w-4 h-4" /></button>
          </div>
        ))}
      </div>
    </div>
  );
};
