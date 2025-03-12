#!/usr/bin/env python3
"""
F1 Data Analyzer - Main Application

This interactive command-line tool allows users to analyze and visualize Formula 1 data
using both the FastF1 and OpenF1 APIs.
"""

import argparse
import os
import sys
from datetime import datetime

# Import our modules
from f1_api.fastf1_client import FastF1Client
from f1_api.openf1_client import OpenF1Client
from f1_api.visualizations import create_visualization
from f1_api.data_processor import process_data

# Create cache directory if it doesn't exist
CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

class F1Analyzer:
    def __init__(self):
        """Initialize the F1 Analyzer application"""
        self.fastf1_client = FastF1Client(CACHE_DIR)
        self.openf1_client = OpenF1Client()
        
        # Current year for default values
        self.current_year = datetime.now().year
        
        # Available commands
        self.commands = {
            'driver_performance': self.analyze_driver_performance,
            'race_analysis': self.analyze_race,
            'compare_drivers': self.compare_drivers,
            'qualifying_analysis': self.analyze_qualifying,
            'available_races': self.list_available_races,
            'available_drivers': self.list_available_drivers,
            'help': self.show_help,
            'exit': self.exit_app
        }
        
        # Welcome message
        print("\n🏎️  F1 Data Analyzer 🏎️")
        print("=======================")
        print("Type 'help' to see available commands or 'exit' to quit.\n")

    def run_interactive(self):
        """Run the application in interactive mode"""
        while True:
            try:
                command = input("\nEnter command: ").strip().lower()
                
                if command in self.commands:
                    self.commands[command]()
                else:
                    print(f"Unknown command: {command}")
                    self.show_help()
            except KeyboardInterrupt:
                print("\nExiting F1 Data Analyzer...")
                sys.exit(0)
            except Exception as e:
                print(f"Error: {e}")
    
    def analyze_driver_performance(self):
        """Analyze a specific driver's performance for a race"""
        driver = input("Enter driver name (e.g., 'VER', 'HAM'): ").strip().upper()
        year = input(f"Enter year (default: {self.current_year}): ").strip() or self.current_year
        gp_name = input("Enter Grand Prix name (e.g., 'Bahrain', 'Monaco'): ").strip()
        session_type = input("Enter session type (e.g., 'R' for race, 'Q' for qualifying, default: 'R'): ").strip() or 'R'
        
        try:
            year = int(year)
            print(f"\n[CHECKPOINT] Analyzing {driver}'s performance at {year} {gp_name} GP ({session_type})")
            
            # Get data from both APIs
            fastf1_data = self.fastf1_client.get_driver_session_data(year, gp_name, driver, session_type)
            round_number = self.fastf1_client.get_round_number(year, gp_name)
            openf1_data = self.openf1_client.get_driver_data(year, round_number, driver)
            
            # Process and visualize data
            if fastf1_data is not None:
                processed_data = process_data(fastf1_data, openf1_data, 'driver_performance')
                visualization_path = create_visualization(processed_data, 'driver_performance', 
                                                          f"{driver}_{year}_{gp_name}_{session_type}")
                print(f"Data analysis complete. Visualization saved to: {visualization_path}")
            else:
                print("No data available for the specified parameters.")
        except ValueError:
            print("Invalid year format. Please enter a valid year.")
        except Exception as e:
            print(f"Error analyzing driver performance: {e}")

    def analyze_race(self):
        """Analyze a specific race"""
        year = input(f"Enter year (default: {self.current_year}): ").strip() or self.current_year
        gp_name = input("Enter Grand Prix name (e.g., 'Bahrain', 'Monaco'): ").strip()
        
        try:
            year = int(year)
            print(f"\n[CHECKPOINT] Analyzing {year} {gp_name} Grand Prix")
            
            # Get data
            race_data = self.fastf1_client.get_race_data(year, gp_name)
            round_number = self.fastf1_client.get_round_number(year, gp_name)
            openf1_race_data = self.openf1_client.get_session_data(year, round_number)
            
            # Process and visualize
            if race_data is not None:
                processed_data = process_data(race_data, openf1_race_data, 'race_analysis')
                visualization_path = create_visualization(processed_data, 'race_analysis', 
                                                          f"{year}_{gp_name}_race")
                print(f"Race analysis complete. Visualization saved to: {visualization_path}")
            else:
                print("No data available for the specified race.")
        except ValueError:
            print("Invalid year format. Please enter a valid year.")
        except Exception as e:
            print(f"Error analyzing race: {e}")

    def compare_drivers(self):
        """Compare two drivers' performance"""
        driver1 = input("Enter first driver code (e.g., 'VER'): ").strip().upper()
        driver2 = input("Enter second driver code (e.g., 'HAM'): ").strip().upper()
        year = input(f"Enter year (default: {self.current_year}): ").strip() or self.current_year
        gp_name = input("Enter Grand Prix name (e.g., 'Bahrain'): ").strip()
        session_type = input("Enter session type (e.g., 'R' for race, 'Q' for qualifying, default: 'R'): ").strip() or 'R'
        
        try:
            year = int(year)
            print(f"\n[CHECKPOINT] Comparing {driver1} vs {driver2} at {year} {gp_name} GP ({session_type})")
            
            # Get data for both drivers
            driver1_data = self.fastf1_client.get_driver_session_data(year, gp_name, driver1, session_type)
            driver2_data = self.fastf1_client.get_driver_session_data(year, gp_name, driver2, session_type)
            
            # If data exists for both drivers, process and visualize
            if driver1_data is not None and driver2_data is not None:
                processed_data = process_data([driver1_data, driver2_data], None, 'driver_comparison')
                visualization_path = create_visualization(processed_data, 'driver_comparison', 
                                                          f"{driver1}_vs_{driver2}_{year}_{gp_name}_{session_type}")
                print(f"Driver comparison complete. Visualization saved to: {visualization_path}")
            else:
                print("No data available for one or both drivers.")
        except ValueError:
            print("Invalid year format. Please enter a valid year.")
        except Exception as e:
            print(f"Error comparing drivers: {e}")

    def analyze_qualifying(self):
        """Analyze qualifying session"""
        year = input(f"Enter year (default: {self.current_year}): ").strip() or self.current_year
        gp_name = input("Enter Grand Prix name (e.g., 'Bahrain'): ").strip()
        
        try:
            year = int(year)
            print(f"\n[CHECKPOINT] Analyzing {year} {gp_name} Qualifying")
            
            # Get qualifying data
            quali_data = self.fastf1_client.get_qualifying_data(year, gp_name)
            round_number = self.fastf1_client.get_round_number(year, gp_name)
            openf1_quali_data = self.openf1_client.get_session_data(year, round_number, 'Q')
            
            # Process and visualize
            if quali_data is not None:
                processed_data = process_data(quali_data, openf1_quali_data, 'qualifying_analysis')
                visualization_path = create_visualization(processed_data, 'qualifying_analysis', 
                                                          f"{year}_{gp_name}_qualifying")
                print(f"Qualifying analysis complete. Visualization saved to: {visualization_path}")
            else:
                print("No qualifying data available for the specified race.")
        except ValueError:
            print("Invalid year format. Please enter a valid year.")
        except Exception as e:
            print(f"Error analyzing qualifying: {e}")

    def list_available_races(self):
        """List available races for a given year"""
        year = input(f"Enter year (default: {self.current_year}): ").strip() or self.current_year
        
        try:
            year = int(year)
            print(f"\n[CHECKPOINT] Fetching available races for {year}")
            
            # Get race calendar
            races = self.fastf1_client.get_race_calendar(year)
            
            if races:
                print(f"\nAvailable races for {year}:")
                for idx, race in enumerate(races, 1):
                    print(f"{idx}. {race['name']} - {race['date']}")
            else:
                print(f"No race information available for {year}")
        except ValueError:
            print("Invalid year format. Please enter a valid year.")
        except Exception as e:
            print(f"Error listing races: {e}")

    def list_available_drivers(self):
        """List available drivers for a given year"""
        year = input(f"Enter year (default: {self.current_year}): ").strip() or self.current_year
        
        try:
            year = int(year)
            print(f"\n[CHECKPOINT] Fetching drivers for {year}")
            
            # Get drivers
            drivers = self.fastf1_client.get_drivers(year)
            
            if drivers:
                print(f"\nDrivers for {year} season:")
                for idx, driver in enumerate(drivers, 1):
                    print(f"{idx}. {driver['code']} - {driver['name']} ({driver['team']})")
            else:
                print(f"No driver information available for {year}")
        except ValueError:
            print("Invalid year format. Please enter a valid year.")
        except Exception as e:
            print(f"Error listing drivers: {e}")

    def show_help(self):
        """Show help information"""
        print("\nAvailable commands:")
        print("  driver_performance - Analyze a specific driver's performance for a race")
        print("  race_analysis      - Analyze a specific race")
        print("  compare_drivers    - Compare two drivers' performance")
        print("  qualifying_analysis - Analyze qualifying session")
        print("  available_races    - List available races for a given year")
        print("  available_drivers  - List available drivers for a given year")
        print("  help               - Show this help message")
        print("  exit               - Exit the application")

    def exit_app(self):
        """Exit the application"""
        print("\nExiting F1 Data Analyzer... Goodbye! 👋")
        sys.exit(0)

def main():
    """Main function to run the application"""
    analyzer = F1Analyzer()
    analyzer.run_interactive()

if __name__ == "__main__":
    main() 