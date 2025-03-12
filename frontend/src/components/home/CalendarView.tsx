
import React, { useState } from 'react';
import { Calendar } from 'lucide-react';
import { races2025 } from '@/data/races';
import RaceTabs from './calendar/RaceTabs';
import RaceDetails from './calendar/RaceDetails';
import RaceNavigation from './calendar/RaceNavigation';

const CalendarView: React.FC = () => {
  const [selectedRound, setSelectedRound] = useState<number>(1);
  const races = races2025;
  
  const nextRace = () => {
    if (selectedRound < races.length) {
      setSelectedRound(selectedRound + 1);
    }
  };

  const prevRace = () => {
    if (selectedRound > 1) {
      setSelectedRound(selectedRound - 1);
    }
  };

  const selectedRaceIndex = selectedRound - 1;
  const selectedRace = races[selectedRaceIndex];

  return (
    <div className="py-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white flex items-center">
          <Calendar size={24} className="mr-2 text-f1-red" />
          2025 F1 Calendar
        </h2>
        <a 
          href="/calendar"
          className="text-f1-red hover:text-f1-red/80 text-sm font-medium transition-colors"
        >
          View Full Calendar
        </a>
      </div>
      
      <div className="card-glass overflow-hidden">
        <RaceTabs 
          races={races} 
          selectedRound={selectedRound} 
          onSelectRound={setSelectedRound} 
        />
        
        <div className="p-6">
          <RaceDetails race={selectedRace} />
          
          <RaceNavigation 
            selectedRound={selectedRound} 
            totalRaces={races.length} 
            onPrevRace={prevRace} 
            onNextRace={nextRace} 
          />
        </div>
      </div>
    </div>
  );
};

export default CalendarView;
