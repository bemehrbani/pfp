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

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <React.Suspense fallback={<LoadingSpinner />}>
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/campaigns" element={<CampaignsPage />} />
            <Route path="/campaigns/create" element={<CampaignCreatePage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/tasks/create" element={<TaskCreatePage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
          </Routes>
        </main>
      </React.Suspense>
    </div>
  );
}

export default App;