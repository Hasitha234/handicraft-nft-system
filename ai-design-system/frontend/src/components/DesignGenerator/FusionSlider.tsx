'use client';

import React from 'react';

interface FusionSliderProps {
  value: number;
  onChange: (value: number) => void;
  disabled?: boolean;
}

export default function FusionSlider({
  value,
  onChange,
  disabled = false,
}: FusionSliderProps) {
  const getFusionLabel = (level: number) => {
    if (level < 30) return 'Traditional';
    if (level < 70) return 'Fusion';
    return 'Modern';
  };

  const getFusionColor = (level: number) => {
    if (level < 30) return 'bg-secondarybrown';
    if (level < 70) return 'bg-darkbrown';
    return 'bg-blackbrown';
  };

  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <label className="block text-sm font-medium text-blackbrown">
          Fusion Level
        </label>
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-blackbrown">{value}%</span>
          <span className={`px-3 py-1 rounded text-xs font-medium text-primary ${getFusionColor(value)}`}>
            {getFusionLabel(value)}
          </span>
        </div>
      </div>
      
      <input
        type="range"
        min="0"
        max="100"
        step="10"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        disabled={disabled}
        className="w-full h-2 bg-lightbrown rounded-lg appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        style={{
          background: `linear-gradient(to right, #693422 0%, #693422 ${value}%, #A28769 ${value}%, #A28769 100%)`,
        }}
      />
      
      <div className="flex justify-between text-xs text-lightbrown">
        <span>0% Traditional</span>
        <span>50% Balanced</span>
        <span>100% Modern</span>
      </div>
    </div>
  );
}

