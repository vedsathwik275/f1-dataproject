
import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

interface FeaturedItem {
  id: string;
  title: string;
  description: string;
  image: string;
  path: string;
}

const FeaturedAnalysis: React.FC = () => {
  const featuredItems: FeaturedItem[] = [
    {
      id: '1',
      title: 'Monaco GP 2023 - Lap Time Analysis',
      description: 'Dive into lap time comparisons between the top 5 drivers in Monaco.',
      image: 'https://via.placeholder.com/600x300',
      path: '/driver-analysis',
    },
    {
      id: '2',
      title: 'Max vs Lewis - Silverstone Battle',
      description: 'Head-to-head comparison of Verstappen and Hamilton at the British GP.',
      image: 'https://via.placeholder.com/600x300',
      path: '/driver-comparison',
    },
    {
      id: '3',
      title: 'Monza 2023 Qualifying - Sector Times',
      description: 'Detailed sector time analysis from the Italian GP qualifying session.',
      image: 'https://via.placeholder.com/600x300',
      path: '/qualifying-analysis',
    },
  ];

  return (
    <div className="py-8">
      <div className="flex items-baseline justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Featured Analyses</h2>
        <Link 
          to="/history" 
          className="text-f1-red hover:text-f1-red/80 text-sm font-medium flex items-center transition-colors"
        >
          View All
          <ArrowRight size={14} className="ml-1" />
        </Link>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {featuredItems.map((item) => (
          <Link 
            key={item.id} 
            to={item.path}
            className="card-glass overflow-hidden group transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="relative h-40 overflow-hidden">
              <img 
                src={item.image} 
                alt={item.title} 
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" 
              />
              <div className="absolute inset-0 bg-gradient-to-t from-f1-darker via-transparent to-transparent"></div>
            </div>
            
            <div className="p-4">
              <h3 className="text-lg font-bold text-white mb-2 group-hover:text-f1-red transition-colors">
                {item.title}
              </h3>
              <p className="text-f1-silver text-sm mb-3">
                {item.description}
              </p>
              <div className="flex items-center text-f1-red text-sm font-medium">
                <span>View Analysis</span>
                <ArrowRight size={14} className="ml-1 transform group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default FeaturedAnalysis;
