import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../utils/axiosConfig';

const CampaignsPage: React.FC = () => {
  const { data: campaigns, isLoading } = useQuery({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const response = await api.get('/api/campaigns/');
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
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Campaigns</h1>
          <p className="text-gray-600">Manage and join peace campaigns</p>
        </div>
        <Link
          to="/campaigns/create"
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md"
        >
          Create Campaign
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {campaigns?.results?.map((campaign: any) => (
          <div key={campaign.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-800">{campaign.name}</h3>
                  <span className={`inline-block px-2 py-1 text-xs font-semibold rounded-full ${
                    campaign.status === 'active' ? 'bg-green-100 text-green-800' :
                    campaign.status === 'draft' ? 'bg-gray-100 text-gray-800' :
                    campaign.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {campaign.status}
                  </span>
                </div>
                <span className="text-sm font-medium text-gray-500">{campaign.campaign_type}</span>
              </div>

              <p className="text-gray-600 mb-4">{campaign.short_description}</p>

              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-500 mb-1">
                  <span>Progress</span>
                  <span>{campaign.progress_percentage?.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${campaign.progress_percentage || 0}%` }}
                  ></div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="text-center">
                  <p className="text-2xl font-bold text-gray-800">{campaign.current_members}</p>
                  <p className="text-sm text-gray-500">Members</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-gray-800">{campaign.completed_activities}</p>
                  <p className="text-sm text-gray-500">Activities</p>
                </div>
              </div>

              <div className="flex space-x-3">
                <Link
                  to={`/campaigns/${campaign.id}`}
                  className="flex-1 bg-blue-50 hover:bg-blue-100 text-blue-700 font-medium py-2 px-4 rounded-md text-center"
                >
                  View Details
                </Link>
                {campaign.status === 'active' && (
                  <Link
                    to={`/campaigns/${campaign.id}/join`}
                    className="flex-1 bg-green-50 hover:bg-green-100 text-green-700 font-medium py-2 px-4 rounded-md text-center"
                  >
                    Join Campaign
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {(!campaigns || campaigns.results?.length === 0) && (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <h3 className="text-xl font-bold text-gray-800 mb-2">No campaigns yet</h3>
          <p className="text-gray-600 mb-4">Create your first campaign to get started</p>
          <Link
            to="/campaigns/create"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md"
          >
            Create First Campaign
          </Link>
        </div>
      )}
    </div>
  );
};

export default CampaignsPage;