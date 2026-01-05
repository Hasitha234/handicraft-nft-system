'use client';

import React from 'react';

interface StatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

export default function StatsCard({
  title,
  value,
  subtitle,
  icon,
  trend,
}: StatsCardProps) {
  return (
    <div className="bg-primary border-2 border-lightbrown rounded-lg p-6 hover:border-secondarybrown transition-all duration-200">
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-sm text-lightbrown mb-1">{title}</p>
          <h3 className="text-3xl font-bold text-blackbrown">{value}</h3>
          {subtitle && (
            <p className="text-xs text-lightbrown mt-1">{subtitle}</p>
          )}
        </div>
        {icon && <span className="text-3xl">{icon}</span>}
      </div>
      {trend && (
        <div
          className={`text-sm font-medium ${
            trend.isPositive ? 'text-green-600' : 'text-red-600'
          }`}
        >
          {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
        </div>
      )}
    </div>
  );
}

