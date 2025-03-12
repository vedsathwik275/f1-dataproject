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
from f1_api.data_processor import process_data
from f1_api.visualizations import create_visualization

# Create cache directory if it doesn't exist
CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

class F1Analyzer:
    def __init__(self):
        """Initialize the F1 Analyzer application"""
        self.fastf1_client = FastF1Client(CACHE_DIR)
        self.openf1_client = OpenF1Client()
        self.data_processor = process_data
        self.visualizations = create_visualization
        
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
            'help': self._show_help,
            'exit': self.exit_app
        }

    def run(self):
        """Run the F1 Data Analyzer interface"""
        print("\nStarting F1 Data Analyzer...\n")
        print("🏎️  F1 Data Analyzer 🏎️")
        print("=======================")
        print("Type 'help' to see available commands or 'exit' to quit.\n")
        
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'exit':
                print("\nExiting F1 Data Analyzer... Goodbye! 👋")
                break
            
            elif command == 'help':
                self._show_help()
                
            elif command == 'driver_performance':
                driver = input("Enter driver name (e.g., 'VER', 'HAM'): ").strip().upper()
                year_input = input(f"Enter year (default: {self.current_year}): ").strip() or str(self.current_year)
                gp_name = input("Enter Grand Prix name (e.g., 'Bahrain', 'Monaco'): ").strip()
                session_type = input("Enter session type (e.g., 'R' for race, 'Q' for qualifying, default: 'R'): ").strip() or 'R'
                
                try:
                    year = int(year_input)
                    self.analyze_driver_performance(driver, year, gp_name, session_type)
                except ValueError:
                    print(f"[ERROR] Invalid year format: {year_input}. Please enter a valid year.")
                
            elif command == 'race_analysis':
                self.analyze_race()
                
            elif command == 'compare_drivers':
                self.compare_drivers()
                
            elif command == 'qualifying_analysis':
                self.analyze_qualifying()
                
            elif command == 'list_races':
                year_input = input(f"Enter year (default: {self.current_year}): ").strip() or str(self.current_year)
                try:
                    year = int(year_input)
                    self.list_available_races(year)
                except ValueError:
                    print(f"[ERROR] Invalid year format: {year_input}. Please enter a valid year.")
                
            elif command == 'list_drivers':
                year_input = input(f"Enter year (default: {self.current_year}): ").strip() or str(self.current_year)
                gp_name = input("Enter Grand Prix name (e.g., 'Bahrain', default: most recent): ").strip() or None
                
                try:
                    year = int(year_input)
                    self.list_available_drivers(year, gp_name)
                except ValueError:
                    print(f"[ERROR] Invalid year format: {year_input}. Please enter a valid year.")
                
            else:
                print(f"Unknown command: '{command}'. Type 'help' to see available commands.")

    def analyze_driver_performance(self, driver_code, year, gp_name, session_type='R'):
        """
        Analyze driver performance for a specific race
        
        Args:
            driver_code (str): Driver code (e.g., 'VER', 'HAM')
            year (int): Year of the race
            gp_name (str): Grand Prix name
            session_type (str): Session type (e.g., 'R' for race, 'Q' for qualifying)
            
        Returns:
            str: Path to the output file
        """
        print(f"[CHECKPOINT] Analyzing {driver_code}'s performance at {year} {gp_name} GP ({session_type})")
        
        # 1. Get session data from FastF1
        print(f"[CHECKPOINT] Loading {year} {gp_name} {session_type} session from FastF1...")
        try:
            fastf1_data = self.fastf1_client.get_session_data(year, gp_name, session_type, driver_code)
            if not fastf1_data:
                print(f"[ERROR] No data found for {driver_code} in {year} {gp_name} {session_type}")
                return None
            print("[SUCCESS] Session loaded successfully")
            
            # 2. Extract driver data
            print(f"[CHECKPOINT] Extracting {driver_code}'s data from {year} {gp_name} {session_type}...")
            num_laps = len(fastf1_data.get('laps', []))
            print(f"[SUCCESS] Extracted {num_laps} laps of data for {driver_code}")
            
            # 3. Get OpenF1 data (may not be available for all seasons)
            openf1_data = None
            try:
                # Find the round number if possible
                race_calendar = self.fastf1_client.get_race_calendar(year)
                round_number = None
                
                for race in race_calendar:
                    if race.get('gp_name', '').lower() == gp_name.lower():
                        round_number = race.get('round')
                        break
                
                if round_number:
                    print(f"[CHECKPOINT] Fetching session data for {year} Round {round_number} from OpenF1...")
                    openf1_data = self.openf1_client.get_session_data(year, round_number, gp_name)
                    
                    if not openf1_data or not openf1_data.get('sessions'):
                        print(f"[WARNING] No session data found for {year} Round {round_number}")
                        # For newer seasons, try with just GP name, with no round number
                        if year >= 2023:
                            print(f"[INFO] Trying alternative method for {year} {gp_name}...")
                            openf1_data = self.openf1_client.get_session_data(year, None, gp_name)
                    
                    if openf1_data and openf1_data.get('sessions'):
                        print(f"[SUCCESS] Found {len(openf1_data['sessions'])} sessions from OpenF1")
                    else:
                        print(f"[INFO] No OpenF1 data available for {year} {gp_name}. Using FastF1 data only.")
                else:
                    print(f"[WARNING] Could not determine round number for {year} {gp_name}")
                    # Try with just the GP name
                    openf1_data = self.openf1_client.get_session_data(year, None, gp_name)
                    
            except Exception as e:
                print(f"[WARNING] Error fetching OpenF1 data: {str(e)}. Using FastF1 data only.")
            
            # 4. Process data
            processed_data = self.data_processor(fastf1_data, openf1_data, 'driver_performance')
            
            # 5. Visualize data
            filename_prefix = f"{driver_code}_{year}_{gp_name}_{session_type}"
            output_file = self.visualizations(processed_data, 'driver_performance', filename_prefix)
            
            print(f"Data analysis complete. Visualization saved to: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"[ERROR] Failed to analyze driver performance: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

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
                processed_data = self.data_processor(race_data, openf1_race_data, 'race_analysis')
                visualization_path = self.visualizations(processed_data, 'race_analysis', 
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
                processed_data = self.data_processor([driver1_data, driver2_data], None, 'driver_comparison')
                visualization_path = self.visualizations(processed_data, 'driver_comparison', 
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
                processed_data = self.data_processor(quali_data, openf1_quali_data, 'qualifying_analysis')
                visualization_path = self.visualizations(processed_data, 'qualifying_analysis', 
                                                        f"{year}_{gp_name}_qualifying")
                print(f"Qualifying analysis complete. Visualization saved to: {visualization_path}")
            else:
                print("No qualifying data available for the specified race.")
        except ValueError:
            print("Invalid year format. Please enter a valid year.")
        except Exception as e:
            print(f"Error analyzing qualifying: {e}")

    def list_available_races(self, year):
        """List available races for a given year"""
        print(f"\n[CHECKPOINT] Fetching available races for {year}")
        
        # Get race calendar
        races = self.fastf1_client.get_race_calendar(year)
        
        if races:
            print(f"\nAvailable races for {year}:")
            for idx, race in enumerate(races, 1):
                race_name = race.get('gp_name', race.get('name', f"Race {idx}"))
                race_date = race.get('date', 'Date unknown')
                print(f"{idx}. {race_name} - {race_date}")
        else:
            print(f"No race information available for {year}")

    def list_available_drivers(self, year, gp_name=None):
        """List available drivers for a given year"""
        print(f"\n[CHECKPOINT] Fetching drivers for {year}")
        
        # Get drivers
        drivers = self.fastf1_client.get_drivers(year)
        
        if drivers:
            print(f"\nDrivers for {year} season:")
            for idx, driver in enumerate(drivers, 1):
                print(f"{idx}. {driver['code']} - {driver['name']} ({driver['team']})")
        else:
            print(f"No driver information available for {year}")

    def _show_help(self):
        """Show help information"""
        print("\nAvailable commands:")
        print("  driver_performance - Analyze driver performance for a race")
        print("  race_analysis      - Analyze race results")
        print("  compare_drivers    - Compare multiple drivers' performance")
        print("  qualifying_analysis - Analyze qualifying session results")
        print("  list_races         - List available races for a year")
        print("  list_drivers       - List available drivers for a year/race")
        print("  help               - Show this help message")
        print("  exit               - Exit the application")

    def exit_app(self):
        """Exit the application"""
        print("\nExiting F1 Data Analyzer... Goodbye! 👋")
        sys.exit(0)

def main():
    """Main function to run the application"""
    analyzer = F1Analyzer()
    analyzer.run()

if __name__ == "__main__":
    main() 