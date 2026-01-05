import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export default function Button({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles = 'font-neutiva font-medium rounded transition-colors duration-200';
  
  const variantStyles = {
    primary: 'bg-secondarybrown text-primary hover:bg-darkbrown',
    secondary: 'bg-lightbrown text-blackbrown hover:bg-secondarybrown hover:text-primary',
    outline: 'border-2 border-secondarybrown text-secondarybrown hover:bg-secondarybrown hover:text-primary',
  };
  
  const sizeStyles = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };
  
  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}



