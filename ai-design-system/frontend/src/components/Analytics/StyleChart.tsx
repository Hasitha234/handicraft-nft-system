'use client';

import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface StyleChartProps {
  data: Record<string, number>;
}

export default function StyleChart({ data }: StyleChartProps) {
  const chartData = Object.entries(data).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
  }));

  const COLORS = {
    Traditional: '#693422',
    Fusion: '#471A14',
    Modern: '#290E0A',
  };

  if (chartData.length === 0) {
    return (
      <div className="bg-primary border-2 border-lightbrown rounded-lg p-12 text-center">
        <p className="text-lightbrown">No data available</p>
      </div>
    );
  }

  return (
    <div className="bg-primary border-2 border-lightbrown rounded-lg p-6">
      <h3 className="text-lg font-bold text-blackbrown mb-4">
        Likes by Style
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) =>
              `${name}: ${(percent * 100).toFixed(0)}%`
            }
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[entry.name as keyof typeof COLORS] || '#A28769'}
              />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#F6E7CA',
              border: '1px solid #A28769',
              borderRadius: '8px',
              color: '#290E0A',
            }}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}



