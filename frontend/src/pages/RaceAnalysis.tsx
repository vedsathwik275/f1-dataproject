
import React, { useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import AnalysisForm from '@/components/analysis/AnalysisForm';
import VisualizationCard from '@/components/ui/custom/VisualizationCard';
import LoadingSpinner from '@/components/ui/custom/LoadingSpinner';
import { Flag, Clock3, PieChart, ArrowUpDown } from 'lucide-react';

const RaceAnalysis = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const handleAnalysisSubmit = (formData: any) => {
    console.log('Race analysis requested:', formData);
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
              <Flag size={24} className="text-f1-red mr-2" />
              <h1 className="text-3xl font-bold text-white">Race Analysis</h1>
            </div>
            <p className="text-f1-silver">
              Comprehensive race analysis with position changes, pace, strategy insights, and lap-by-lap breakdowns.
            </p>
          </div>
          
          <AnalysisForm 
            type="race"
            onSubmit={handleAnalysisSubmit}
            isLoading={isLoading}
          />
          
          {isLoading && (
            <div className="results-container py-12">
              <LoadingSpinner 
                size="lg"
                message="Analyzing race data..."
              />
            </div>
          )}
          
          {showResults && !isLoading && (
            <div className="results-container">
              <h2 className="text-xl font-bold mb-6 text-white">Race Analysis Results</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Race Position</p>
                      <p className="text-2xl font-medium text-white">P4</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Flag size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Gap to Winner</p>
                      <p className="text-2xl font-medium text-white">+12.345s</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Clock3 size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Pit Stops</p>
                      <p className="text-2xl font-medium text-white">2</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <PieChart size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Positions Gained</p>
                      <p className="text-2xl font-medium text-white">+3</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <ArrowUpDown size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <VisualizationCard 
                  title="Race Pace Analysis"
                  imageSrc="https://via.placeholder.com/600x400"
                  description="Lap-by-lap pace compared to competitors, highlighting performance variations throughout the race."
                />
                
                <VisualizationCard 
                  title="Tire Strategy"
                  imageSrc="https://via.placeholder.com/600x400"
                  description="Tire compound usage and performance degradation across race distance."
                />
              </div>
              
              <div className="grid grid-cols-1 mb-6">
                <VisualizationCard 
                  title="Position Changes"
                  imageSrc="https://via.placeholder.com/1200x400"
                  description="Lap-by-lap position changes throughout the race with key overtaking moments highlighted."
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <VisualizationCard 
                  title="Stint Analysis - Soft"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Performance details during soft tire stint with lap time consistency and degradation."
                />
                
                <VisualizationCard 
                  title="Stint Analysis - Medium"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Performance details during medium tire stint with lap time consistency and degradation."
                />
                
                <VisualizationCard 
                  title="Stint Analysis - Hard"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Performance details during hard tire stint with lap time consistency and degradation."
                />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default RaceAnalysis;
