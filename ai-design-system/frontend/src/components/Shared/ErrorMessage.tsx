import React from 'react';

interface ErrorMessageProps {
  message: string;
  className?: string;
}

export default function ErrorMessage({ message, className = '' }: ErrorMessageProps) {
  return (
    <div className={`bg-red/10 border border-red text-red px-4 py-3 rounded ${className}`}>
      <p className="font-medium">{message}</p>
    </div>
  );
}

