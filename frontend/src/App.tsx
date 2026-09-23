import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import { ProtectedRoute } from "./layouts/ProtectedRoute";
import { AppLayout } from "./layouts/AppLayout";
import { ROLE_HOME } from "./utils/roleHome";

import { LoginPage } from "./pages/auth/LoginPage";
import { RegisterPage } from "./pages/auth/RegisterPage";

import { CitizenDashboard } from "./pages/citizen/CitizenDashboard";
import { ComplaintsListPage } from "./pages/citizen/ComplaintsListPage";
import { NewComplaintPage } from "./pages/citizen/NewComplaintPage";
import { ComplaintDetailPage } from "./pages/citizen/ComplaintDetailPage";
import { NotificationsPage } from "./pages/citizen/NotificationsPage";
import { ProfilePage } from "./pages/citizen/ProfilePage";

import { OfficerDashboard } from "./pages/officer/OfficerDashboard";
import { OfficerComplaintsPage } from "./pages/officer/OfficerComplaintsPage";
import { OfficerComplaintDetailPage } from "./pages/officer/OfficerComplaintDetailPage";

import { HeadDashboard } from "./pages/head/HeadDashboard";
import { HeadComplaintsPage } from "./pages/head/HeadComplaintsPage";
import { HeadEscalationsPage } from "./pages/head/HeadEscalationsPage";
import { HeadAnalyticsPage } from "./pages/head/HeadAnalyticsPage";

import { AdminDashboard } from "./pages/admin/AdminDashboard";
import { UsersPage } from "./pages/admin/UsersPage";
import { DepartmentsPage } from "./pages/admin/DepartmentsPage";
import { AdminComplaintsPage } from "./pages/admin/AdminComplaintsPage";
import { AdminEscalationsPage } from "./pages/admin/AdminEscalationsPage";
import { AdminAnalyticsPage } from "./pages/admin/AdminAnalyticsPage";
import { SettingsPage } from "./pages/admin/SettingsPage";
import { AuditLogsPage } from "./pages/admin/AuditLogsPage";

const HomeRedirect: React.FC = () => {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;
  return <Navigate to={ROLE_HOME[user.role]} replace />;
};

const App: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/" element={<HomeRedirect />} />

      <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
        {/* Citizen */}
        <Route path="/dashboard" element={<ProtectedRoute roles={["CITIZEN"]}><CitizenDashboard /></ProtectedRoute>} />
        <Route path="/complaints" element={<ProtectedRoute roles={["CITIZEN"]}><ComplaintsListPage /></ProtectedRoute>} />
        <Route path="/complaints/new" element={<ProtectedRoute roles={["CITIZEN"]}><NewComplaintPage /></ProtectedRoute>} />
        <Route path="/complaints/:id" element={<ComplaintDetailPage />} />
        <Route path="/notifications" element={<NotificationsPage />} />
        <Route path="/profile" element={<ProtectedRoute roles={["CITIZEN"]}><ProfilePage /></ProtectedRoute>} />

        {/* Officer */}
        <Route path="/officer/dashboard" element={<ProtectedRoute roles={["OFFICER"]}><OfficerDashboard /></ProtectedRoute>} />
        <Route path="/officer/complaints" element={<ProtectedRoute roles={["OFFICER"]}><OfficerComplaintsPage /></ProtectedRoute>} />
        <Route path="/officer/complaints/:id" element={<ProtectedRoute roles={["OFFICER"]}><OfficerComplaintDetailPage /></ProtectedRoute>} />

        {/* Department Head */}
        <Route path="/head/dashboard" element={<ProtectedRoute roles={["DEPARTMENT_HEAD"]}><HeadDashboard /></ProtectedRoute>} />
        <Route path="/head/complaints" element={<ProtectedRoute roles={["DEPARTMENT_HEAD"]}><HeadComplaintsPage /></ProtectedRoute>} />
        <Route path="/head/escalations" element={<ProtectedRoute roles={["DEPARTMENT_HEAD"]}><HeadEscalationsPage /></ProtectedRoute>} />
        <Route path="/head/analytics" element={<ProtectedRoute roles={["DEPARTMENT_HEAD"]}><HeadAnalyticsPage /></ProtectedRoute>} />

        {/* Admin */}
        <Route path="/admin/dashboard" element={<ProtectedRoute roles={["ADMIN"]}><AdminDashboard /></ProtectedRoute>} />
        <Route path="/admin/users" element={<ProtectedRoute roles={["ADMIN"]}><UsersPage /></ProtectedRoute>} />
        <Route path="/admin/departments" element={<ProtectedRoute roles={["ADMIN"]}><DepartmentsPage /></ProtectedRoute>} />
        <Route path="/admin/complaints" element={<ProtectedRoute roles={["ADMIN"]}><AdminComplaintsPage /></ProtectedRoute>} />
        <Route path="/admin/escalations" element={<ProtectedRoute roles={["ADMIN"]}><AdminEscalationsPage /></ProtectedRoute>} />
        <Route path="/admin/analytics" element={<ProtectedRoute roles={["ADMIN"]}><AdminAnalyticsPage /></ProtectedRoute>} />
        <Route path="/admin/settings" element={<ProtectedRoute roles={["ADMIN"]}><SettingsPage /></ProtectedRoute>} />
        <Route path="/admin/audit-logs" element={<ProtectedRoute roles={["ADMIN"]}><AuditLogsPage /></ProtectedRoute>} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  </BrowserRouter>
);

export default App;
