
import React, { useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import CalendarView from '@/components/home/CalendarView';
import { BarChart3, Users, Flag, Timer, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const Index = () => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const analysisModes = [
    {
      id: 'driver',
      title: 'Driver Performance',
      description: 'Analyze individual driver performance with detailed lap time analysis.',
      icon: Users,
      path: '/driver-analysis',
      color: 'from-purple-600 to-blue-600',
    },
    {
      id: 'race',
      title: 'Race Analysis',
      description: 'Comprehensive race stats with position changes, pace, and strategy insights.',
      icon: Flag,
      path: '/race-analysis',
      color: 'from-blue-600 to-cyan-600',
    },
    {
      id: 'comparison',
      title: 'Driver Comparison',
      description: 'Head-to-head comparison between drivers with telemetry visualization.',
      icon: BarChart3,
      path: '/driver-comparison',
      color: 'from-amber-600 to-orange-600',
    },
    {
      id: 'qualifying',
      title: 'Qualifying Analysis',
      description: 'Detailed qualifying session analysis with sector times and improvements.',
      icon: Timer,
      path: '/qualifying-analysis',
      color: 'from-green-600 to-emerald-600',
    },
  ];

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
          {/* Hero Section */}
          <div className="relative rounded-xl overflow-hidden mb-10 shadow-2xl">
            <div className="absolute inset-0 bg-gradient-to-r from-f1-darker/90 to-transparent z-10"></div>
            <img 
              src="https://via.placeholder.com/1200x400" 
              alt="F1 Racing" 
              className="w-full h-72 md:h-80 object-cover"
            />
            <div className="absolute inset-0 z-20 flex flex-col justify-center px-8 md:px-12 lg:px-16 py-10">
              <span className="inline-block text-f1-red font-medium text-sm md:text-base bg-f1-darker/50 px-3 py-1 rounded-sm mb-4">
                Formula 1 Data Analytics
              </span>
              <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 max-w-2xl leading-tight drop-shadow-md">
                Visualize and Analyze F1 Performance Data
              </h1>
              <p className="text-f1-silver max-w-xl mb-8 text-base md:text-lg leading-relaxed drop-shadow">
                Dive into detailed race analysis, lap times, and driver comparisons using FastF1 and OpenF1 APIs.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link 
                  to="/driver-analysis" 
                  className="btn-primary py-3 px-6 text-base font-semibold flex items-center"
                >
                  Start Analyzing
                  <ChevronRight className="ml-2" size={18} />
                </Link>
                <Link 
                  to="/about" 
                  className="btn-secondary py-3 px-6 text-base font-semibold"
                >
                  Learn More
                </Link>
              </div>
            </div>
          </div>
          
          {/* Analysis Modes Section */}
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-white mb-6">Analysis Modes</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {analysisModes.map((mode) => (
                <Link
                  key={mode.id}
                  to={mode.path}
                  className="card-glass p-6 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg group"
                >
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${mode.color} flex items-center justify-center mb-4`}>
                    <mode.icon size={24} className="text-white" />
                  </div>
                  <h3 className="text-lg font-bold text-white mb-2 group-hover:text-f1-red transition-colors">
                    {mode.title}
                  </h3>
                  <p className="text-f1-silver text-sm mb-4">
                    {mode.description}
                  </p>
                  <div className="flex items-center text-f1-red text-sm font-medium">
                    <span>Start Analysis</span>
                    <ChevronRight size={16} className="ml-1 transform group-hover:translate-x-1 transition-transform" />
                  </div>
                </Link>
              ))}
            </div>
          </div>
          
          {/* Calendar Section */}
          <CalendarView />
        </div>
      </main>
    </div>
  );
};

export default Index;
