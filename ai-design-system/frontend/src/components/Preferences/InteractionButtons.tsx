'use client';

import React from 'react';

interface InteractionButtonsProps {
  onLike: () => void;
  onSave: () => void;
  onSkip: () => void;
  isLoading?: boolean;
}

export default function InteractionButtons({
  onLike,
  onSave,
  onSkip,
  isLoading = false,
}: InteractionButtonsProps) {
  return (
    <div className="flex items-center gap-2">
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
        aria-label="Skip design"
      >
        <span className="text-xl">⏭️</span>
      </button>
    </div>
  );
}



