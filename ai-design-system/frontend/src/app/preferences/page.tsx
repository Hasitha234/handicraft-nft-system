'use client';

import React, { useState, useEffect } from 'react';
import UserRegistration from '@/components/Preferences/UserRegistration';
import DesignCard from '@/components/Preferences/DesignCard';
import InteractionButtons from '@/components/Preferences/InteractionButtons';
import CommentBox from '@/components/Preferences/CommentBox';
import Button from '@/components/Shared/Button';
import LoadingSpinner from '@/components/Shared/LoadingSpinner';
import ErrorMessage from '@/components/Shared/ErrorMessage';
import { preferencesAPI } from '@/lib/api';
import { Design } from '@/types';

export default function PreferencesPage() {
  const [isRegistered, setIsRegistered] = useState(false);
  const [userId, setUserId] = useState<number | null>(null);
  const [currentDesignIndex, setCurrentDesignIndex] = useState(0);
  const [designs, setDesigns] = useState<Design[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState('');

  useEffect(() => {
    loadDesigns();
  }, []);

  const loadDesigns = async () => {
    try {
      const response = await preferencesAPI.getDesigns();
      if (response.designs && response.designs.length > 0) {
        setDesigns(response.designs);
      } else {
        // Mock data for development
        setDesigns([
          {
            id: '1',
            filename: 'design_001.png',
            craft_type: 'mask',
            style: 'fusion',
            fusion_level: 60,
            prompt: 'Fusion mask design',
          },
          {
            id: '2',
            filename: 'design_002.png',
            craft_type: 'batik',
            style: 'traditional',
            fusion_level: 20,
            prompt: 'Traditional batik design',
          },
        ]);
      }
    } catch (err) {
      console.error('Failed to load designs:', err);
      // Use mock data on error
      setDesigns([
        {
          id: '1',
          filename: 'design_001.png',
          craft_type: 'mask',
          style: 'fusion',
          fusion_level: 60,
          prompt: 'Fusion mask design',
        },
      ]);
    }
  };

  const handleRegister = async (userData: {
    user_type: string;
    age_group: string;
    gender: string;
    country: string;
  }) => {
    setIsLoading(true);
    setError('');

    try {
      const response = await preferencesAPI.register(userData);
      setUserId(response.user_id);
      setIsRegistered(true);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to register. Please try again.'
      );
      // For development, allow continuing with mock userId
      setUserId(1);
      setIsRegistered(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInteraction = async (
    action: 'like' | 'save' | 'comment' | 'skip',
    comment?: string
  ) => {
    if (!userId || designs.length === 0) return;

    const currentDesign = designs[currentDesignIndex];
    setFeedbackMessage('');

    try {
      await preferencesAPI.interact({
        user_id: userId,
        design_id: currentDesign.id,
        action,
        comment: comment || '',
      });

      setFeedbackMessage(`✅ ${action.charAt(0).toUpperCase() + action.slice(1)}d!`);
      setTimeout(() => setFeedbackMessage(''), 2000);
      setShowCommentBox(false);
    } catch (err) {
      console.error('Failed to save interaction:', err);
      // Still show feedback for UX even if API fails
      setFeedbackMessage(`✅ ${action.charAt(0).toUpperCase() + action.slice(1)}d!`);
      setTimeout(() => setFeedbackMessage(''), 2000);
      setShowCommentBox(false);
    }
  };

  const handleNext = () => {
    if (designs.length > 0) {
      setCurrentDesignIndex((prev) => (prev + 1) % designs.length);
      setShowCommentBox(false);
      setFeedbackMessage('');
    }
  };

  const currentDesign = designs[currentDesignIndex];

  if (!isRegistered) {
    return (
      <div className="min-h-screen bg-primary">
        <div className="containerpadding container mx-auto py-8 md:py-12">
          <div className="max-w-2xl mx-auto">
            {error && (
              <div className="mb-6">
                <ErrorMessage message={error} />
              </div>
            )}
            <UserRegistration onSubmit={handleRegister} isLoading={isLoading} />
          </div>
        </div>
      </div>
    );
  }

  if (designs.length === 0) {
    return (
      <div className="min-h-screen bg-primary">
        <div className="containerpadding container mx-auto py-8 md:py-12">
          <div className="max-w-2xl mx-auto text-center">
            <p className="text-lg text-blackbrown mb-4">
              No designs available yet.
            </p>
            <p className="text-lightbrown">
              Please generate designs first using the Design Generator.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-primary">
      <div className="containerpadding container mx-auto py-8 md:py-12">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="title text-blackbrown mb-2">
            Design Gallery
          </h1>
          <p className="description text-blackbrown">
            Browse and rate AI-generated designs. Your feedback helps artisans create better products.
          </p>
        </div>

        {/* Design Counter */}
        <div className="text-center mb-6">
          <p className="text-sm text-lightbrown">
            Design {currentDesignIndex + 1} of {designs.length}
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-2xl mx-auto">
          {/* Design Card */}
          <div className="bg-primary border-2 border-lightbrown rounded-lg overflow-hidden mb-6">
            {/* Design Image */}
            <div className="relative aspect-square bg-lightbrown/30">
              <img
                src={`https://via.placeholder.com/600x600/693422/F6E7CA?text=${currentDesign.craft_type}+${currentDesign.style}`}
                alt={`${currentDesign.craft_type} ${currentDesign.style} design`}
                className="w-full h-full object-cover"
              />
            </div>

            {/* Design Info */}
            <div className="p-4 border-t border-lightbrown">
              <div className="mb-4">
                <h3 className="font-bold text-blackbrown text-lg mb-1">
                  {currentDesign.craft_type.charAt(0).toUpperCase() +
                    currentDesign.craft_type.slice(1)}{' '}
                  Design
                </h3>
                <p className="text-sm text-lightbrown">
                  {currentDesign.style.charAt(0).toUpperCase() +
                    currentDesign.style.slice(1)}{' '}
                  • {currentDesign.fusion_level}% Fusion
                </p>
              </div>

              {/* Feedback Message */}
              {feedbackMessage && (
                <div className="mb-4 p-2 bg-lightbrown/30 rounded text-center text-blackbrown font-medium">
                  {feedbackMessage}
                </div>
              )}

              {/* Interaction Buttons */}
              <InteractionButtons
                onLike={() => handleInteraction('like')}
                onSave={() => handleInteraction('save')}
                onSkip={() => handleInteraction('skip')}
                isLoading={isLoading}
              />

              {/* Comment Section */}
              <div className="mt-4">
                {showCommentBox ? (
                  <CommentBox
                    onSubmit={(comment) => handleInteraction('comment', comment)}
                    onCancel={() => setShowCommentBox(false)}
                    isLoading={isLoading}
                  />
                ) : (
                  <button
                    onClick={() => setShowCommentBox(true)}
                    className="w-full py-2 px-4 bg-lightbrown/30 hover:bg-lightbrown/50 text-blackbrown rounded-lg transition-colors text-left"
                  >
                    💬 Add a comment...
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Next Button */}
          <Button onClick={handleNext} className="w-full" size="lg">
            Next Design →
          </Button>
        </div>
      </div>
    </div>
  );
}
