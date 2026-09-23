import React, { useEffect, useState } from "react";
import { Bell, CheckCheck } from "lucide-react";
import { listNotifications, markNotificationRead } from "../../services/notifications";
import type { Notification } from "../../types";
import { LoadingState } from "../../components/LoadingState";
import { EmptyState } from "../../components/EmptyState";
import { formatDateTime } from "../../utils/format";

export const NotificationsPage: React.FC = () => {
  const [items, setItems] = useState<Notification[] | null>(null);

  const load = () => listNotifications().then(setItems);
  useEffect(() => { load(); }, []);

  if (!items) return <LoadingState />;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold text-slate-800 flex items-center gap-2"><Bell className="w-5 h-5" /> Notifications</h1>
      {items.length === 0 ? (
        <div className="card"><EmptyState title="No notifications yet" /></div>
      ) : (
        <div className="card divide-y divide-slate-100 p-0">
          {items.map((n) => (
            <div key={n.id} className={`p-4 flex items-start justify-between gap-3 ${!n.is_read ? "bg-civic-50/50" : ""}`}>
              <div>
                <p className="text-sm font-medium text-slate-700">{n.title}</p>
                <p className="text-sm text-slate-500">{n.message}</p>
                <p className="text-xs text-slate-400 mt-1">{formatDateTime(n.created_at)}</p>
              </div>
              {!n.is_read && (
                <button onClick={() => markNotificationRead(n.id).then(load)} className="text-civic-600 hover:text-civic-800" title="Mark as read">
                  <CheckCheck className="w-4 h-4" />
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
