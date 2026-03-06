import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../utils/axiosConfig';

const TasksPage: React.FC = () => {
  const [filter, setFilter] = useState('all');

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks', filter],
    queryFn: async () => {
      const url = filter === 'available'
        ? '/tasks/available/'
        : filter === 'my-tasks'
        ? '/tasks/my-assignments/'
        : '/tasks/';
      const response = await api.get(url);
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
        <h1 className="text-3xl font-bold text-gray-800">Tasks</h1>
        <p className="text-gray-600">Find and complete campaign tasks</p>
      </div>

      {/* Filter Tabs */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="flex space-x-4">
          {['all', 'available', 'my-tasks', 'completed'].map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-4 py-2 rounded-md font-medium ${
                filter === tab
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {tab.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Tasks Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tasks?.results?.map((task: any) => (
          <div key={task.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-800">{task.title}</h3>
                  <span className={`inline-block px-2 py-1 text-xs font-semibold rounded-full mt-2 ${
                    task.task_type === 'twitter_post' ? 'bg-blue-100 text-blue-800' :
                    task.task_type === 'twitter_retweet' ? 'bg-green-100 text-green-800' :
                    task.task_type === 'telegram_share' ? 'bg-purple-100 text-purple-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {task.task_type.replace('_', ' ')}
                  </span>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-yellow-600">{task.points}</p>
                  <p className="text-sm text-gray-500">points</p>
                </div>
              </div>

              <p className="text-gray-600 mb-4">{task.description?.substring(0, 100)}...</p>

              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-500 mb-1">
                  <span>Campaign</span>
                  <span>{task.campaign_name}</span>
                </div>
                <div className="flex justify-between text-sm text-gray-500 mb-1">
                  <span>Estimated Time</span>
                  <span>{task.estimated_time} min</span>
                </div>
                {task.available_slots !== undefined && (
                  <div className="flex justify-between text-sm text-gray-500">
                    <span>Available Slots</span>
                    <span>{task.available_slots}</span>
                  </div>
                )}
              </div>

              <div className="flex space-x-3">
                <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md">
                  View Details
                </button>
                {filter === 'available' && task.available_slots > 0 && (
                  <button className="flex-1 bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-md">
                    Claim Task
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {(!tasks || tasks.results?.length === 0) && (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <h3 className="text-xl font-bold text-gray-800 mb-2">No tasks found</h3>
          <p className="text-gray-600 mb-4">
            {filter === 'available'
              ? 'No tasks available at the moment. Check back later!'
              : filter === 'my-tasks'
              ? 'You have no assigned tasks.'
              : 'No tasks have been created yet.'}
          </p>
          {filter !== 'available' && (
            <button
              onClick={() => setFilter('available')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md"
            >
              Find Available Tasks
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default TasksPage;