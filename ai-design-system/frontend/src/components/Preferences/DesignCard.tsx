'use client';

import React, { useState } from 'react';
import Image from 'next/image';

interface DesignCardProps {
  designId: string;
  imageUrl: string;
  craftType: string;
  style: string;
  fusionLevel: number;
  onLike: () => void;
  onSave: () => void;
  onSkip: () => void;
  onComment: (comment: string) => void;
  isLoading?: boolean;
}

export default function DesignCard({
  imageUrl,
  craftType,
  style,
  fusionLevel,
  onLike,
  onSave,
  onSkip,
  onComment,
  isLoading = false,
}: DesignCardProps) {
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [comment, setComment] = useState('');

  const handleCommentSubmit = () => {
    if (comment.trim()) {
      onComment(comment);
      setComment('');
      setShowCommentBox(false);
    }
  };

  return (
    <div className="bg-primary border-2 border-lightbrown rounded-lg overflow-hidden">
      {/* Design Image */}
      <div className="relative aspect-square bg-lightbrown/30">
        <Image
          src={imageUrl}
          alt={`${craftType} ${style} design`}
          fill
          className="object-cover"
        />
      </div>

      {/* Design Info */}
      <div className="p-4 border-t border-lightbrown">
        <div className="flex justify-between items-start mb-3">
          <div>
            <h3 className="font-bold text-blackbrown">
              {craftType.charAt(0).toUpperCase() + craftType.slice(1)} Design
            </h3>
            <p className="text-sm text-lightbrown">
              {style} • {fusionLevel}% Fusion
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2 mb-3">
          <button
            onClick={onLike}
            disabled={isLoading}
            className="flex-1 flex items-center justify-center gap-2 py-2 px-4 bg-lightbrown/30 hover:bg-lightbrown/50 text-blackbrown rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="text-xl">❤️</span>
            <span className="font-medium">Like</span>
          </button>

          <button
            onClick={onSave}
            disabled={isLoading}
            className="flex-1 flex items-center justify-center gap-2 py-2 px-4 bg-lightbrown/30 hover:bg-lightbrown/50 text-blackbrown rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="text-xl">🔖</span>
            <span className="font-medium">Save</span>
          </button>

          <button
            onClick={onSkip}
            disabled={isLoading}
            className="px-4 py-2 bg-lightbrown/30 hover:bg-lightbrown/50 text-blackbrown rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="text-xl">⏭️</span>
          </button>
        </div>

        {/* Comment Section */}
        {showCommentBox ? (
          <div className="space-y-2">
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Add a comment..."
              rows={2}
              className="w-full px-3 py-2 bg-primary border border-lightbrown rounded-lg text-blackbrown placeholder-lightbrown focus:border-secondarybrown focus:outline-none resize-none"
            />
            <div className="flex gap-2">
              <button
                onClick={handleCommentSubmit}
                disabled={isLoading || !comment.trim()}
                className="flex-1 py-2 px-4 bg-secondarybrown text-primary rounded-lg hover:bg-darkbrown transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Post Comment
              </button>
              <button
                onClick={() => {
                  setShowCommentBox(false);
                  setComment('');
                }}
                className="py-2 px-4 bg-lightbrown/30 text-blackbrown rounded-lg hover:bg-lightbrown/50 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
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
  );
}

