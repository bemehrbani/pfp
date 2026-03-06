import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import api from '../utils/axiosConfig';
import FormInput from '../components/FormInput';
import FormTextarea from '../components/FormTextarea';
import FormSelect from '../components/FormSelect';
import FormDatePicker from '../components/FormDatePicker';
import LoadingButton from '../components/LoadingButton';
import { CampaignFormData, ApiErrorResponse } from '../types/form';

const CampaignCreate: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [apiError, setApiError] = useState<string>('');

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<CampaignFormData>({
    defaultValues: {
      campaign_type: 'regular',
      status: 'draft',
      target_members: 100,
      target_activities: 50,
      target_twitter_posts: 1000,
      twitter_hashtags: '',
      twitter_accounts: '',
      twitter_storm_schedule: '{}',
      telegram_channel_id: '',
      telegram_group_id: '',
    },
  });

  const campaignType = watch('campaign_type');

  const createCampaignMutation = useMutation({
    mutationFn: async (data: CampaignFormData) => {
      // Parse JSON fields
      const formattedData = {
        ...data,
        target_members: Number(data.target_members),
        target_activities: Number(data.target_activities),
        target_twitter_posts: Number(data.target_twitter_posts),
        telegram_channel_id: data.telegram_channel_id ? Number(data.telegram_channel_id) : null,
        telegram_group_id: data.telegram_group_id ? Number(data.telegram_group_id) : null,
        twitter_storm_schedule: data.twitter_storm_schedule ? JSON.parse(data.twitter_storm_schedule) : null,
      };

      const response = await api.post('/campaigns/', formattedData);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
      navigate('/campaigns');
    },
    onError: (error: any) => {
      if (error.response?.data) {
        const apiError = error.response.data as ApiErrorResponse;
        if (apiError.errors && apiError.errors.length > 0) {
          setApiError(apiError.errors.map(e => e.message).join(', '));
        } else if (apiError.message) {
          setApiError(apiError.message);
        } else {
          setApiError('Failed to create campaign. Please try again.');
        }
      } else {
        setApiError('Network error. Please check your connection and try again.');
      }
    },
  });

  const onSubmit = (data: CampaignFormData) => {
    setApiError('');
    createCampaignMutation.mutate(data);
  };

  const campaignTypeOptions = [
    { value: 'regular', label: 'Regular Campaign' },
    { value: 'twitter_storm', label: 'Twitter Storm' },
    { value: 'hybrid', label: 'Hybrid (Regular + Twitter Storm)' },
  ];

  const statusOptions = [
    { value: 'draft', label: 'Draft' },
    { value: 'active', label: 'Active' },
    { value: 'paused', label: 'Paused' },
    { value: 'completed', label: 'Completed' },
    { value: 'archived', label: 'Archived' },
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Create New Campaign</h1>
        <p className="text-gray-600">Start a new peace campaign and engage volunteers</p>
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
                label="Campaign Name"
                name="name"
                placeholder="Enter campaign name"
                register={register}
                error={errors.name}
                required
                className="md:col-span-2"
              />

              <FormTextarea
                label="Short Description"
                name="short_description"
                placeholder="Brief description for listings (max 500 characters)"
                register={register}
                error={errors.short_description}
                required
                rows={3}
                className="md:col-span-2"
              />

              <FormTextarea
                label="Detailed Description"
                name="description"
                placeholder="Provide detailed information about the campaign"
                register={register}
                error={errors.description}
                required
                rows={6}
                className="md:col-span-2"
              />

              <FormSelect
                label="Campaign Type"
                name="campaign_type"
                options={campaignTypeOptions}
                register={register}
                error={errors.campaign_type}
                required
              />

              <FormSelect
                label="Status"
                name="status"
                options={statusOptions}
                register={register}
                error={errors.status}
                required
              />
            </div>
          </div>

          {/* Goals Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Campaign Goals</h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <FormInput
                label="Target Members"
                name="target_members"
                type="number"
                placeholder="100"
                register={register}
                error={errors.target_members}
                required
                helpText="Target number of core members"
              />

              <FormInput
                label="Target Activities"
                name="target_activities"
                type="number"
                placeholder="50"
                register={register}
                error={errors.target_activities}
                required
                helpText="Target number of activities"
              />

              <FormInput
                label="Target Twitter Posts"
                name="target_twitter_posts"
                type="number"
                placeholder="1000"
                register={register}
                error={errors.target_twitter_posts}
                required={campaignType !== 'regular'}
                disabled={campaignType === 'regular'}
                helpText="Target Twitter posts (for Twitter storms)"
              />
            </div>
          </div>

          {/* Twitter Storm Section (Conditional) */}
          {(campaignType === 'twitter_storm' || campaignType === 'hybrid') && (
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Twitter Storm Settings</h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormInput
                  label="Hashtags"
                  name="twitter_hashtags"
                  placeholder="#PeaceForAll, #StandForPeace (comma-separated)"
                  register={register}
                  error={errors.twitter_hashtags}
                  required={campaignType === 'twitter_storm'}
                  helpText="Comma-separated list of hashtags"
                />

                <FormInput
                  label="Accounts to Mention"
                  name="twitter_accounts"
                  placeholder="@UN, @ICRC (comma-separated)"
                  register={register}
                  error={errors.twitter_accounts}
                  helpText="Comma-separated list of Twitter accounts"
                />

                <FormTextarea
                  label="Storm Schedule (JSON)"
                  name="twitter_storm_schedule"
                  placeholder='{"start_time": "2024-01-01T10:00:00Z", "duration_hours": 24, "peak_times": ["14:00", "20:00"]}'
                  register={register}
                  error={errors.twitter_storm_schedule}
                  rows={4}
                  className="md:col-span-2"
                  helpText="JSON object with Twitter storm schedule"
                />
              </div>
            </div>
          )}

          {/* Telegram Integration */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Telegram Integration</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormInput
                label="Telegram Channel ID"
                name="telegram_channel_id"
                type="number"
                placeholder="1234567890"
                register={register}
                error={errors.telegram_channel_id}
                helpText="Telegram channel ID for announcements"
              />

              <FormInput
                label="Telegram Group ID"
                name="telegram_group_id"
                type="number"
                placeholder="1234567890"
                register={register}
                error={errors.telegram_group_id}
                helpText="Telegram group ID for coordination"
              />
            </div>
          </div>

          {/* Timeline Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 pb-2 border-b">Campaign Timeline</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormDatePicker
                label="Start Date & Time"
                name="start_date"
                register={register}
                error={errors.start_date}
                required
                includeTime
                helpText="Planned start date and time"
              />

              <FormDatePicker
                label="End Date & Time"
                name="end_date"
                register={register}
                error={errors.end_date}
                required
                includeTime
                helpText="Planned end date and time"
              />
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-4 pt-6 border-t">
            <button
              type="button"
              onClick={() => navigate('/campaigns')}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>

            <LoadingButton
              isLoading={createCampaignMutation.isPending}
              loadingText="Creating Campaign..."
              type="submit"
            >
              Create Campaign
            </LoadingButton>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CampaignCreate;