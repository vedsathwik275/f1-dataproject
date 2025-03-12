
import React from 'react';
import RaceTab from './RaceTab';
import { Race } from '@/models/race';

interface RaceTabsProps {
  races: Race[];
  selectedRound: number;
  onSelectRound: (round: number) => void;
}

const RaceTabs: React.FC<RaceTabsProps> = ({ 
  races, 
  selectedRound, 
  onSelectRound 
}) => {
  return (
    <div className="flex border-b border-f1-gray/30">
      {races.map((race, index) => (
        <RaceTab
          key={race.id}
          index={index}
          selectedIndex={selectedRound - 1}
          roundNumber={index + 1}
          onClick={() => onSelectRound(index + 1)}
        />
      ))}
    </div>
  );
};

export default RaceTabs;
