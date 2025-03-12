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
from f1_api.historical_data import HistoricalDataManager

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
        self.historical_data = HistoricalDataManager(CACHE_DIR)
        
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
            'multi_season_driver': self.analyze_driver_across_seasons,
            'multi_season_team': self.analyze_team_across_seasons,
            'circuit_history': self.analyze_circuit_history,
            'season_comparison': self.compare_seasons,
            'get_calendar': self.display_calendar,
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
                
            elif command == 'multi_season_driver':
                driver = input("Enter driver name (e.g., 'VER', 'HAM'): ").strip().upper()
                gp_name = input("Enter Grand Prix name to filter by (optional, press Enter to skip): ").strip() or None
                gp_names = [gp_name] if gp_name else None
                self.analyze_driver_across_seasons(driver, gp_names)
                
            elif command == 'multi_season_team':
                team = input("Enter team name (e.g., 'Red Bull Racing', 'Mercedes'): ").strip()
                self.analyze_team_across_seasons(team)
                
            elif command == 'circuit_history':
                gp_name = input("Enter Grand Prix name (e.g., 'Monaco', 'Monza'): ").strip()
                self.analyze_circuit_history(gp_name)
                
            elif command == 'season_comparison':
                self.compare_seasons()
                
            elif command == 'get_calendar':
                year_input = input(f"Enter year (default: {self.current_year}): ").strip() or str(self.current_year)
                try:
                    year = int(year_input)
                    self.display_calendar(year)
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

    def analyze_driver_across_seasons(self, driver_code, gp_names=None):
        """
        Analyze a driver's performance across multiple seasons (2021-2025)
        
        Args:
            driver_code (str): Driver code (e.g., 'VER', 'HAM')
            gp_names (list, optional): List of GP names to filter by
        """
        print(f"\n[CHECKPOINT] Analyzing {driver_code}'s performance across seasons (2021-2025)")
        
        try:
            # Get driver performance history
            performance_history = self.historical_data.get_driver_performance_history(driver_code, gp_names)
            
            if not performance_history or not performance_history.get('seasons'):
                print(f"[ERROR] No historical data found for {driver_code}")
                return
            
            # Print summary of performance by season
            print(f"\n===== {driver_code}'s Performance Across Seasons =====\n")
            
            seasons_data = []
            for year, season in sorted(performance_history['seasons'].items()):
                if 'statistics' in season:
                    stats = season['statistics']
                    seasons_data.append({
                        'year': year,
                        'races': stats.get('races_completed', 0),
                        'points': stats.get('points', 0),
                        'wins': stats.get('wins', 0),
                        'podiums': stats.get('podiums', 0)
                    })
            
            # Create a DataFrame and print
            if seasons_data:
                print(f"{'YEAR':<6} {'RACES':<6} {'POINTS':<8} {'WINS':<6} {'PODIUMS':<8}")
                print("-" * 40)
                
                for season in sorted(seasons_data, key=lambda x: x['year']):
                    print(f"{season['year']:<6} {season['races']:<6} {season['points']:<8.1f} {season['wins']:<6} {season['podiums']:<8}")
                
                # Compare seasons
                comparison = self.historical_data.compare_seasons(driver_code=driver_code)
                
                # Process data for visualization
                processed_data = {
                    'driver_code': driver_code,
                    'seasons': seasons_data,
                    'positions_by_race': comparison.get('positions_by_race', {}),
                    'points_by_season': comparison.get('points_by_season', {}),
                    'wins_by_season': comparison.get('wins_by_season', {}),
                    'podiums_by_season': comparison.get('podiums_by_season', {})
                }
                
                # TODO: Create a visualization of multi-season performance
                # For now, just print some additional details
                print("\n===== Performance Details =====\n")
                
                # Count number of seasons with data
                active_seasons = len([s for s in seasons_data if s['races'] > 0])
                print(f"Seasons active: {active_seasons}")
                
                # Calculate career stats
                total_races = sum(s['races'] for s in seasons_data)
                total_wins = sum(s['wins'] for s in seasons_data)
                total_podiums = sum(s['podiums'] for s in seasons_data)
                total_points = sum(s['points'] for s in seasons_data)
                
                print(f"Total races: {total_races}")
                print(f"Total wins: {total_wins} ({total_wins/total_races*100:.1f}% win rate)")
                print(f"Total podiums: {total_podiums} ({total_podiums/total_races*100:.1f}% podium rate)")
                print(f"Total points: {total_points:.1f}")
                
                # Display best and worst performing seasons
                if seasons_data:
                    best_season = max(seasons_data, key=lambda x: x['points'])
                    print(f"\nBest season: {best_season['year']} - {best_season['points']:.1f} points, {best_season['wins']} wins")
                    
                    active_seasons = [s for s in seasons_data if s['races'] > 0]
                    if active_seasons:
                        worst_season = min(active_seasons, key=lambda x: x['points'])
                        print(f"Worst season: {worst_season['year']} - {worst_season['points']:.1f} points, {worst_season['wins']} wins")
            else:
                print(f"No season statistics available for {driver_code}")
                
        except Exception as e:
            print(f"[ERROR] Failed to analyze multi-season data: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def analyze_team_across_seasons(self, team_name):
        """
        Analyze a team's performance across multiple seasons (2021-2025)
        
        Args:
            team_name (str): Team name
        """
        print(f"\n[CHECKPOINT] Analyzing {team_name}'s performance across seasons (2021-2025)")
        
        try:
            # Get team performance history
            team_history = self.historical_data.get_team_performance_history(team_name)
            
            if not team_history or not team_history.get('seasons'):
                print(f"[ERROR] No historical data found for {team_name}")
                return
            
            # Print summary of performance by season
            print(f"\n===== {team_name} Performance Across Seasons =====\n")
            
            seasons_data = []
            for year, season in sorted(team_history['seasons'].items()):
                if 'statistics' in season:
                    stats = season['statistics']
                    seasons_data.append({
                        'year': year,
                        'races': stats.get('races_completed', 0),
                        'points': stats.get('total_points', 0),
                        'wins': stats.get('wins', 0),
                        'podiums': stats.get('podiums', 0),
                        'drivers': season.get('drivers', [])
                    })
            
            # Create a DataFrame and print
            if seasons_data:
                print(f"{'YEAR':<6} {'RACES':<6} {'POINTS':<8} {'WINS':<6} {'PODIUMS':<8} {'DRIVERS'}")
                print("-" * 70)
                
                for season in sorted(seasons_data, key=lambda x: x['year']):
                    drivers_str = ", ".join([d['driver_code'] for d in season['drivers']])
                    print(f"{season['year']:<6} {season['races']:<6} {season['points']:<8.1f} {season['wins']:<6} {season['podiums']:<8} {drivers_str}")
                
                # Compare seasons
                comparison = self.historical_data.compare_seasons(team_name=team_name)
                
                # Process data for visualization
                processed_data = {
                    'team_name': team_name,
                    'seasons': seasons_data,
                    'points_by_season': comparison.get('points_by_season', {}),
                    'wins_by_season': comparison.get('wins_by_season', {}),
                    'podiums_by_season': comparison.get('podiums_by_season', {})
                }
                
                # TODO: Create a visualization of multi-season performance
                # For now, just print some additional details
                print("\n===== Performance Details =====\n")
                
                # Count number of seasons with data
                active_seasons = len([s for s in seasons_data if s['races'] > 0])
                print(f"Seasons active: {active_seasons}")
                
                # Calculate team stats
                total_races = sum(s['races'] for s in seasons_data)
                total_wins = sum(s['wins'] for s in seasons_data)
                total_podiums = sum(s['podiums'] for s in seasons_data)
                total_points = sum(s['points'] for s in seasons_data)
                
                print(f"Total races: {total_races}")
                print(f"Total wins: {total_wins} ({total_wins/total_races*100:.1f}% win rate if total_races > 0 else 0)")
                print(f"Total podiums: {total_podiums} ({total_podiums/total_races*100:.1f}% podium rate if total_races > 0 else 0)")
                print(f"Total points: {total_points:.1f}")
                
                # Display best and worst performing seasons
                if seasons_data:
                    best_season = max(seasons_data, key=lambda x: x['points'])
                    print(f"\nBest season: {best_season['year']} - {best_season['points']:.1f} points, {best_season['wins']} wins")
                    
                    active_seasons = [s for s in seasons_data if s['races'] > 0]
                    if active_seasons:
                        worst_season = min(active_seasons, key=lambda x: x['points'])
                        print(f"Worst season: {worst_season['year']} - {worst_season['points']:.1f} points, {worst_season['wins']} wins")
            else:
                print(f"No season statistics available for {team_name}")
                
        except Exception as e:
            print(f"[ERROR] Failed to analyze multi-season data: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def analyze_circuit_history(self, gp_name):
        """
        Analyze the history of a specific circuit across seasons
        
        Args:
            gp_name (str): Grand Prix name
        """
        print(f"\n[CHECKPOINT] Analyzing {gp_name} history across seasons (2021-2025)")
        
        try:
            # Get circuit history
            circuit_history = self.historical_data.get_circuit_history(gp_name)
            
            if not circuit_history or not circuit_history.get('seasons'):
                print(f"[ERROR] No historical data found for {gp_name}")
                return
            
            # Print summary of race results by season
            print(f"\n===== {gp_name} Grand Prix History (2021-2025) =====\n")
            
            for year, season in sorted(circuit_history['seasons'].items()):
                print(f"\n{year} {gp_name} Grand Prix ({season.get('date', 'Date unknown')})")
                print("-" * 70)
                
                # Print pole position
                if season.get('pole_position'):
                    pole = season['pole_position']
                    print(f"Pole position: {pole['driver_code']} ({pole['team']})")
                
                # Print race winner
                if season.get('results') and len(season['results']) > 0:
                    winner = next((r for r in season['results'] if r['position'] == 1), None)
                    if winner:
                        print(f"Race winner: {winner['driver_code']} ({winner['team']})")
                
                # Print fastest lap
                if season.get('fastest_lap'):
                    fastest = season['fastest_lap']
                    time_str = str(datetime.fromtimestamp(fastest['time']).strftime('%M:%S.%f'))[:-3]
                    print(f"Fastest lap: {fastest['driver_code']} - {time_str}")
                
                # Print podium
                podium = [r for r in season.get('results', []) if r['position'] and r['position'] <= 3]
                if podium:
                    print("\nPodium:")
                    for p in sorted(podium, key=lambda x: x['position']):
                        print(f"{p['position']}. {p['driver_code']} ({p['team']})")
                
                print()
            
            # TODO: Create a visualization of circuit history
            # For now, just print some additional statistics
            print("\n===== Circuit Statistics =====\n")
            
            # Count winners
            winners = {}
            for _, season in circuit_history['seasons'].items():
                if season.get('results'):
                    winner = next((r for r in season['results'] if r['position'] == 1), None)
                    if winner:
                        driver = winner['driver_code']
                        winners[driver] = winners.get(driver, 0) + 1
            
            if winners:
                print("Most successful drivers at this circuit:")
                for driver, wins in sorted(winners.items(), key=lambda x: x[1], reverse=True):
                    print(f"{driver}: {wins} win(s)")
            
            # Count pole positions
            poles = {}
            for _, season in circuit_history['seasons'].items():
                if season.get('pole_position'):
                    driver = season['pole_position']['driver_code']
                    poles[driver] = poles.get(driver, 0) + 1
            
            if poles:
                print("\nMost pole positions at this circuit:")
                for driver, p_count in sorted(poles.items(), key=lambda x: x[1], reverse=True):
                    print(f"{driver}: {p_count} pole(s)")
                
        except Exception as e:
            print(f"[ERROR] Failed to analyze circuit history: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def compare_seasons(self):
        """
        Compare championship standings across multiple seasons (2021-2025)
        """
        print("\n[CHECKPOINT] Comparing championship standings across seasons (2021-2025)")
        
        try:
            # Get comparison data
            comparison = self.historical_data.compare_seasons()
            
            if not comparison or not comparison.get('driver_champions'):
                print("[ERROR] No championship data available")
                return
            
            # Print driver champions by season
            print("\n===== F1 World Champions (2021-2025) =====\n")
            print(f"{'YEAR':<6} {'DRIVER CHAMPION':<20} {'POINTS':<8} {'CONSTRUCTOR CHAMPION':<25}")
            print("-" * 70)
            
            for year in sorted(comparison.get('years', [])):
                driver_champ = comparison.get('driver_champions', {}).get(year, {})
                team_champ = comparison.get('team_champions', {}).get(year, {})
                
                driver_name = driver_champ.get('name', 'Unknown') if driver_champ else 'Unknown'
                driver_points = driver_champ.get('points', 0) if driver_champ else 0
                team_name = team_champ.get('name', 'Unknown') if team_champ else 'Unknown'
                
                print(f"{year:<6} {driver_name:<20} {driver_points:<8} {team_name:<25}")
            
            # TODO: Create a visualization of championship comparison
            
        except Exception as e:
            print(f"[ERROR] Failed to compare seasons: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def display_calendar(self, year):
        """
        Display the full F1 calendar for a given year with detailed information
        
        Args:
            year (int): The year to display the calendar for
        """
        print(f"\n[CHECKPOINT] Fetching {year} F1 race calendar")
        
        try:
            # Get the race calendar
            calendar = self.fastf1_client.get_race_calendar(year)
            
            if not calendar:
                print(f"[ERROR] No calendar data available for {year}")
                return
            
            # Display calendar in a formatted table
            print(f"\n===== {year} FORMULA 1 RACE CALENDAR =====\n")
            print(f"{'ROUND':<6} {'DATE':<12} {'GRAND PRIX':<30} {'CIRCUIT':<25} {'COUNTRY':<15}")
            print("-" * 90)
            
            for race in sorted(calendar, key=lambda x: x['round']):
                round_num = race.get('round', 'N/A')
                date = race.get('date', 'TBC')
                gp_name = race.get('gp_name', 'Unknown')
                location = race.get('location', 'Unknown')
                country = race.get('country', 'Unknown')
                
                print(f"{round_num:<6} {date:<12} {gp_name:<30} {location:<25} {country:<15}")
            
            # Display upcoming races if applicable
            try:
                current_date = datetime.now().date()
                upcoming_races = [
                    race for race in calendar 
                    if race.get('date') and datetime.strptime(race['date'], '%Y-%m-%d').date() >= current_date
                ]
                
                if upcoming_races and year == self.current_year:
                    next_race = min(upcoming_races, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d').date())
                    days_until = (datetime.strptime(next_race['date'], '%Y-%m-%d').date() - current_date).days
                    
                    print(f"\n[INFO] Next race: {next_race['gp_name']} ({next_race['date']}) - {days_until} days from now")
                    
                    # Show session schedule for next race
                    if 'sessions' in next_race and next_race['sessions']:
                        print("\nSession schedule:")
                        for session_type, session_info in sorted(next_race['sessions'].items()):
                            session_name = {
                                'FP1': 'Practice 1',
                                'FP2': 'Practice 2',
                                'FP3': 'Practice 3',
                                'Q': 'Qualifying',
                                'S': 'Sprint',
                                'R': 'Race'
                            }.get(session_type, session_type)
                            
                            session_date = session_info.get('date', 'TBC')
                            session_time = session_info.get('time', 'TBC')
                            print(f"  {session_name:<12}: {session_date} {session_time}")
            except Exception as e:
                # If there's any error in showing upcoming races, just skip it
                pass
                
        except Exception as e:
            print(f"[ERROR] Failed to display calendar: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _show_help(self):
        """Show help information"""
        print("\nAvailable commands:")
        print("  driver_performance   - Analyze driver performance for a race")
        print("  race_analysis        - Analyze race results")
        print("  compare_drivers      - Compare multiple drivers' performance")
        print("  qualifying_analysis  - Analyze qualifying session results")
        print("  list_races           - List available races for a year")
        print("  list_drivers         - List available drivers for a year/race")
        print("  multi_season_driver  - Analyze a driver's performance across multiple seasons (2021-2025)")
        print("  multi_season_team    - Analyze a team's performance across multiple seasons (2021-2025)")
        print("  circuit_history      - Analyze a circuit's history across multiple seasons (2021-2025)")
        print("  season_comparison    - Compare championship standings across multiple seasons (2021-2025)")
        print("  get_calendar         - Display the full F1 calendar for a year")
        print("  help                 - Show this help message")
        print("  exit                 - Exit the application")

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