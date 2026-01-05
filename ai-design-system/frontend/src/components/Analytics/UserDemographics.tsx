'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface UserDemographicsProps {
  userTypes: Record<string, number>;
}

export default function UserDemographics({ userTypes }: UserDemographicsProps) {
  const chartData = Object.entries(userTypes).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
  }));

  if (chartData.length === 0) {
    return (
      <div className="bg-primary border-2 border-lightbrown rounded-lg p-12 text-center">
        <p className="text-lightbrown">No user data available</p>
      </div>
    );
  }

  return (
    <div className="bg-primary border-2 border-lightbrown rounded-lg p-6">
      <h3 className="text-lg font-bold text-blackbrown mb-4">
        User Demographics
      </h3>
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
            label={{ value: 'Users', angle: -90, position: 'insideLeft', fill: '#290E0A' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#F6E7CA',
              border: '1px solid #A28769',
              borderRadius: '8px',
              color: '#290E0A',
            }}
          />
          <Bar
            dataKey="value"
            fill="#693422"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

