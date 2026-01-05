'use client';

import React, { useState } from 'react';
import ImageUpload from '@/components/Classification/ImageUpload';
import PredictionResult from '@/components/Classification/PredictionResult';
import ConfidenceChart from '@/components/Classification/ConfidenceChart';
import Button from '@/components/Shared/Button';
import LoadingSpinner from '@/components/Shared/LoadingSpinner';
import ErrorMessage from '@/components/Shared/ErrorMessage';
import { classificationAPI } from '@/lib/api';
import { ClassificationResult } from '@/types';

export default function ClassificationPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleImageSelect = (file: File) => {
    setSelectedFile(file);
    setResult(null);
    setError('');
    
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleClassify = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await classificationAPI.classify(selectedFile);
      setResult({
        predicted_class: response.predicted_class as 'Traditional' | 'Fusion' | 'Modern',
        confidence: response.confidence,
        probabilities: response.probabilities,
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to classify image. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl('');
    setResult(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-primary">
      <div className="containerpadding container mx-auto py-8 md:py-12">
        {/* Header */}
        <div className="text-center mb-8 md:mb-12">
          <h1 className="title text-blackbrown mb-4">
            Handicraft Classification
          </h1>
          <p className="description text-blackbrown max-w-2xl mx-auto">
            Upload an image of a Sri Lankan handicraft to classify it as Traditional, Fusion, or Modern.
            Our AI model achieves 79.25% accuracy on test data.
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6">
            <ErrorMessage message={error} />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
          {/* Left Column - Image Upload */}
          <div className="space-y-6">
            <div className="bg-primary border-2 border-lightbrown rounded-lg p-6">
              <h2 className="text-xl font-bold text-blackbrown mb-4">
                Upload Image
              </h2>
              <ImageUpload
                onImageSelect={handleImageSelect}
                previewUrl={previewUrl}
                isLoading={isLoading}
              />
              
              <div className="flex gap-4 mt-6">
                <Button
                  onClick={handleClassify}
                  disabled={!selectedFile || isLoading}
                  className="flex-1"
                >
                  {isLoading ? (
                    <span className="flex items-center gap-2">
                      <LoadingSpinner size="sm" />
                      Classifying...
                    </span>
                  ) : (
                    'Classify Image'
                  )}
                </Button>
                
                {selectedFile && (
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

            {/* Prediction Result */}
            <PredictionResult result={result} isLoading={isLoading} />
          </div>

          {/* Right Column - Confidence Chart */}
          <div>
            <ConfidenceChart result={result} />
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
              <span>Upload a clear image of a Sri Lankan handicraft</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">2.</span>
              <span>Our AI model analyzes the design elements and patterns</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">3.</span>
              <span>Get instant classification with confidence scores</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
