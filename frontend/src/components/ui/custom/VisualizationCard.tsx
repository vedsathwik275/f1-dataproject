
import React, { useState } from 'react';
import { Maximize2, Download, Info } from 'lucide-react';

interface VisualizationCardProps {
  title: string;
  imageSrc: string;
  description?: string;
  isLoading?: boolean;
}

const VisualizationCard: React.FC<VisualizationCardProps> = ({
  title,
  imageSrc,
  description,
  isLoading = false,
}) => {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showInfo, setShowInfo] = useState(false);

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const toggleInfo = () => {
    setShowInfo(!showInfo);
  };

  const handleDownload = () => {
    // Create a temporary link element
    const link = document.createElement('a');
    link.href = imageSrc;
    link.download = `f1-visualization-${title.toLowerCase().replace(/\s+/g, '-')}.png`;
    
    // Append to the document
    document.body.appendChild(link);
    
    // Trigger the download
    link.click();
    
    // Clean up
    document.body.removeChild(link);
  };

  return (
    <>
      <div className={`card-glass overflow-hidden transition-all duration-300 ease-in-out ${isLoading ? 'opacity-60' : ''}`}>
        <div className="p-4 flex justify-between items-center border-b border-f1-gray/30">
          <h3 className="text-white text-lg font-medium">{title}</h3>
          <div className="flex space-x-2">
            <button
              onClick={toggleInfo}
              className="p-1.5 rounded-full hover:bg-f1-gray/20 text-f1-lightgray hover:text-white transition-colors"
              aria-label="Show information"
            >
              <Info size={16} />
            </button>
            <button
              onClick={handleDownload}
              className="p-1.5 rounded-full hover:bg-f1-gray/20 text-f1-lightgray hover:text-white transition-colors"
              aria-label="Download visualization"
            >
              <Download size={16} />
            </button>
            <button
              onClick={toggleFullscreen}
              className="p-1.5 rounded-full hover:bg-f1-gray/20 text-f1-lightgray hover:text-white transition-colors"
              aria-label="View fullscreen"
            >
              <Maximize2 size={16} />
            </button>
          </div>
        </div>
        
        <div className="relative">
          {isLoading && (
            <div className="absolute inset-0 flex items-center justify-center bg-f1-darker/50 z-10">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-f1-red"></div>
            </div>
          )}
          
          <div className="flex justify-center items-center p-4">
            <img
              src={imageSrc}
              alt={title}
              className="max-w-full rounded transition-transform duration-200 hover:scale-[1.02]"
            />
          </div>
        </div>
        
        {showInfo && description && (
          <div className="p-4 border-t border-f1-gray/30 bg-f1-dark/50">
            <p className="text-sm text-f1-silver">{description}</p>
          </div>
        )}
      </div>

      {/* Fullscreen Modal */}
      {isFullscreen && (
        <div 
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          onClick={toggleFullscreen}
        >
          <div 
            className="relative max-w-5xl max-h-screen"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="absolute top-4 right-4 flex space-x-4 z-10">
              <button
                onClick={handleDownload}
                className="p-2 bg-f1-dark/70 rounded-full hover:bg-f1-dark transition-colors"
                aria-label="Download visualization"
              >
                <Download size={20} className="text-white" />
              </button>
              <button
                onClick={toggleFullscreen}
                className="p-2 bg-f1-dark/70 rounded-full hover:bg-f1-dark transition-colors"
                aria-label="Close fullscreen"
              >
                <Maximize2 size={20} className="text-white" />
              </button>
            </div>
            
            <img
              src={imageSrc}
              alt={title}
              className="max-w-full max-h-[90vh] object-contain rounded shadow-xl"
            />
            
            <div className="mt-4 bg-f1-dark/70 p-4 rounded">
              <h3 className="text-white text-xl font-medium mb-2">{title}</h3>
              {description && <p className="text-f1-silver">{description}</p>}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default VisualizationCard;
