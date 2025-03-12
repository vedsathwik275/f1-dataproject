
import React from 'react';

interface RaceTabProps {
  index: number;
  selectedIndex: number;
  roundNumber: number;
  onClick: () => void;
}

const RaceTab: React.FC<RaceTabProps> = ({ 
  index, 
  selectedIndex, 
  roundNumber, 
  onClick 
}) => {
  return (
    <div 
      className={`px-4 py-3 text-center w-full ${
        index === selectedIndex 
          ? 'text-white bg-f1-dark' 
          : 'text-f1-lightgray hover:bg-f1-dark/50 cursor-pointer'
      }`}
      onClick={onClick}
    >
      Round {roundNumber}
    </div>
  );
};

export default RaceTab;
