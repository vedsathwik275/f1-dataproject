
import React, { useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import AnalysisForm from '@/components/analysis/AnalysisForm';
import VisualizationCard from '@/components/ui/custom/VisualizationCard';
import LoadingSpinner from '@/components/ui/custom/LoadingSpinner';
import { BarChart, Users, Trophy, Clock3 } from 'lucide-react';

const DriverAnalysis = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const handleAnalysisSubmit = (formData: any) => {
    console.log('Analysis requested:', formData);
    setIsLoading(true);
    
    // Simulate API call delay
    setTimeout(() => {
      setIsLoading(false);
      setShowResults(true);
    }, 2000);
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
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="mb-8">
            <div className="flex items-center mb-2">
              <Users size={24} className="text-f1-red mr-2" />
              <h1 className="text-3xl font-bold text-white">Driver Performance Analysis</h1>
            </div>
            <p className="text-f1-silver">
              Analyze individual driver performance including lap times, sector times, and tire strategies.
            </p>
          </div>
          
          <AnalysisForm 
            type="driver"
            onSubmit={handleAnalysisSubmit}
            isLoading={isLoading}
          />
          
          {isLoading && (
            <div className="results-container py-12">
              <LoadingSpinner 
                size="lg"
                message="Analyzing driver performance data..."
              />
            </div>
          )}
          
          {showResults && !isLoading && (
            <div className="results-container">
              <h2 className="text-xl font-bold mb-6 text-white">Analysis Results</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Fastest Lap</p>
                      <p className="text-2xl font-medium text-white">1:23.456</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Clock3 size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Position</p>
                      <p className="text-2xl font-medium text-white">P3</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Trophy size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Average Lap</p>
                      <p className="text-2xl font-medium text-white">1:24.789</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Clock3 size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Points Earned</p>
                      <p className="text-2xl font-medium text-white">15</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <BarChart size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <VisualizationCard 
                  title="Lap Time Distribution"
                  imageSrc="https://via.placeholder.com/600x400"
                  description="Distribution of lap times throughout the race showing pace consistency and evolution."
                />
                
                <VisualizationCard 
                  title="Tire Strategy"
                  imageSrc="https://via.placeholder.com/600x400"
                  description="Tire compounds used during the race with corresponding lap time performance."
                />
              </div>
              
              <div className="grid grid-cols-1 mb-6">
                <VisualizationCard 
                  title="Sector Performance"
                  imageSrc="https://via.placeholder.com/1200x400"
                  description="Detailed sector time analysis compared to the driver's best sectors and race leader."
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <VisualizationCard 
                  title="Speed Traces - Sector 1"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Speed telemetry data through Sector 1 of the circuit."
                />
                
                <VisualizationCard 
                  title="Speed Traces - Sector 2"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Speed telemetry data through Sector 2 of the circuit."
                />
                
                <VisualizationCard 
                  title="Speed Traces - Sector 3"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Speed telemetry data through Sector 3 of the circuit."
                />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default DriverAnalysis;
