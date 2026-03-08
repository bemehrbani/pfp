import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import api from '../utils/axiosConfig';
import FormInput from '../components/FormInput';
import FormTextarea from '../components/FormTextarea';
import FormSelect from '../components/FormSelect';
import FormDatePicker from '../components/FormDatePicker';
import LoadingButton from '../components/LoadingButton';
import { TaskFormData, KeyTweetFormData, ApiErrorResponse } from '../types/form';

interface Campaign {
  id: number;
  name: string;
  status: string;
}

const TaskCreate: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [apiError, setApiError] = useState<string>('');
  const [selectedCampaign, setSelectedCampaign] = useState<number | null>(null);
  const [keyTweets, setKeyTweets] = useState<KeyTweetFormData[]>([]);

  // Fetch campaigns for dropdown
  const { data: campaigns, isLoading: isLoadingCampaigns } = useQuery({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const response = await api.get('/campaigns/');
      return response.data.results as Campaign[];
    },
  });

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<TaskFormData>({
    defaultValues: {
      task_type: 'twitter_post',
      assignment_type: 'first_come',
      points: 10,
      estimated_time: 15,
      max_assignments: 1,
      target_url: '',
      hashtags: '',
      mentions: '',
      image_url: '',
    },
  });

  const taskType = watch('task_type');
  const campaignId = watch('campaign');

  // Update selected campaign when form value changes
  useEffect(() => {
    if (campaignId) {
      setSelectedCampaign(Number(campaignId));
    }
  }, [campaignId]);

  const createTaskMutation = useMutation({
    mutationFn: async (data: TaskFormData) => {
      // Format numeric fields
      const formattedData = {
        ...data,
        campaign: Number(data.campaign),
        points: Number(data.points),
        estimated_time: Number(data.estimated_time),
        max_assignments: Number(data.max_assignments),
        hashtags: data.hashtags || '',
        mentions: data.mentions || '',
        target_url: data.target_url || '',
        image_url: data.image_url || '',
        key_tweets: data.task_type === 'twitter_comment' ? keyTweets.filter(kt => kt.tweet_url) : [],
      };

      const response = await api.post('/tasks/', formattedData);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      navigate('/tasks');
    },
    onError: (error: any) => {
      if (error.response?.data) {
        const apiError = error.response.data as ApiErrorResponse;
        if (apiError.errors && apiError.errors.length > 0) {
          setApiError(apiError.errors.map(e => e.message).join(', '));
        } else if (apiError.message) {
          setApiError(apiError.message);
        } else {
          setApiError('Failed to create task. Please try again.');
        }
      } else {
        setApiError('Network error. Please check your connection and try again.');
      }
    },
  });

  const onSubmit = (data: TaskFormData) => {
    setApiError('');
    createTaskMutation.mutate(data);
  };

  const taskTypeOptions = [
    { value: 'twitter_post', label: 'Twitter Post' },
    { value: 'twitter_retweet', label: 'Twitter Retweet' },
    { value: 'twitter_comment', label: 'Twitter Comment' },
    { value: 'twitter_like', label: 'Twitter Like' },
    { value: 'telegram_share', label: 'Telegram Share' },
    { value: 'telegram_invite', label: 'Telegram Invite' },
    { value: 'content_creation', label: 'Content Creation' },
    { value: 'research', label: 'Research' },
    { value: 'other', label: 'Other' },
  ];

  const addKeyTweet = () => {
    setKeyTweets([...keyTweets, { tweet_url: '', author_name: '', author_handle: '', description: '' }]);
  };

  const removeKeyTweet = (index: number) => {
    setKeyTweets(keyTweets.filter((_, i) => i !== index));
  };

  const updateKeyTweet = (index: number, field: keyof KeyTweetFormData, value: string) => {
    const updated = [...keyTweets];
    updated[index] = { ...updated[index], [field]: value };
    setKeyTweets(updated);
  };

  const assignmentTypeOptions = [
    { value: 'first_come', label: 'First Come, First Served' },
    { value: 'manual', label: 'Manual Assignment' },
    { value: 'automatic', label: 'Automatic Assignment' },
  ];

  const campaignOptions = campaigns?.map((campaign: Campaign) => ({
    value: campaign.id.toString(),
    label: `${campaign.name} (${campaign.status})`,
  })) || [];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Create New Task</h1>
        <p className="text-gray-600">Add a new task to engage volunteers in your campaign</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        {apiError && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-700">{apiError}</p>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)}>
          {/* Basic Information Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Basic Information</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormInput
                label="Task Title"
                name="title"
                placeholder="Enter task title"
                register={register}
                error={errors.title}
                required
                className="md:col-span-2"
              />

              <FormTextarea
                label="Description"
                name="description"
                placeholder="Describe what needs to be done"
                register={register}
                error={errors.description}
                required
                rows={4}
                className="md:col-span-2"
              />

              <FormTextarea
                label="Instructions"
                name="instructions"
                placeholder="Step-by-step instructions for volunteers"
                register={register}
                error={errors.instructions}
                required
                rows={6}
                className="md:col-span-2"
              />

              <FormSelect
                label="Task Type"
                name="task_type"
                options={taskTypeOptions}
                register={register}
                error={errors.task_type}
                required
              />

              <FormSelect
                label="Assignment Type"
                name="assignment_type"
                options={assignmentTypeOptions}
                register={register}
                error={errors.assignment_type}
                required
              />

              <FormSelect
                label="Campaign"
                name="campaign"
                options={campaignOptions}
                register={register}
                error={errors.campaign}
                required
                disabled={isLoadingCampaigns}
                placeholder={isLoadingCampaigns ? "Loading campaigns..." : "Select a campaign"}
              />
            </div>
          </div>

          {/* Requirements & Rewards Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Requirements & Rewards</h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <FormInput
                label="Points Awarded"
                name="points"
                type="number"
                placeholder="10"
                register={register}
                error={errors.points}
                required
                helpText="Points volunteers earn for completion"
              />

              <FormInput
                label="Estimated Time (minutes)"
                name="estimated_time"
                type="number"
                placeholder="15"
                register={register}
                error={errors.estimated_time}
                required
                helpText="Estimated time to complete"
              />

              <FormInput
                label="Max Assignments"
                name="max_assignments"
                type="number"
                placeholder="1"
                register={register}
                error={errors.max_assignments}
                required
                helpText="Maximum volunteers who can complete"
              />
            </div>
          </div>

          {/* Social Media & URLs Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Social Media & URLs</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormInput
                label="Target URL"
                name="target_url"
                type="url"
                placeholder="https://twitter.com/status/123456"
                register={register}
                error={errors.target_url}
                required={taskType === 'twitter_retweet' || taskType === 'twitter_like'}
                helpText="URL for retweet, like, or reference"
              />

              <FormInput
                label="Image URL"
                name="image_url"
                type="url"
                placeholder="https://example.com/image.jpg"
                register={register}
                error={errors.image_url}
                helpText="URL of image to use (if applicable)"
              />

              <FormInput
                label="Hashtags"
                name="hashtags"
                placeholder="#PeaceForAll, #StandForPeace (comma-separated)"
                register={register}
                error={errors.hashtags}
                helpText="Comma-separated list of hashtags"
              />

              <FormInput
                label="Accounts to Mention"
                name="mentions"
                placeholder="@UN, @ICRC (comma-separated)"
                register={register}
                error={errors.mentions}
                helpText="Comma-separated list of accounts"
              />
            </div>
          </div>

          {/* Key Tweets Section (for twitter_comment) */}
          {taskType === 'twitter_comment' && (
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Key Tweets to Comment On</h2>
              <p className="text-gray-600 mb-4 text-sm">Add tweets from key figures that volunteers should comment on.</p>

              {keyTweets.map((kt, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-4 mb-4 border border-gray-200">
                  <div className="flex justify-between items-center mb-3">
                    <span className="font-medium text-gray-700">Tweet #{index + 1}</span>
                    <button
                      type="button"
                      onClick={() => removeKeyTweet(index)}
                      className="text-red-500 hover:text-red-700 text-sm font-medium"
                    >
                      ✕ Remove
                    </button>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Tweet URL *</label>
                      <input
                        type="url"
                        value={kt.tweet_url}
                        onChange={(e) => updateKeyTweet(index, 'tweet_url', e.target.value)}
                        placeholder="https://x.com/UN/status/123456789"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Author Name *</label>
                      <input
                        type="text"
                        value={kt.author_name}
                        onChange={(e) => updateKeyTweet(index, 'author_name', e.target.value)}
                        placeholder="United Nations"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Author Handle *</label>
                      <input
                        type="text"
                        value={kt.author_handle}
                        onChange={(e) => updateKeyTweet(index, 'author_handle', e.target.value)}
                        placeholder="@UN"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                      <input
                        type="text"
                        value={kt.description}
                        onChange={(e) => updateKeyTweet(index, 'description', e.target.value)}
                        placeholder="Brief description of the tweet content"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                      />
                    </div>
                  </div>
                </div>
              ))}

              <button
                type="button"
                onClick={addKeyTweet}
                className="w-full py-2 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-400 hover:text-blue-600 transition-colors text-sm font-medium"
              >
                + Add Key Tweet
              </button>
            </div>
          )}

          {/* Availability Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Availability</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormDatePicker
                label="Available From"
                name="available_from"
                register={register}
                error={errors.available_from}
                includeTime
                helpText="When task becomes available (optional)"
              />

              <FormDatePicker
                label="Available Until"
                name="available_until"
                register={register}
                error={errors.available_until}
                includeTime
                helpText="When task expires (optional)"
              />
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-4 pt-6 border-t">
            <button
              type="button"
              onClick={() => navigate('/tasks')}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>

            <LoadingButton
              isLoading={createTaskMutation.isPending}
              loadingText="Creating Task..."
              type="submit"
              disabled={!selectedCampaign}
            >
              Create Task
            </LoadingButton>
          </div>

          {!selectedCampaign && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="text-yellow-700 text-sm">
                Please select a campaign before creating a task.
              </p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default TaskCreate;