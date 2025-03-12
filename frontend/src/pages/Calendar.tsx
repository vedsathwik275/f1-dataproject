
import React, { useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import { Calendar as CalendarIcon, ChevronDown, ChevronUp, MapPin, Clock } from 'lucide-react';
import { races2025 } from '@/data/races';
import { Race } from '@/models/race';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const Calendar = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [expandedRace, setExpandedRace] = useState<string | null>(null);

  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const toggleRaceExpansion = (raceId: string) => {
    if (expandedRace === raceId) {
      setExpandedRace(null);
    } else {
      setExpandedRace(raceId);
    }
  };

  const races = races2025;
  
  // Group races by their status (upcoming or completed)
  const upcomingRaces = races.filter(race => race.upcoming);
  const completedRaces = races.filter(race => race.completed);
  
  const renderRace = (race: Race) => {
    const isExpanded = expandedRace === race.id;
    
    return (
      <div 
        key={race.id} 
        className={`card-glass mb-4 overflow-hidden transition-all duration-300 ${
          isExpanded ? 'shadow-lg' : ''
        }`}
      >
        <div 
          className="p-4 md:p-5 flex flex-col md:flex-row md:items-center justify-between cursor-pointer"
          onClick={() => toggleRaceExpansion(race.id)}
        >
          <div className="flex items-center mb-3 md:mb-0">
            <div className="w-12 h-8 mr-4 overflow-hidden rounded flex-shrink-0">
              <img 
                src={race.flag} 
                alt={`${race.location} flag`} 
                className="w-full h-full object-cover"
              />
            </div>
            <div>
              <h3 className="text-white font-bold text-lg">{race.name}</h3>
              <p className="text-f1-silver text-sm flex items-center">
                <MapPin size={14} className="mr-1" /> {race.location}
              </p>
            </div>
          </div>
          
          <div className="flex items-center justify-between md:justify-end w-full md:w-auto">
            <div className="text-right mr-4">
              <p className="text-white font-medium">{race.date}</p>
              <p className="text-f1-silver text-sm">{race.circuit}</p>
            </div>
            {isExpanded ? (
              <ChevronUp size={20} className="text-f1-red" />
            ) : (
              <ChevronDown size={20} className="text-f1-red" />
            )}
          </div>
        </div>
        
        {isExpanded && (
          <div className="bg-f1-darker p-4 md:p-6 border-t border-f1-gray/20">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-white font-semibold mb-3 flex items-center">
                  <Clock size={18} className="text-f1-red mr-2" /> Race Schedule
                </h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-f1-silver">Free Practice 1</span>
                    <span className="text-white">Fri 10:30</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-f1-silver">Free Practice 2</span>
                    <span className="text-white">Fri 14:00</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-f1-silver">Free Practice 3</span>
                    <span className="text-white">Sat 10:30</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-f1-silver">Qualifying</span>
                    <span className="text-white">Sat 14:00</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-f1-silver">Race</span>
                    <span className="text-white">Sun 14:00</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="text-white font-semibold mb-3">Circuit Information</h4>
                <div className="bg-f1-dark rounded-lg overflow-hidden">
                  <img 
                    src="https://via.placeholder.com/400x200" 
                    alt={`${race.circuit} layout`} 
                    className="w-full h-40 object-cover"
                  />
                  <div className="p-4">
                    <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                      <div>
                        <span className="text-f1-silver">Length:</span>
                        <p className="text-white">5.303 km</p>
                      </div>
                      <div>
                        <span className="text-f1-silver">Laps:</span>
                        <p className="text-white">70</p>
                      </div>
                      <div>
                        <span className="text-f1-silver">Distance:</span>
                        <p className="text-white">371.21 km</p>
                      </div>
                      <div>
                        <span className="text-f1-silver">Lap Record:</span>
                        <p className="text-white">1:13.556</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex min-h-screen bg-f1-charcoal">
      <Header />
      <Sidebar isCollapsed={isSidebarCollapsed} toggleSidebar={toggleSidebar} />
      
      <main 
        className={`flex-1 pt-16 transition-all duration-300 ${
          isSidebarCollapsed ? 'ml-16' : 'ml-60'
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <div className="flex items-center mb-2">
              <CalendarIcon size={24} className="text-f1-red mr-2" />
              <h1 className="text-3xl font-bold text-white">2025 Formula 1 Calendar</h1>
            </div>
            <p className="text-f1-silver">
              View the complete Formula 1 race schedule for the 2025 season with circuit details and session times.
            </p>
          </div>
          
          <Tabs defaultValue="upcoming" className="mb-8">
            <TabsList className="bg-f1-dark border border-f1-gray/20 mb-6">
              <TabsTrigger value="upcoming" className="data-[state=active]:bg-f1-red data-[state=active]:text-white">
                Upcoming Races
              </TabsTrigger>
              <TabsTrigger value="completed" className="data-[state=active]:bg-f1-red data-[state=active]:text-white">
                Completed Races
              </TabsTrigger>
              <TabsTrigger value="all" className="data-[state=active]:bg-f1-red data-[state=active]:text-white">
                All Races
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="upcoming" className="mt-0">
              {upcomingRaces.length > 0 ? (
                upcomingRaces.map(renderRace)
              ) : (
                <div className="text-center py-12 text-f1-silver">
                  No upcoming races for the current season.
                </div>
              )}
            </TabsContent>
            
            <TabsContent value="completed" className="mt-0">
              {completedRaces.length > 0 ? (
                completedRaces.map(renderRace)
              ) : (
                <div className="text-center py-12 text-f1-silver">
                  No completed races for the current season yet.
                </div>
              )}
            </TabsContent>
            
            <TabsContent value="all" className="mt-0">
              {races.map(renderRace)}
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  );
};

export default Calendar;
