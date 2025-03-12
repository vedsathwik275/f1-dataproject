
import React, { useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import AnalysisForm from '@/components/analysis/AnalysisForm';
import VisualizationCard from '@/components/ui/custom/VisualizationCard';
import LoadingSpinner from '@/components/ui/custom/LoadingSpinner';
import { Timer, Flag, Zap, Medal } from 'lucide-react';

const QualifyingAnalysis = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const handleAnalysisSubmit = (formData: any) => {
    console.log('Qualifying analysis requested:', formData);
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
              <Timer size={24} className="text-f1-red mr-2" />
              <h1 className="text-3xl font-bold text-white">Qualifying Analysis</h1>
            </div>
            <p className="text-f1-silver">
              Analyze qualifying sessions with detailed sector times, improvements across Q1, Q2, and Q3, and track evolution.
            </p>
          </div>
          
          <AnalysisForm 
            type="qualifying"
            onSubmit={handleAnalysisSubmit}
            isLoading={isLoading}
          />
          
          {isLoading && (
            <div className="results-container py-12">
              <LoadingSpinner 
                size="lg"
                message="Analyzing qualifying data..."
              />
            </div>
          )}
          
          {showResults && !isLoading && (
            <div className="results-container">
              <h2 className="text-xl font-bold mb-6 text-white">Qualifying Results</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Pole Position</p>
                      <p className="text-2xl font-medium text-white">1:21.046</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Flag size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Gap to Pole</p>
                      <p className="text-2xl font-medium text-white">+0.356s</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Timer size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Best Sector</p>
                      <p className="text-2xl font-medium text-white">S1</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Zap size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
                
                <div className="card-glass p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-f1-lightgray text-sm">Position</p>
                      <p className="text-2xl font-medium text-white">P2</p>
                    </div>
                    <div className="p-2 rounded-full bg-f1-dark">
                      <Medal size={20} className="text-f1-red" />
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <VisualizationCard 
                  title="Qualifying Progression"
                  imageSrc="https://via.placeholder.com/600x400"
                  description="Performance improvement across Q1, Q2, and Q3 sessions compared to competitors."
                />
                
                <VisualizationCard 
                  title="Sector Times Comparison"
                  imageSrc="https://via.placeholder.com/600x400"
                  description="Detailed sector time comparison with other drivers in the same qualifying session."
                />
              </div>
              
              <div className="grid grid-cols-1 mb-6">
                <VisualizationCard 
                  title="Qualifying Lap Analysis"
                  imageSrc="https://via.placeholder.com/1200x400"
                  description="Complete breakdown of the fastest qualifying lap with speed traces and comparison to pole position."
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <VisualizationCard 
                  title="Q1 Performance"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Detailed analysis of performance in the first qualifying segment."
                />
                
                <VisualizationCard 
                  title="Q2 Performance"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Detailed analysis of performance in the second qualifying segment."
                />
                
                <VisualizationCard 
                  title="Q3 Performance"
                  imageSrc="https://via.placeholder.com/400x300"
                  description="Detailed analysis of performance in the final qualifying segment."
                />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default QualifyingAnalysis;
