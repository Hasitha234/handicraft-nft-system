'use client';

import React, { useState } from 'react';
import CraftSelector from '@/components/DesignGenerator/CraftSelector';
import FusionSlider from '@/components/DesignGenerator/FusionSlider';
import DesignGallery from '@/components/DesignGenerator/DesignGallery';
import PromptDisplay from '@/components/DesignGenerator/PromptDisplay';
import Button from '@/components/Shared/Button';
import LoadingSpinner from '@/components/Shared/LoadingSpinner';
import ErrorMessage from '@/components/Shared/ErrorMessage';
import { STYLE_PREFERENCES } from '@/lib/constants';

export default function DesignGeneratorPage() {
  const [craftType, setCraftType] = useState('mask');
  const [stylePreference, setStylePreference] = useState('fusion');
  const [fusionLevel, setFusionLevel] = useState(50);
  const [additionalPrompt, setAdditionalPrompt] = useState('');
  const [designs, setDesigns] = useState<string[]>([]);
  const [prompts, setPrompts] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleGenerate = async () => {
    setIsLoading(true);
    setError('');
    setDesigns([]);
    setPrompts([]);

    try {
      // TODO: Replace with actual API call when design generation endpoint is ready
      // For now, simulate generation
      await new Promise((resolve) => setTimeout(resolve, 2000));
      
      // Mock data - replace with actual API response
      const mockDesigns = Array.from({ length: 5 }, (_, i) => 
        `https://via.placeholder.com/512x512/693422/F6E7CA?text=Design+${i + 1}`
      );
      const mockPrompts = Array.from({ length: 5 }, (_, i) => 
        `Fusion design: ${craftType} with ${stylePreference} style, ${fusionLevel}% fusion level${additionalPrompt ? `, ${additionalPrompt}` : ''}`
      );

      setDesigns(mockDesigns);
      setPrompts(mockPrompts);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to generate designs. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setCraftType('mask');
    setStylePreference('fusion');
    setFusionLevel(50);
    setAdditionalPrompt('');
    setDesigns([]);
    setPrompts([]);
    setError('');
  };

  return (
    <div className="min-h-screen bg-primary">
      <div className="containerpadding container mx-auto py-8 md:py-12">
        {/* Header */}
        <div className="text-center mb-8 md:mb-12">
          <h1 className="title text-blackbrown mb-4">
            AI Design Generator
          </h1>
          <p className="description text-blackbrown max-w-2xl mx-auto">
            Generate fusion designs by blending traditional Sri Lankan patterns with modern styles.
            Control the fusion level to create designs that balance cultural authenticity with contemporary appeal.
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6">
            <ErrorMessage message={error} />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
          {/* Left Column - Controls */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-primary border-2 border-lightbrown rounded-lg p-6 sticky top-24">
              <h2 className="text-xl font-bold text-blackbrown mb-6">
                Design Settings
              </h2>

              <div className="space-y-6">
                {/* Craft Type */}
                <CraftSelector
                  value={craftType}
                  onChange={setCraftType}
                  disabled={isLoading}
                />

                {/* Style Preference */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-blackbrown">
                    Style Preference
                  </label>
                  <div className="space-y-2">
                    {STYLE_PREFERENCES.map((style) => (
                      <label
                        key={style.value}
                        className="flex items-center space-x-3 p-3 bg-lightbrown/30 rounded-lg cursor-pointer hover:bg-lightbrown/50 transition-colors"
                      >
                        <input
                          type="radio"
                          name="style"
                          value={style.value}
                          checked={stylePreference === style.value}
                          onChange={(e) => setStylePreference(e.target.value)}
                          disabled={isLoading}
                          className="w-4 h-4 text-secondarybrown focus:ring-secondarybrown"
                        />
                        <span className="text-blackbrown font-medium">
                          {style.label}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Fusion Level */}
                <FusionSlider
                  value={fusionLevel}
                  onChange={setFusionLevel}
                  disabled={isLoading}
                />

                {/* Additional Prompt */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-blackbrown">
                    Additional Details (Optional)
                  </label>
                  <textarea
                    value={additionalPrompt}
                    onChange={(e) => setAdditionalPrompt(e.target.value)}
                    disabled={isLoading}
                    placeholder="e.g., bright colors, gold accents, geometric patterns"
                    rows={3}
                    className="w-full px-4 py-3 bg-primary border-2 border-lightbrown rounded-lg text-blackbrown focus:border-secondarybrown focus:outline-none transition-colors disabled:opacity-50 disabled:cursor-not-allowed resize-none"
                  />
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 pt-4">
                  <Button
                    onClick={handleGenerate}
                    disabled={isLoading}
                    className="flex-1"
                    size="lg"
                  >
                    {isLoading ? (
                      <span className="flex items-center justify-center gap-2">
                        <LoadingSpinner size="sm" />
                        Generating...
                      </span>
                    ) : (
                      'Generate 5 Designs'
                    )}
                  </Button>
                  
                  {designs.length > 0 && (
                    <Button
                      onClick={handleReset}
                      variant="outline"
                      disabled={isLoading}
                    >
                      Reset
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2 space-y-6">
            <DesignGallery designs={designs} isLoading={isLoading} />
            {prompts.length > 0 && <PromptDisplay prompts={prompts} />}
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-8 md:mt-12 bg-lightbrown/30 border border-lightbrown rounded-lg p-6">
          <h3 className="text-lg font-bold text-blackbrown mb-3">
            How It Works
          </h3>
          <ul className="space-y-2 text-blackbrown description">
            <li className="flex items-start">
              <span className="mr-2">1.</span>
              <span>Select craft type (Mask, Batik, Wood Carving, or Pottery)</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">2.</span>
              <span>Choose style preference and adjust fusion level (0-100%)</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">3.</span>
              <span>Add optional details to customize the design</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">4.</span>
              <span>Generate 5 unique design variations instantly</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
