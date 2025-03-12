
import React from 'react';
import { MapPin, Calendar as CalendarIcon } from 'lucide-react';
import { Race } from '@/models/race';

interface RaceDetailsProps {
  race: Race;
}

const RaceDetails: React.FC<RaceDetailsProps> = ({ race }) => {
  return (
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
      <div className="flex items-center mb-4 md:mb-0">
        <img 
          src={race.flag} 
          alt={`Flag of ${race.location}`} 
          className="w-10 h-6 object-cover rounded mr-4"
        />
        <div>
          <h3 className="text-xl font-bold text-white">{race.name}</h3>
          <p className="text-f1-silver flex items-center">
            <MapPin size={14} className="mr-1" />
            {race.circuit}, {race.location}
          </p>
        </div>
      </div>
      
      <div className="flex items-center">
        <div className="flex flex-col items-end">
          <span className="text-f1-silver flex items-center">
            <CalendarIcon size={14} className="mr-1" />
            {race.date}
          </span>
          {race.completed ? (
            <span className="text-sm px-2 py-0.5 bg-f1-dark rounded-full text-f1-silver mt-1">
              Completed
            </span>
          ) : (
            <span className="text-sm px-2 py-0.5 bg-f1-red rounded-full text-white mt-1">
              Upcoming
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default RaceDetails;
