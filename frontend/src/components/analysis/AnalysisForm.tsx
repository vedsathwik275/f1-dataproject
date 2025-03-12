
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import DataBrowser from '@/components/ui/custom/DataBrowser';
import { ChevronRight } from 'lucide-react';

// Mock data for demo
const years = Array.from({ length: 10 }, (_, i) => ({
  id: `${2023 - i}`,
  name: `${2023 - i}`,
}));

const sessionTypes = [
  { id: 'race', name: 'Race' },
  { id: 'qualifying', name: 'Qualifying' },
  { id: 'sprint', name: 'Sprint' },
  { id: 'practice1', name: 'Practice 1' },
  { id: 'practice2', name: 'Practice 2' },
  { id: 'practice3', name: 'Practice 3' },
];

interface AnalysisFormProps {
  type: 'driver' | 'race' | 'comparison' | 'qualifying';
  onSubmit: (formData: any) => void;
  isLoading?: boolean;
}

const AnalysisForm: React.FC<AnalysisFormProps> = ({
  type,
  onSubmit,
  isLoading = false,
}) => {
  // Form state
  const [year, setYear] = useState<any>(null);
  const [grandPrix, setGrandPrix] = useState<any>(null);
  const [sessionType, setSessionType] = useState<any>(null);
  const [driver1, setDriver1] = useState<any>(null);
  const [driver2, setDriver2] = useState<any>(null);

  // Mock data - in a real app, these would be fetched based on selected year
  const drivers = [
    { id: 'HAM', name: 'Lewis Hamilton', code: 'HAM', flag: 'https://via.placeholder.com/30x20' },
    { id: 'VER', name: 'Max Verstappen', code: 'VER', flag: 'https://via.placeholder.com/30x20' },
    { id: 'NOR', name: 'Lando Norris', code: 'NOR', flag: 'https://via.placeholder.com/30x20' },
    { id: 'LEC', name: 'Charles Leclerc', code: 'LEC', flag: 'https://via.placeholder.com/30x20' },
    { id: 'PER', name: 'Sergio Perez', code: 'PER', flag: 'https://via.placeholder.com/30x20' },
  ];

  const races = [
    { id: 'monaco', name: 'Monaco Grand Prix', flag: 'https://via.placeholder.com/30x20' },
    { id: 'silverstone', name: 'British Grand Prix', flag: 'https://via.placeholder.com/30x20' },
    { id: 'monza', name: 'Italian Grand Prix', flag: 'https://via.placeholder.com/30x20' },
    { id: 'spa', name: 'Belgian Grand Prix', flag: 'https://via.placeholder.com/30x20' },
    { id: 'suzuka', name: 'Japanese Grand Prix', flag: 'https://via.placeholder.com/30x20' },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const formData = {
      year,
      grandPrix,
      sessionType,
      driver1,
      driver2,
    };
    
    onSubmit(formData);
  };
  
  const renderFormFields = () => {
    switch (type) {
      case 'driver':
        return (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <DataBrowser 
                title="Year"
                items={years}
                onSelect={setYear}
                selectedItem={year}
                type="year"
              />
              <DataBrowser 
                title="Grand Prix"
                items={races}
                onSelect={setGrandPrix}
                selectedItem={grandPrix}
                type="race"
              />
              <DataBrowser 
                title="Session Type"
                items={sessionTypes}
                onSelect={setSessionType}
                selectedItem={sessionType}
                type="race"
              />
              <DataBrowser 
                title="Driver"
                items={drivers}
                onSelect={setDriver1}
                selectedItem={driver1}
                type="driver"
              />
            </div>
          </>
        );
        
      case 'race':
        return (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <DataBrowser 
                title="Year"
                items={years}
                onSelect={setYear}
                selectedItem={year}
                type="year"
              />
              <DataBrowser 
                title="Grand Prix"
                items={races}
                onSelect={setGrandPrix}
                selectedItem={grandPrix}
                type="race"
              />
              <DataBrowser 
                title="Session Type"
                items={sessionTypes}
                onSelect={setSessionType}
                selectedItem={sessionType}
                type="race"
              />
            </div>
          </>
        );
        
      case 'comparison':
        return (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <DataBrowser 
                title="Year"
                items={years}
                onSelect={setYear}
                selectedItem={year}
                type="year"
              />
              <DataBrowser 
                title="Grand Prix"
                items={races}
                onSelect={setGrandPrix}
                selectedItem={grandPrix}
                type="race"
              />
              <DataBrowser 
                title="Session Type"
                items={sessionTypes}
                onSelect={setSessionType}
                selectedItem={sessionType}
                type="race"
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <DataBrowser 
                title="Driver 1"
                items={drivers}
                onSelect={setDriver1}
                selectedItem={driver1}
                type="driver"
              />
              <DataBrowser 
                title="Driver 2"
                items={drivers}
                onSelect={setDriver2}
                selectedItem={driver2}
                type="driver"
              />
            </div>
          </>
        );
        
      case 'qualifying':
        return (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <DataBrowser 
                title="Year"
                items={years}
                onSelect={setYear}
                selectedItem={year}
                type="year"
              />
              <DataBrowser 
                title="Grand Prix"
                items={races}
                onSelect={setGrandPrix}
                selectedItem={grandPrix}
                type="race"
              />
            </div>
          </>
        );
        
      default:
        return null;
    }
  };

  return (
    <form onSubmit={handleSubmit} className="analysis-form">
      <h2 className="text-xl font-bold mb-6 text-white">
        {type === 'driver' && 'Driver Performance Analysis'}
        {type === 'race' && 'Race Analysis'}
        {type === 'comparison' && 'Driver Comparison'}
        {type === 'qualifying' && 'Qualifying Analysis'}
      </h2>
      
      {renderFormFields()}
      
      <div className="mt-6 flex justify-end">
        <Button 
          type="submit" 
          className="btn-primary flex items-center"
          disabled={isLoading}
        >
          <span>Analyze</span>
          <ChevronRight size={16} className="ml-1" />
        </Button>
      </div>
    </form>
  );
};

export default AnalysisForm;
