
import React from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';

interface RaceNavigationProps {
  selectedRound: number;
  totalRaces: number;
  onPrevRace: () => void;
  onNextRace: () => void;
}

const RaceNavigation: React.FC<RaceNavigationProps> = ({
  selectedRound,
  totalRaces,
  onPrevRace,
  onNextRace
}) => {
  return (
    <div className="flex justify-between mt-8">
      <button
        onClick={onPrevRace}
        disabled={selectedRound === 1}
        className={`flex items-center px-3 py-1.5 rounded ${
          selectedRound === 1
            ? 'text-f1-lightgray/50 cursor-not-allowed'
            : 'text-f1-lightgray hover:bg-f1-dark'
        }`}
      >
        <ArrowLeft size={16} className="mr-1" />
        Previous Race
      </button>
      
      <button
        onClick={onNextRace}
        disabled={selectedRound === totalRaces}
        className={`flex items-center px-3 py-1.5 rounded ${
          selectedRound === totalRaces
            ? 'text-f1-lightgray/50 cursor-not-allowed'
            : 'text-f1-lightgray hover:bg-f1-dark'
        }`}
      >
        Next Race
        <ArrowRight size={16} className="ml-1" />
      </button>
    </div>
  );
};

export default RaceNavigation;
