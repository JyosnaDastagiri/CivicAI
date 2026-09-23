import React, { useEffect, useState } from "react";
import { PlusCircle, Building2 } from "lucide-react";
import { listDepartments, createDepartment } from "../../services/admin";
import type { Department } from "../../types";
import { LoadingState } from "../../components/LoadingState";
import { useToast } from "../../context/ToastContext";
import { apiErrorMessage } from "../../services/api";

export const DepartmentsPage: React.FC = () => {
  const [departments, setDepartments] = useState<Department[] | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const { showToast } = useToast();

  const load = () => listDepartments().then(setDepartments);
  useEffect(() => { load(); }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createDepartment({ name, description });
      showToast("Department created", "success");
      setName(""); setDescription("");
      load();
    } catch (err) { showToast(apiErrorMessage(err), "error"); }
  };

  if (!departments) return <LoadingState />;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold text-slate-800 flex items-center gap-2"><Building2 className="w-5 h-5" /> Departments</h1>
      <form onSubmit={submit} className="card flex gap-3">
        <input className="input" placeholder="Department name" required value={name} onChange={(e) => setName(e.target.value)} />
        <input className="input" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button className="btn-primary shrink-0" type="submit"><PlusCircle className="w-4 h-4" /> Add</button>
      </form>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {departments.map((d) => (
          <div key={d.id} className="card">
            <p className="font-medium text-slate-800">{d.name}</p>
            <p className="text-sm text-slate-500">{d.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
