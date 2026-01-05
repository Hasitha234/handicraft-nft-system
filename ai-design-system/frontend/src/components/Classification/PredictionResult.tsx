'use client';

import React from 'react';
import { ClassificationResult } from '@/types';

interface PredictionResultProps {
  result: ClassificationResult | null;
  isLoading?: boolean;
}

export default function PredictionResult({
  result,
  isLoading = false,
}: PredictionResultProps) {
  if (isLoading) {
    return (
      <div className="bg-primary border-2 border-lightbrown rounded-lg p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-lightbrown rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-lightbrown rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  const getClassColor = (className: string) => {
    switch (className) {
      case 'Traditional':
        return 'bg-secondarybrown';
      case 'Fusion':
        return 'bg-darkbrown';
      case 'Modern':
        return 'bg-blackbrown';
      default:
        return 'bg-lightbrown';
    }
  };

  const getClassIcon = (className: string) => {
    switch (className) {
      case 'Traditional':
        return '🏛️';
      case 'Fusion':
        return '🎨';
      case 'Modern':
        return '✨';
      default:
        return '📦';
    }
  };

  return (
    <div className="bg-primary border-2 border-lightbrown rounded-lg p-6 space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-blackbrown">Prediction Result</h3>
        <span className="text-3xl">{getClassIcon(result.predicted_class)}</span>
      </div>

      <div className={`${getClassColor(result.predicted_class)} text-primary rounded-lg p-4 mb-4`}>
        <div className="flex items-center justify-between">
          <span className="text-lg font-medium">{result.predicted_class}</span>
          <span className="text-2xl font-bold">
            {(result.confidence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-medium text-blackbrown mb-2">Confidence Breakdown:</p>
        {Object.entries(result.probabilities).map(([className, probability]) => (
          <div key={className} className="space-y-1">
            <div className="flex justify-between text-sm text-blackbrown mb-1">
              <span>{className}</span>
              <span className="font-medium">{(probability * 100).toFixed(1)}%</span>
            </div>
            <div className="w-full bg-lightbrown rounded-full h-2">
              <div
                className={`${getClassColor(className)} h-2 rounded-full transition-all duration-500`}
                style={{ width: `${probability * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}



