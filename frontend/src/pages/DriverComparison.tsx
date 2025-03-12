
import React, { useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import AnalysisForm from '@/components/analysis/AnalysisForm';
import VisualizationCard from '@/components/ui/custom/VisualizationCard';
import LoadingSpinner from '@/components/ui/custom/LoadingSpinner';
import { BarChart3, Users, Gauge, MoveHorizontal } from 'lucide-react';

const DriverComparison = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const handleAnalysisSubmit = (formData: any) => {
    console.log('Driver comparison requested:', formData);
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
              <BarChart3 size={24} className="text-f1-red mr-2" />
              <h1 className="text-3xl font-bold text-white">Driver Comparison</h1>
            </div>
            <p className="text-f1-silver">
              Head-to-head comparison between drivers with detailed telemetry visualization and performance metrics.
            </p>
          </div>
          
          <AnalysisForm 
            type="comparison"
            onSubmit={handleAnalysisSubmit}
            isLoading={isLoading}
          />
          
          {isLoading && (
            <div className="results-container py-12">
              <LoadingSpinner 
                size="lg"
                message="Analyzing driver comparison data..."
              />
            </div>
          )}
          
          {showResults && !isLoading && (
            <div className="results-container">
              <h2 className="text-xl font-bold mb-6 text-white">Comparison Results</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Lap Time Delta</p>
                      <p className="text-2xl font-medium text-white">+0.243s</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <MoveHorizontal size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Top Speed Difference</p>
                      <p className="text-2xl font-medium text-white">+4.2 km/h</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Gauge size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Fastest Sector</p>
                      <p className="text-2xl font-medium text-white">S2</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Users size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Cornering Delta</p>
                      <p className="text-2xl font-medium text-white">-0.12s</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <BarChart3 size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <VisualizationCard 
                  title="Lap Time Comparison"
                  imageSrc="https://via.placeholder.com/600x400"
                  description="Lap-by-lap time comparison highlighting performance differences throughout the session."
                />
                
                <VisualizationCard 
                  title="Sector Time Comparison"
                  imageSrc="https://via.placeholder.com/600x400"
                  description="Detailed sector time comparison showing strengths and weaknesses in different parts of the circuit."
                />
              </div>
              
              <div className="grid grid-cols-1 mb-6">
                <VisualizationCard 
                  title="Speed Trace Overlay"
                  imageSrc="https://via.placeholder.com/1200x400"
                  description="Detailed speed trace overlay showing throttle, brake and speed differences throughout a lap."
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <VisualizationCard 
                  title="Cornering Analysis"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Comparison of cornering techniques, apex speeds, and racing lines."
                />
                
                <VisualizationCard 
                  title="Braking Analysis"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Comparison of braking points, brake pressure, and deceleration rates."
                />
                
                <VisualizationCard 
                  title="Acceleration Analysis"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Comparison of throttle application, traction control usage, and acceleration rates."
                />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default DriverComparison;
