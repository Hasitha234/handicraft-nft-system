'use client';

import React, { useState, useEffect } from 'react';
import StatsCard from '@/components/Analytics/StatsCard';
import StyleChart from '@/components/Analytics/StyleChart';
import UserDemographics from '@/components/Analytics/UserDemographics';
import Button from '@/components/Shared/Button';
import LoadingSpinner from '@/components/Shared/LoadingSpinner';
import ErrorMessage from '@/components/Shared/ErrorMessage';
import { analyticsAPI } from '@/lib/api';
import { Analytics } from '@/types';

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  const loadAnalytics = async () => {
    setIsLoading(true);
    setError('');

    try {
      const data = await analyticsAPI.getAnalytics();
      setAnalytics(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to load analytics. Please try again.'
      );
      // Use mock data for development
      setAnalytics({
        total_interactions: 45,
        total_users: 12,
        total_likes: 28,
        likes_by_style: {
          Traditional: 8,
          Fusion: 15,
          Modern: 5,
        },
        user_types: {
          Tourist: 5,
          Local: 4,
          Expat: 3,
        },
        popular_fusion_levels: {
          50: 8,
          60: 7,
          40: 5,
          70: 4,
          30: 4,
        },
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-primary">
        <div className="containerpadding container mx-auto py-8 md:py-12">
          <div className="flex items-center justify-center min-h-[400px]">
            <LoadingSpinner size="lg" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-primary">
      <div className="containerpadding container mx-auto py-8 md:py-12">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="title text-blackbrown mb-2">Analytics Dashboard</h1>
            <p className="description text-blackbrown">
              Insights and trends from user preference data
            </p>
          </div>
          <Button onClick={loadAnalytics} variant="outline">
            🔄 Refresh
          </Button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6">
            <ErrorMessage message={error} />
          </div>
        )}

        {analytics ? (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
              <StatsCard
                title="Total Interactions"
                value={analytics.total_interactions}
                subtitle="All user actions"
                icon="📊"
              />
              <StatsCard
                title="Total Users"
                value={analytics.total_users}
                subtitle="Registered users"
                icon="👥"
              />
              <StatsCard
                title="Total Likes"
                value={analytics.total_likes}
                subtitle="Designs liked"
                icon="❤️"
              />
              <StatsCard
                title="Engagement Rate"
                value={
                  analytics.total_users > 0
                    ? `${Math.round(
                        (analytics.total_likes / analytics.total_users) * 10
                      )}%`
                    : '0%'
                }
                subtitle="Likes per user"
                icon="📈"
              />
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8 mb-8">
              <StyleChart data={analytics.likes_by_style} />
              <UserDemographics userTypes={analytics.user_types} />
            </div>

            {/* Popular Fusion Levels */}
            {Object.keys(analytics.popular_fusion_levels).length > 0 && (
              <div className="bg-primary border-2 border-lightbrown rounded-lg p-6">
                <h3 className="text-lg font-bold text-blackbrown mb-4">
                  Popular Fusion Levels
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  {Object.entries(analytics.popular_fusion_levels)
                    .sort((a, b) => b[1] - a[1])
                    .map(([level, count]) => (
                      <div
                        key={level}
                        className="bg-lightbrown/30 border border-lightbrown rounded-lg p-4 text-center"
                      >
                        <div className="text-2xl font-bold text-secondarybrown mb-1">
                          {level}%
                        </div>
                        <div className="text-sm text-blackbrown">
                          {count} {count === 1 ? 'like' : 'likes'}
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="bg-primary border-2 border-lightbrown rounded-lg p-12 text-center">
            <p className="text-lg text-blackbrown mb-2">No analytics data available</p>
            <p className="text-lightbrown">
              Start collecting user preferences to see insights here.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
