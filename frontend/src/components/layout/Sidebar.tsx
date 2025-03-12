
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  BarChart3, 
  Users, 
  Flag, 
  Timer,
  Calendar, 
  Home, 
  ChevronRight,
  ChevronLeft
} from 'lucide-react';

interface SidebarProps {
  isCollapsed: boolean;
  toggleSidebar: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isCollapsed, toggleSidebar }) => {
  const location = useLocation();
  
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <aside 
      className={`fixed left-0 top-16 bottom-0 bg-f1-charcoal border-r border-f1-gray/20 transition-all duration-300 ease-in-out z-40 ${
        isCollapsed ? 'w-16' : 'w-60'
      }`}
    >
      <div className="h-full flex flex-col justify-between py-4">
        <div>
          <div className="px-4 mb-6 flex items-center justify-between">
            {!isCollapsed && (
              <h3 className="text-f1-lightgray font-medium text-sm uppercase tracking-wider">
                Navigation
              </h3>
            )}
            <button 
              onClick={toggleSidebar}
              className="text-f1-lightgray hover:text-white p-1 rounded-md hover:bg-f1-gray/20 transition-colors"
            >
              {isCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
            </button>
          </div>
          
          <nav className="space-y-1 px-2">
            <Link 
              to="/" 
              className={`sidebar-item ${isActive('/') && 'active'}`}
            >
              <Home size={20} className={isActive('/') ? 'text-f1-red' : 'text-f1-lightgray'} />
              {!isCollapsed && <span>Dashboard</span>}
            </Link>
            
            <Link 
              to="/driver-analysis" 
              className={`sidebar-item ${isActive('/driver-analysis') && 'active'}`}
            >
              <Users size={20} className={isActive('/driver-analysis') ? 'text-f1-red' : 'text-f1-lightgray'} />
              {!isCollapsed && <span>Driver Analysis</span>}
            </Link>
            
            <Link 
              to="/race-analysis" 
              className={`sidebar-item ${isActive('/race-analysis') && 'active'}`}
            >
              <Flag size={20} className={isActive('/race-analysis') ? 'text-f1-red' : 'text-f1-lightgray'} />
              {!isCollapsed && <span>Race Analysis</span>}
            </Link>
            
            <Link 
              to="/driver-comparison" 
              className={`sidebar-item ${isActive('/driver-comparison') && 'active'}`}
            >
              <BarChart3 size={20} className={isActive('/driver-comparison') ? 'text-f1-red' : 'text-f1-lightgray'} />
              {!isCollapsed && <span>Driver Comparison</span>}
            </Link>
            
            <Link 
              to="/qualifying-analysis" 
              className={`sidebar-item ${isActive('/qualifying-analysis') && 'active'}`}
            >
              <Timer size={20} className={isActive('/qualifying-analysis') ? 'text-f1-red' : 'text-f1-lightgray'} />
              {!isCollapsed && <span>Qualifying</span>}
            </Link>
            
            <Link 
              to="/calendar" 
              className={`sidebar-item ${isActive('/calendar') && 'active'}`}
            >
              <Calendar size={20} className={isActive('/calendar') ? 'text-f1-red' : 'text-f1-lightgray'} />
              {!isCollapsed && <span>Calendar</span>}
            </Link>
          </nav>
        </div>
        
        <div className="px-2">
          {!isCollapsed && (
            <div className="border-t border-f1-gray/20 pt-4 px-2 mb-4">
              <p className="text-xs text-f1-lightgray/60">
                Data powered by FastF1 and OpenF1
              </p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
