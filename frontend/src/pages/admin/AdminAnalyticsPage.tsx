import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from "recharts";
import { getAnalytics } from "../../services/dashboard";
import { LoadingState } from "../../components/LoadingState";

const COLORS = ["#2f75b8", "#f59e0b", "#ef4444", "#10b981", "#6366f1", "#84cc16", "#ec4899"];

export const AdminAnalyticsPage: React.FC = () => {
  const [byCategory, setByCategory] = useState<any[] | null>(null);
  const [byDept, setByDept] = useState<any[] | null>(null);
  const [byStatus, setByStatus] = useState<any[] | null>(null);
  const [byPriority, setByPriority] = useState<any[] | null>(null);
  const [monthly, setMonthly] = useState<any[] | null>(null);

  useEffect(() => {
    getAnalytics("complaints").then((d) => {
      setByCategory(Object.entries(d.byCategory).map(([name, value]) => ({ name, value })));
      setMonthly(Object.entries(d.monthlyTrend).sort().map(([name, value]) => ({ name, value })));
    });
    getAnalytics("departments").then((d) => setByDept(Object.entries(d.complaintsByDepartment).map(([name, value]) => ({ name, value }))));
    getAnalytics("status").then((d) => setByStatus(Object.entries(d.byStatus).map(([name, value]) => ({ name, value }))));
    getAnalytics("priority").then((d) => setByPriority(Object.entries(d.byPriority).map(([name, value]) => ({ name, value }))));
  }, []);

  if (!byCategory || !byDept || !byStatus || !byPriority || !monthly) return <LoadingState />;

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold text-slate-800">Analytics</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Complaints by Category</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={byCategory}>
              <XAxis dataKey="name" fontSize={10} interval={0} angle={-25} textAnchor="end" height={70} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill="#2f75b8" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Complaints by Department</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={byDept}>
              <XAxis dataKey="name" fontSize={10} interval={0} angle={-25} textAnchor="end" height={70} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Status Overview</h2>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={byStatus} dataKey="value" nameKey="name" outerRadius={100} label>
                {byStatus.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Priority Distribution</h2>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={byPriority} dataKey="value" nameKey="name" outerRadius={100} label>
                {byPriority.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="card lg:col-span-2">
          <h2 className="font-semibold text-slate-800 mb-3">Monthly Complaint Trend</h2>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={monthly}>
              <XAxis dataKey="name" fontSize={11} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#2f75b8" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
