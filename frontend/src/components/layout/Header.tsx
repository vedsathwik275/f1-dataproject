
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, ChevronDown } from 'lucide-react';

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'bg-f1-darker/90 backdrop-blur-md shadow-md'
          : 'bg-transparent'
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <span className="text-f1-red font-titillium font-bold text-2xl tracking-tight">F1</span>
              <span className="text-white font-titillium ml-1 mr-1 text-2xl font-light">Analytics</span>
              <span className="text-f1-red font-titillium font-bold text-2xl tracking-tight">Hub</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/" className="racing-underline text-white hover:text-f1-red transition-colors duration-200">
              Dashboard
            </Link>
            <div className="relative group">
              <button className="flex items-center racing-underline text-white hover:text-f1-red transition-colors duration-200">
                Analyses
                <ChevronDown size={16} className="ml-1" />
              </button>
              <div className="absolute left-0 mt-2 w-48 rounded-md shadow-lg bg-f1-dark border border-f1-gray/20 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform origin-top-left">
                <div className="py-1">
                  <Link to="/driver-analysis" className="block px-4 py-2 text-sm text-white hover:bg-f1-gray/20 hover:text-f1-red">
                    Driver Performance
                  </Link>
                  <Link to="/race-analysis" className="block px-4 py-2 text-sm text-white hover:bg-f1-gray/20 hover:text-f1-red">
                    Race Analysis
                  </Link>
                  <Link to="/driver-comparison" className="block px-4 py-2 text-sm text-white hover:bg-f1-gray/20 hover:text-f1-red">
                    Driver Comparison
                  </Link>
                  <Link to="/qualifying-analysis" className="block px-4 py-2 text-sm text-white hover:bg-f1-gray/20 hover:text-f1-red">
                    Qualifying Analysis
                  </Link>
                </div>
              </div>
            </div>
            <Link to="/calendar" className="racing-underline text-white hover:text-f1-red transition-colors duration-200">
              Calendar
            </Link>
            <Link to="/about" className="racing-underline text-white hover:text-f1-red transition-colors duration-200">
              About
            </Link>
          </nav>

          {/* Mobile menu button */}
          <button
            onClick={toggleMobileMenu}
            className="md:hidden text-white hover:text-f1-red focus:outline-none"
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div
        className={`md:hidden bg-f1-darker/95 backdrop-blur-md overflow-hidden transition-all duration-300 ease-in-out ${
          isMobileMenuOpen ? 'max-h-96' : 'max-h-0'
        }`}
      >
        <div className="container mx-auto px-4 py-2">
          <Link to="/" className="block py-3 text-white hover:text-f1-red" onClick={toggleMobileMenu}>
            Dashboard
          </Link>
          <Link to="/driver-analysis" className="block py-3 text-white hover:text-f1-red" onClick={toggleMobileMenu}>
            Driver Performance
          </Link>
          <Link to="/race-analysis" className="block py-3 text-white hover:text-f1-red" onClick={toggleMobileMenu}>
            Race Analysis
          </Link>
          <Link to="/driver-comparison" className="block py-3 text-white hover:text-f1-red" onClick={toggleMobileMenu}>
            Driver Comparison
          </Link>
          <Link to="/qualifying-analysis" className="block py-3 text-white hover:text-f1-red" onClick={toggleMobileMenu}>
            Qualifying Analysis
          </Link>
          <Link to="/calendar" className="block py-3 text-white hover:text-f1-red" onClick={toggleMobileMenu}>
            Calendar
          </Link>
          <Link to="/about" className="block py-3 text-white hover:text-f1-red" onClick={toggleMobileMenu}>
            About
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
