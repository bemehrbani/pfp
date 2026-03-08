// Form types for PFP Campaign Manager

export interface CampaignFormData {
  name: string;
  description: string;
  short_description: string;
  campaign_type: 'regular' | 'twitter_storm' | 'hybrid';
  status: 'draft' | 'active' | 'paused' | 'completed' | 'archived';
  target_members: number;
  target_activities: number;
  target_twitter_posts: number;
  twitter_hashtags: string;
  twitter_accounts: string;
  twitter_storm_schedule: string; // JSON string
  telegram_channel_id: string;
  telegram_group_id: string;
  start_date: string;
  end_date: string;
}

export interface KeyTweetFormData {
  tweet_url: string;
  author_name: string;
  author_handle: string;
  description: string;
}

export interface TaskFormData {
  title: string;
  description: string;
  instructions: string;
  task_type: 'twitter_post' | 'twitter_retweet' | 'twitter_comment' | 'twitter_like' | 'telegram_share' | 'telegram_invite' | 'content_creation' | 'research' | 'other';
  assignment_type: 'first_come' | 'manual' | 'automatic';
  campaign: number;
  points: number;
  estimated_time: number;
  max_assignments: number;
  target_url: string;
  hashtags: string;
  mentions: string;
  image_url: string;
  key_tweets?: KeyTweetFormData[];
  available_from: string;
  available_until: string;
}

export interface FormError {
  field: string;
  message: string;
}

export interface ApiErrorResponse {
  errors?: FormError[];
  message?: string;
  [key: string]: any;
}