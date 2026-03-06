import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../utils/axiosConfig';

const DashboardPage: React.FC = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const response = await api.get('/analytics/dashboard-stats/');
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-600">Welcome to People for Peace Campaign Manager</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Active Campaigns</h3>
          <p className="text-3xl font-bold text-blue-600">{stats?.active_campaigns || 0}</p>
          <Link to="/campaigns" className="text-blue-500 hover:text-blue-700 text-sm mt-2 inline-block">
            View all →
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">My Tasks</h3>
          <p className="text-3xl font-bold text-green-600">{stats?.my_tasks || 0}</p>
          <Link to="/tasks" className="text-blue-500 hover:text-blue-700 text-sm mt-2 inline-block">
            View tasks →
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Points Earned</h3>
          <p className="text-3xl font-bold text-yellow-600">{stats?.points_earned || 0}</p>
          <p className="text-gray-500 text-sm mt-2">Keep up the good work!</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Volunteers</h3>
          <p className="text-3xl font-bold text-purple-600">{stats?.total_volunteers || 0}</p>
          <p className="text-gray-500 text-sm mt-2">Active this month</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/campaigns/create"
            className="bg-blue-50 hover:bg-blue-100 p-4 rounded-lg border border-blue-200 text-blue-700 font-medium text-center"
          >
            Create New Campaign
          </Link>
          <Link
            to="/tasks/available"
            className="bg-green-50 hover:bg-green-100 p-4 rounded-lg border border-green-200 text-green-700 font-medium text-center"
          >
            Find Available Tasks
          </Link>
          <Link
            to="/analytics"
            className="bg-purple-50 hover:bg-purple-100 p-4 rounded-lg border border-purple-200 text-purple-700 font-medium text-center"
          >
            View Analytics
          </Link>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Recent Activity</h2>
        <div className="space-y-4">
          {stats?.recent_activity?.length > 0 ? (
            stats.recent_activity.map((activity: any, index: number) => (
              <div key={index} className="border-b border-gray-100 pb-3 last:border-0">
                <p className="text-gray-700">{activity.description}</p>
                <p className="text-gray-500 text-sm">{activity.time}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500 text-center py-4">No recent activity</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;