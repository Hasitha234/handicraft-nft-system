'use client';

import React from 'react';
import { CRAFT_TYPES } from '@/lib/constants';

interface CraftSelectorProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export default function CraftSelector({
  value,
  onChange,
  disabled = false,
}: CraftSelectorProps) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-blackbrown">
        Craft Type
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className="w-full px-4 py-3 bg-primary border-2 border-lightbrown rounded-lg text-blackbrown focus:border-secondarybrown focus:outline-none transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {CRAFT_TYPES.map((craft) => (
          <option key={craft.value} value={craft.value}>
            {craft.label}
          </option>
        ))}
      </select>
    </div>
  );
}



