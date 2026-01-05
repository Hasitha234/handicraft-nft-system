'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ClassificationResult } from '@/types';

interface ConfidenceChartProps {
  result: ClassificationResult | null;
}

export default function ConfidenceChart({ result }: ConfidenceChartProps) {
  if (!result) {
    return (
      <div className="bg-primary border-2 border-lightbrown rounded-lg p-6 h-64 flex items-center justify-center">
        <p className="text-lightbrown">Upload an image to see confidence chart</p>
      </div>
    );
  }

  const chartData = Object.entries(result.probabilities).map(([name, value]) => {
    const getBarColor = () => {
      switch (name) {
        case 'Traditional':
          return '#693422';
        case 'Fusion':
          return '#471A14';
        case 'Modern':
          return '#290E0A';
        default:
          return '#A28769';
      }
    };
    
    return {
      name,
      confidence: (value * 100).toFixed(1),
      value: value * 100,
      fill: getBarColor(),
    };
  });

  return (
    <div className="bg-primary border-2 border-lightbrown rounded-lg p-6">
      <h3 className="text-xl font-bold text-blackbrown mb-4">Confidence Visualization</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#A28769" opacity={0.3} />
          <XAxis
            dataKey="name"
            stroke="#290E0A"
            fontSize={12}
            fontWeight={500}
          />
          <YAxis
            stroke="#290E0A"
            fontSize={12}
            label={{ value: 'Confidence %', angle: -90, position: 'insideLeft', fill: '#290E0A' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#F6E7CA',
              border: '1px solid #A28769',
              borderRadius: '8px',
              color: '#290E0A',
            }}
            formatter={(value: number) => [`${value}%`, 'Confidence']}
          />
          <Bar
            dataKey="value"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

