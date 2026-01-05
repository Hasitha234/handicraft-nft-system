'use client';

import React, { useState } from 'react';

interface PromptDisplayProps {
  prompts: string[];
}

export default function PromptDisplay({ prompts }: PromptDisplayProps) {
  const [expanded, setExpanded] = useState(false);

  if (prompts.length === 0) {
    return null;
  }

  return (
    <div className="bg-primary border-2 border-lightbrown rounded-lg p-4">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between text-left"
      >
        <h3 className="text-sm font-bold text-blackbrown">
          Generated Prompts ({prompts.length})
        </h3>
        <svg
          className={`w-5 h-5 text-blackbrown transition-transform ${
            expanded ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {expanded && (
        <div className="mt-4 space-y-3">
          {prompts.map((prompt, index) => (
            <div
              key={index}
              className="bg-lightbrown/30 rounded p-3 border border-lightbrown"
            >
              <p className="text-xs font-medium text-blackbrown mb-1">
                Design {index + 1}:
              </p>
              <p className="text-sm text-blackbrown description">{prompt}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

