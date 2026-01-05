'use client';

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import Image from 'next/image';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  previewUrl?: string;
  isLoading?: boolean;
}

export default function ImageUpload({
  onImageSelect,
  previewUrl,
  isLoading = false,
}: ImageUploadProps) {
  const [dragActive, setDragActive] = useState(false);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onImageSelect(acceptedFiles[0]);
      }
    },
    [onImageSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp'],
    },
    multiple: false,
    disabled: isLoading,
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-all duration-200
          ${
            isDragActive || dragActive
              ? 'border-secondarybrown bg-lightbrown/20'
              : 'border-lightbrown bg-primary/50'
          }
          ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:border-secondarybrown hover:bg-lightbrown/10'}
        `}
        onMouseEnter={() => setDragActive(true)}
        onMouseLeave={() => setDragActive(false)}
      >
        <input {...getInputProps()} />
        
        {previewUrl ? (
          <div className="relative w-full h-64 md:h-96 rounded-lg overflow-hidden mb-4">
            <Image
              src={previewUrl}
              alt="Preview"
              fill
              className="object-contain"
            />
          </div>
        ) : (
          <div className="py-8">
            <svg
              className="mx-auto h-12 w-12 text-lightbrown mb-4"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <p className="text-blackbrown font-medium mb-2">
              {isDragActive ? 'Drop image here' : 'Drag & drop image here'}
            </p>
            <p className="text-lightbrown text-sm">or click to browse</p>
            <p className="text-lightbrown text-xs mt-2">
              Supports: JPEG, PNG, WebP
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

