'use client';

import React from 'react';
import Image from 'next/image';

interface DesignGalleryProps {
  designs: string[];
  isLoading?: boolean;
}

export default function DesignGallery({
  designs,
  isLoading = false,
}: DesignGalleryProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="aspect-square bg-lightbrown/30 rounded-lg animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (designs.length === 0) {
    return (
      <div className="bg-primary border-2 border-lightbrown rounded-lg p-12 text-center">
        <p className="text-lightbrown text-lg mb-2">No designs generated yet</p>
        <p className="text-lightbrown text-sm">
          Configure your settings and click "Generate Designs" to create AI-powered fusion designs
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-blackbrown">
        Generated Designs ({designs.length})
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {designs.map((design, index) => (
          <div
            key={index}
            className="group relative aspect-square bg-primary border-2 border-lightbrown rounded-lg overflow-hidden hover:border-secondarybrown transition-all duration-200"
          >
            <Image
              src={design}
              alt={`Generated design ${index + 1}`}
              fill
              className="object-cover"
            />
            <div className="absolute inset-0 bg-blackbrown/0 group-hover:bg-blackbrown/20 transition-colors flex items-center justify-center">
              <span className="opacity-0 group-hover:opacity-100 text-primary font-medium transition-opacity">
                Design {index + 1}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

