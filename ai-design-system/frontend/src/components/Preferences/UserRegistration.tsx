'use client';

import React from 'react';
import { USER_TYPES, AGE_GROUPS, GENDERS } from '@/lib/constants';

interface UserRegistrationProps {
  onSubmit: (data: {
    user_type: string;
    age_group: string;
    gender: string;
    country: string;
  }) => void;
  isLoading?: boolean;
}

export default function UserRegistration({
  onSubmit,
  isLoading = false,
}: UserRegistrationProps) {
  const [formData, setFormData] = React.useState({
    user_type: 'Tourist',
    age_group: '25-34',
    gender: 'Male',
    country: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.country.trim()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="bg-primary border-2 border-lightbrown rounded-lg p-6 md:p-8">
      <h2 className="text-2xl font-bold text-blackbrown mb-6">
        Welcome to Handicraft Gallery
      </h2>
      <p className="description text-blackbrown mb-6">
        Help us understand design preferences by browsing and rating AI-generated designs.
        Your feedback helps artisans create better products.
      </p>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* User Type */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-blackbrown">
            I am a
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {USER_TYPES.map((type) => (
              <label
                key={type.value}
                className={`flex items-center justify-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  formData.user_type === type.value
                    ? 'border-secondarybrown bg-secondarybrown text-primary'
                    : 'border-lightbrown bg-primary text-blackbrown hover:border-secondarybrown'
                }`}
              >
                <input
                  type="radio"
                  name="user_type"
                  value={type.value}
                  checked={formData.user_type === type.value}
                  onChange={(e) =>
                    setFormData({ ...formData, user_type: e.target.value })
                  }
                  className="sr-only"
                />
                <span className="font-medium">{type.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Age Group */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-blackbrown">
            Age Group
          </label>
          <select
            value={formData.age_group}
            onChange={(e) =>
              setFormData({ ...formData, age_group: e.target.value })
            }
            className="w-full px-4 py-3 bg-primary border-2 border-lightbrown rounded-lg text-blackbrown focus:border-secondarybrown focus:outline-none transition-colors"
          >
            {AGE_GROUPS.map((age) => (
              <option key={age.value} value={age.value}>
                {age.label}
              </option>
            ))}
          </select>
        </div>

        {/* Gender */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-blackbrown">
            Gender
          </label>
          <div className="grid grid-cols-3 gap-3">
            {GENDERS.map((gender) => (
              <label
                key={gender.value}
                className={`flex items-center justify-center p-3 border-2 rounded-lg cursor-pointer transition-all ${
                  formData.gender === gender.value
                    ? 'border-secondarybrown bg-secondarybrown text-primary'
                    : 'border-lightbrown bg-primary text-blackbrown hover:border-secondarybrown'
                }`}
              >
                <input
                  type="radio"
                  name="gender"
                  value={gender.value}
                  checked={formData.gender === gender.value}
                  onChange={(e) =>
                    setFormData({ ...formData, gender: e.target.value })
                  }
                  className="sr-only"
                />
                <span className="text-sm font-medium">{gender.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Country */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-blackbrown">
            Country
          </label>
          <input
            type="text"
            value={formData.country}
            onChange={(e) =>
              setFormData({ ...formData, country: e.target.value })
            }
            placeholder="e.g., Sri Lanka, Germany, USA"
            required
            className="w-full px-4 py-3 bg-primary border-2 border-lightbrown rounded-lg text-blackbrown placeholder-lightbrown focus:border-secondarybrown focus:outline-none transition-colors"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || !formData.country.trim()}
          className="w-full py-3 bg-secondarybrown text-primary font-medium rounded-lg hover:bg-darkbrown transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Starting...' : 'Start Browsing Designs'}
        </button>
      </form>
    </div>
  );
}



