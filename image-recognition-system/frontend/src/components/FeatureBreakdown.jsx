import React from 'react';

const FeatureBreakdown = ({ scores }) => {
  if (!scores) return null;

  const features = [
    { key: 'geometric', label: 'Shape/Structure', color: 'bg-blue-500' },
    { key: 'color', label: 'Color', color: 'bg-purple-500' },
    { key: 'pattern', label: 'Pattern', color: 'bg-yellow-500' },
    { key: 'clip', label: 'Semantic', color: 'bg-gray-500' },
  ];

  return (
    <div className="mt-4 space-y-3">
      <h4 className="text-sm font-semibold text-gray-700 mb-2">Feature Similarity:</h4>
      {features.map((feature) => {
        const score = scores[feature.key];
        if (score === undefined) return null;
        
        const percentage = (score * 100).toFixed(1);
        
        return (
          <div key={feature.key} className="space-y-1">
            <div className="flex justify-between text-xs">
              <span className="text-gray-600">{feature.label}</span>
              <span className="font-medium text-gray-800">{percentage}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`${feature.color} h-2 rounded-full transition-all duration-300`}
                style={{ width: `${percentage}%` }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default FeatureBreakdown;


