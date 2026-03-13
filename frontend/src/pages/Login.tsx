import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import api from '../utils/axiosConfig';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const loginMutation = useMutation({
    mutationFn: async (credentials: { username: string; otp_code: string }) => {
      const response = await api.post('/api/auth/otp-login/', credentials);
      return response.data;
    },
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      navigate('/');
    },
    onError: (error: any) => {
      setError(error.response?.data?.error || 'Login failed');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    loginMutation.mutate({ username, otp_code: otpCode });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">People for Peace</h1>
          <p className="text-gray-600 mt-2">Campaign Manager Dashboard</p>
        </div>

        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <p className="text-sm text-blue-800">
            <strong>How to log in:</strong> Send <code className="bg-blue-100 px-1 rounded">/dashboard</code> to{' '}
            <a
              href="https://t.me/PeopleForPeaceBot"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline hover:text-blue-800"
            >
              @PeopleForPeaceBot
            </a>{' '}
            on Telegram to get your login code.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
              Telegram Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. @username"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="otp-code">
              Login Code
            </label>
            <input
              id="otp-code"
              type="text"
              inputMode="numeric"
              pattern="[0-9]{6}"
              maxLength={6}
              value={otpCode}
              onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
              placeholder="6-digit code from bot"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-center text-2xl tracking-widest font-mono"
              required
            />
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loginMutation.isPending || otpCode.length !== 6}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md focus:outline-none focus:shadow-outline disabled:opacity-50"
          >
            {loginMutation.isPending ? 'Verifying...' : 'Log In'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>Only campaign managers and admins can access this dashboard.</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;