'use client';

import React, { useState } from 'react';

interface CommentBoxProps {
  onSubmit: (comment: string) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

export default function CommentBox({
  onSubmit,
  onCancel,
  isLoading = false,
}: CommentBoxProps) {
  const [comment, setComment] = useState('');

  const handleSubmit = () => {
    if (comment.trim()) {
      onSubmit(comment);
      setComment('');
    }
  };

  return (
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
          onClick={handleSubmit}
          disabled={isLoading || !comment.trim()}
          className="flex-1 py-2 px-4 bg-secondarybrown text-primary rounded-lg hover:bg-darkbrown transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Post Comment
        </button>
        <button
          onClick={() => {
            onCancel();
            setComment('');
          }}
          className="py-2 px-4 bg-lightbrown/30 text-blackbrown rounded-lg hover:bg-lightbrown/50 transition-colors"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}



