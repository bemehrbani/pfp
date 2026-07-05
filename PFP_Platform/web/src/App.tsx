import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Pages
const LoginPage = React.lazy(() => import('./pages/Login'));
const DashboardPage = React.lazy(() => import('./pages/Dashboard'));
const CampaignsPage = React.lazy(() => import('./pages/Campaigns'));
const CampaignCreatePage = React.lazy(() => import('./pages/CampaignCreate'));
const TasksPage = React.lazy(() => import('./pages/Tasks'));
const TaskCreatePage = React.lazy(() => import('./pages/TaskCreate'));
const AnalyticsPage = React.lazy(() => import('./pages/Analytics'));

// Components
const Navigation = React.lazy(() => import('./components/Navigation'));
const LoadingSpinner = React.lazy(() => import('./components/LoadingSpinner'));
const ProtectedRoute = React.lazy(() => import('./components/ProtectedRoute'));

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <React.Suspense fallback={<LoadingSpinner />}>
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
            <Route path="/campaigns" element={<ProtectedRoute><CampaignsPage /></ProtectedRoute>} />
            <Route path="/campaigns/create" element={<ProtectedRoute><CampaignCreatePage /></ProtectedRoute>} />
            <Route path="/tasks" element={<ProtectedRoute><TasksPage /></ProtectedRoute>} />
            <Route path="/tasks/create" element={<ProtectedRoute><TaskCreatePage /></ProtectedRoute>} />
            <Route path="/analytics" element={<ProtectedRoute><AnalyticsPage /></ProtectedRoute>} />
          </Routes>
        </main>
      </React.Suspense>
    </div>
  );
}

export default App;