import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { getAnalytics } from "../../services/dashboard";
import { LoadingState } from "../../components/LoadingState";

const COLORS = ["#2f75b8", "#f59e0b", "#ef4444", "#10b981", "#6366f1", "#84cc16"];

export const HeadAnalyticsPage: React.FC = () => {
  const [statusData, setStatusData] = useState<any[] | null>(null);
  const [priorityData, setPriorityData] = useState<any[] | null>(null);

  useEffect(() => {
    getAnalytics("status").then((d) => setStatusData(Object.entries(d.byStatus).map(([name, value]) => ({ name, value }))));
    getAnalytics("priority").then((d) => setPriorityData(Object.entries(d.byPriority).map(([name, value]) => ({ name, value }))));
  }, []);

  if (!statusData || !priorityData) return <LoadingState />;

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold text-slate-800">Department Analytics</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Complaints by Status</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={statusData}>
              <XAxis dataKey="name" fontSize={11} interval={0} angle={-20} textAnchor="end" height={60} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill="#2f75b8" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Complaints by Priority</h2>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={priorityData} dataKey="value" nameKey="name" outerRadius={100} label>
                {priorityData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
