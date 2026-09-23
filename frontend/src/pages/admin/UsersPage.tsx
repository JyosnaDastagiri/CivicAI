import React, { useEffect, useState } from "react";
import { UserPlus } from "lucide-react";
import { listUsers, createUser, listDepartments, updateUser } from "../../services/admin";
import type { User, Department } from "../../types";
import { LoadingState } from "../../components/LoadingState";
import { useToast } from "../../context/ToastContext";
import { apiErrorMessage } from "../../services/api";

export const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[] | null>(null);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: "", email: "", password: "", role: "OFFICER", department_id: "" });
  const { showToast } = useToast();

  const load = () => listUsers().then(setUsers);
  useEffect(() => {
    load();
    listDepartments().then(setDepartments);
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createUser({ ...form, department_id: form.department_id ? Number(form.department_id) : null });
      showToast("User created", "success");
      setShowForm(false);
      setForm({ name: "", email: "", password: "", role: "OFFICER", department_id: "" });
      load();
    } catch (err) { showToast(apiErrorMessage(err), "error"); }
  };

  const toggleActive = async (u: User) => {
    await updateUser(u.id, { is_active: !u.is_active });
    load();
  };

  if (!users) return <LoadingState />;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-slate-800">Users</h1>
        <button className="btn-primary" onClick={() => setShowForm((s) => !s)}><UserPlus className="w-4 h-4" /> Add User</button>
      </div>

      {showForm && (
        <form onSubmit={submit} className="card grid grid-cols-2 gap-3">
          <input className="input" placeholder="Name" required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <input className="input" placeholder="Email" type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input className="input" placeholder="Password" type="password" required minLength={6} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          <select className="input" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="OFFICER">Officer</option>
            <option value="DEPARTMENT_HEAD">Department Head</option>
            <option value="ADMIN">Admin</option>
            <option value="CITIZEN">Citizen</option>
          </select>
          <select className="input col-span-2" value={form.department_id} onChange={(e) => setForm({ ...form, department_id: e.target.value })}>
            <option value="">No department</option>
            {departments.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
          </select>
          <button className="btn-primary col-span-2" type="submit">Create User</button>
        </form>
      )}

      <div className="card overflow-x-auto p-0">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b border-slate-100">
              <th className="py-3 px-4">Name</th><th className="py-3 px-4">Email</th><th className="py-3 px-4">Role</th><th className="py-3 px-4">Active</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-b border-slate-50">
                <td className="py-3 px-4 font-medium">{u.name}</td>
                <td className="py-3 px-4 text-slate-500">{u.email}</td>
                <td className="py-3 px-4">{u.role.replace("_", " ")}</td>
                <td className="py-3 px-4">
                  <button onClick={() => toggleActive(u)} className={`text-xs rounded-full px-2 py-1 ${u.is_active ? "bg-green-100 text-green-700" : "bg-slate-200 text-slate-500"}`}>
                    {u.is_active ? "Active" : "Inactive"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
