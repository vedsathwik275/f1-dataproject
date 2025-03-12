
import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  message?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  size = 'md', 
  message = 'Loading analysis...' 
}) => {
  // Determine size classes
  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24',
    lg: 'w-32 h-32',
  };

  return (
    <div className="flex flex-col items-center justify-center py-8">
      <div className="relative">
        <div className={`${sizeClasses[size]} rounded-full card-glass`}>
          <div className="absolute inset-0 checkered-flag-animation rounded-full opacity-20"></div>
          <div className="absolute top-0 bottom-0 left-0 right-0 flex items-center justify-center">
            <div className="w-1/3 h-1/3 rounded-full animate-pulse-red"></div>
          </div>
        </div>
        <div className="absolute inset-0 border-t-2 border-f1-red rounded-full animate-spin"></div>
      </div>
      
      <div className="mt-4 flex flex-col items-center">
        <p className="text-f1-silver font-medium">{message}</p>
        <div className="flex justify-center space-x-1 mt-2">
          <div className="w-2 h-2 bg-f1-red rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-f1-red rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          <div className="w-2 h-2 bg-f1-red rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
