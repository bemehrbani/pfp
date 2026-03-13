import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../utils/axiosConfig';

const AnalyticsPage: React.FC = () => {
  const { data: analytics, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: async () => {
      const response = await api.get('/api/analytics/');
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
        <h1 className="text-3xl font-bold text-gray-800">Analytics Dashboard</h1>
        <p className="text-gray-600">Track campaign performance and volunteer engagement</p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Campaigns</h3>
          <p className="text-3xl font-bold text-blue-600">{analytics?.total_campaigns || 0}</p>
          <p className="text-gray-500 text-sm mt-2">
            {analytics?.active_campaigns || 0} active
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Volunteers</h3>
          <p className="text-3xl font-bold text-green-600">{analytics?.total_volunteers || 0}</p>
          <p className="text-gray-500 text-sm mt-2">
            {analytics?.active_volunteers || 0} active this month
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Tasks Completed</h3>
          <p className="text-3xl font-bold text-yellow-600">{analytics?.tasks_completed || 0}</p>
          <p className="text-gray-500 text-sm mt-2">
            {analytics?.verification_rate || 0}% verification rate
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Points</h3>
          <p className="text-3xl font-bold text-purple-600">{analytics?.total_points_awarded || 0}</p>
          <p className="text-gray-500 text-sm mt-2">
            Avg. {analytics?.avg_points_per_user || 0} per volunteer
          </p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Campaign Progress */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Campaign Progress</h2>
          <div className="space-y-4">
            {analytics?.campaign_progress?.map((campaign: any) => (
              <div key={campaign.id}>
                <div className="flex justify-between text-sm text-gray-500 mb-1">
                  <span>{campaign.name}</span>
                  <span>{campaign.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${campaign.progress}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Task Types Distribution */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Task Types Distribution</h2>
          <div className="space-y-4">
            {analytics?.task_types?.map((type: any) => (
              <div key={type.name}>
                <div className="flex justify-between text-sm text-gray-500 mb-1">
                  <span>{type.name}</span>
                  <span>{type.count} tasks ({type.percentage}%)</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: `${type.percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Activity Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-800">Recent Activity</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Volunteer
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Action
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Campaign
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Time
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {analytics?.recent_activity?.map((activity: any, index: number) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {activity.volunteer_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          @{activity.volunteer_username}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      activity.action_type === 'task_complete'
                        ? 'bg-green-100 text-green-800'
                        : activity.action_type === 'campaign_join'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {activity.action_type.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {activity.campaign_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {activity.time_ago}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;