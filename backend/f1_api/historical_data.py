"""
Historical Data Module

This module provides functions for retrieving and analyzing historical F1 data
across multiple seasons (2021-2025).
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import fastf1
import logging
import time
import json
import pickle
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('f1_historical')

# Define the seasons we want to analyze
HISTORICAL_SEASONS = [2021, 2022, 2023, 2024, 2025]

class HistoricalDataManager:
    """Manager for retrieving and processing historical F1 data across multiple seasons."""
    
    def __init__(self, cache_dir='cache'):
        """
        Initialize the historical data manager
        
        Args:
            cache_dir (str): Directory to use for caching FastF1 data
        """
        self.cache_dir = cache_dir
        self.historical_cache_dir = os.path.join(cache_dir, 'historical')
        
        # Create cache directories
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        if not os.path.exists(self.historical_cache_dir):
            os.makedirs(self.historical_cache_dir)
            
        fastf1.Cache.enable_cache(cache_dir)
        
        # Initialize data storage
        self.calendars = {}  # Store race calendars by year
        self.driver_standings = {}  # Store driver standings by year
        self.team_standings = {}  # Store team standings by year
        
        # Load calendars from cache if available
        self._load_calendars_from_cache()
        
    def _load_calendars_from_cache(self):
        """Load cached race calendars if available"""
        cache_file = os.path.join(self.historical_cache_dir, 'calendars.pkl')
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    self.calendars = pickle.load(f)
                logger.info(f"Loaded cached calendars for {len(self.calendars)} seasons")
            except Exception as e:
                logger.warning(f"Failed to load cached calendars: {str(e)}")
                
    def _save_calendars_to_cache(self):
        """Save race calendars to cache"""
        cache_file = os.path.join(self.historical_cache_dir, 'calendars.pkl')
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(self.calendars, f)
            logger.info(f"Saved calendars for {len(self.calendars)} seasons to cache")
        except Exception as e:
            logger.warning(f"Failed to save calendars to cache: {str(e)}")
        
    def get_all_seasons_calendars(self):
        """
        Retrieve race calendars for all historical seasons (2021-2025)
        
        Returns:
            dict: Dictionary with year as key and calendar data as value
        """
        # If we already have all the calendars loaded, return them
        if len(self.calendars) == len(HISTORICAL_SEASONS):
            logger.info("Using cached race calendars")
            return self.calendars
        
        logger.info(f"Retrieving race calendars for seasons {HISTORICAL_SEASONS}")
        print("Loading race calendars for all seasons... ", end="")
        
        missing_years = [year for year in HISTORICAL_SEASONS if year not in self.calendars]
        for year in missing_years:
            try:
                schedule = fastf1.get_event_schedule(year)
                
                if schedule.empty:
                    logger.warning(f"No race calendar found for {year}")
                    self.calendars[year] = []
                    continue
                
                calendar = []
                for index, event in schedule.iterrows():
                    race_data = {
                        'round': event['RoundNumber'],
                        'gp_name': event['EventName'],
                        'country': event['Country'],
                        'location': event['Location'],
                        'date': event['EventDate'].strftime('%Y-%m-%d') if pd.notna(event['EventDate']) else None,
                        'sessions': {}
                    }
                    
                    # Add session information if available
                    for session_type in ['FP1', 'FP2', 'FP3', 'Q', 'S', 'R']:
                        if f"{session_type}Date" in event and pd.notna(event[f"{session_type}Date"]):
                            race_data['sessions'][session_type] = {
                                'date': event[f"{session_type}Date"].strftime('%Y-%m-%d'),
                                'time': event[f"{session_type}Time"].strftime('%H:%M:%S') if pd.notna(event[f"{session_type}Time"]) else None
                            }
                    
                    calendar.append(race_data)
                
                logger.info(f"Found {len(calendar)} races in {year} calendar")
                self.calendars[year] = calendar
                
            except Exception as e:
                logger.error(f"Error fetching race calendar for {year}: {str(e)}")
                self.calendars[year] = []
        
        # Save calendars to cache
        self._save_calendars_to_cache()
        print("Done")
        return self.calendars
    
    def _get_driver_cache_path(self, driver_code):
        """Get the cache file path for a driver's performance history"""
        return os.path.join(self.historical_cache_dir, f"driver_{driver_code}.pkl")
    
    def get_driver_performance_history(self, driver_code, gp_names=None):
        """
        Get a driver's performance history across multiple seasons
        
        Args:
            driver_code (str): Driver code (e.g., 'VER', 'HAM')
            gp_names (list, optional): List of GP names to filter by
            
        Returns:
            dict: Driver performance history across seasons
        """
        logger.info(f"Retrieving performance history for {driver_code} across {HISTORICAL_SEASONS}")
        
        # Create cache key and file
        cache_file = self._get_driver_cache_path(driver_code)
        print(f"\nGathering data for {driver_code} across seasons 2021-2025...")
        
        # Check if we have cached data for this driver
        performance_history = None
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    performance_history = pickle.load(f)
                logger.info(f"Loaded cached performance history for {driver_code}")
                print(f"Found cached data for {driver_code}")
            except Exception as e:
                logger.warning(f"Failed to load cached data for {driver_code}: {str(e)}")
                performance_history = None
        
        # If we have cached data and no specific GP filter, use the cached data
        if performance_history and not gp_names:
            return performance_history
            
        # Get calendars if not already loaded
        if not self.calendars:
            self.get_all_seasons_calendars()
        
        # Initialize performance history if needed
        if not performance_history:
            performance_history = {
                'driver': driver_code,
                'seasons': {}
            }
        
        # Add a flag for interrupted operations
        interrupted = False
        
        print(f"\nLoading season data for {driver_code}...")
        total_races = sum(len(self.calendars[year]) for year in HISTORICAL_SEASONS if year in self.calendars)
        processed_races = 0
        
        for year in HISTORICAL_SEASONS:
            # Skip years we've already processed if we're not filtering by GP
            if year in performance_history['seasons'] and not gp_names:
                processed_races += len(self.calendars[year]) if year in self.calendars else 0
                continue
                
            season_data = performance_history['seasons'].get(year, {
                'year': year,
                'races': []
            })
            
            # Initialize empty races list if it doesn't exist
            if 'races' not in season_data:
                season_data['races'] = []
            
            # Find all races for this year
            if year in self.calendars and self.calendars[year]:
                # Get race names we've already processed
                processed_race_names = [race['gp_name'] for race in season_data.get('races', [])]
                
                for race in self.calendars[year]:
                    gp_name = race['gp_name']
                    
                    # Skip if we've already processed this race and we're not filtering
                    if gp_name in processed_race_names and not gp_names:
                        processed_races += 1
                        continue
                        
                    # Filter by GP names if specified
                    if gp_names and gp_name not in gp_names:
                        processed_races += 1
                        continue
                    
                    # Show progress
                    print(f"\rProcessing: {year} {gp_name} ({processed_races}/{total_races} races)", end="")
                    
                    try:
                        # Try to load the session with a timeout
                        start_time = time.time()
                        session = fastf1.get_session(year, gp_name, 'R')
                        
                        # Only load basic data (not full telemetry) to speed things up
                        session.load(laps=False, telemetry=False, weather=False)
                        
                        # Check for timeout or keyboard interrupt
                        if time.time() - start_time > 30:  # 30 second timeout per race
                            logger.warning(f"Timeout loading {year} {gp_name}, skipping")
                            processed_races += 1
                            continue
                        
                        # Check if driver participated
                        if driver_code in session.results['Abbreviation'].values:
                            # Get driver result
                            driver_results = session.results[session.results['Abbreviation'] == driver_code]
                            driver_result = None
                            
                            if not driver_results.empty:
                                result_row = driver_results.iloc[0]
                                driver_result = {
                                    'position': int(result_row['Position']) if pd.notna(result_row['Position']) else None,
                                    'points': float(result_row['Points']) if pd.notna(result_row['Points']) else 0,
                                    'status': result_row['Status']
                                }
                            
                            # Get qualifying position if easily available
                            quali_position = None
                            if 'GridPosition' in driver_results.columns:
                                quali_position = int(driver_results.iloc[0]['GridPosition']) if pd.notna(driver_results.iloc[0]['GridPosition']) else None
                            
                            # Compile race data without detailed lap analysis (for speed)
                            race_data = {
                                'gp_name': gp_name,
                                'round': race['round'],
                                'date': race['date'],
                                'country': race['country'],
                                'result': driver_result,
                                'qualifying': quali_position,
                                'laps_completed': int(driver_results.iloc[0]['LapsCompleted']) if 'LapsCompleted' in driver_results.columns and pd.notna(driver_results.iloc[0]['LapsCompleted']) else 0
                            }
                            
                            # Add to season data
                            if race_data not in season_data['races']:
                                season_data['races'].append(race_data)
                            
                            logger.info(f"Added {year} {gp_name} data for {driver_code}")
                        else:
                            logger.info(f"Driver {driver_code} did not participate in {year} {gp_name}")
                            
                    except KeyboardInterrupt:
                        logger.warning("Operation interrupted by user")
                        print("\nOperation interrupted. Saving partial results...")
                        interrupted = True
                        break
                    except Exception as e:
                        logger.warning(f"Could not load data for {year} {gp_name}: {str(e)}")
                    
                    processed_races += 1
                
                if interrupted:
                    break
            
            # Calculate season statistics
            if season_data.get('races'):
                points = sum(race['result']['points'] for race in season_data['races'] if race.get('result') and 'points' in race['result'])
                podiums = sum(1 for race in season_data['races'] if race.get('result') and race['result'].get('position') and race['result']['position'] <= 3)
                wins = sum(1 for race in season_data['races'] if race.get('result') and race['result'].get('position') == 1)
                
                season_data['statistics'] = {
                    'points': points,
                    'podiums': podiums,
                    'wins': wins,
                    'races_completed': len(season_data['races'])
                }
                
                performance_history['seasons'][year] = season_data
            
            if interrupted:
                break
        
        print("\nData collection complete.")
        
        # Save to cache if we have data and we're not just filtering
        if performance_history['seasons'] and not gp_names:
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(performance_history, f)
                logger.info(f"Saved performance history for {driver_code} to cache")
            except Exception as e:
                logger.warning(f"Failed to save performance history to cache: {str(e)}")
        
        return performance_history
    
    def get_circuit_history(self, gp_name):
        """
        Get historical data for a specific circuit across seasons
        
        Args:
            gp_name (str): Grand Prix name
            
        Returns:
            dict: Circuit historical data
        """
        logger.info(f"Retrieving circuit history for {gp_name} across {HISTORICAL_SEASONS}")
        print(f"\nGathering circuit history for {gp_name}...")
        
        # Get calendars if not already loaded
        if not self.calendars:
            self.get_all_seasons_calendars()
        
        circuit_history = {
            'gp_name': gp_name,
            'seasons': {}
        }
        
        total_seasons = len(HISTORICAL_SEASONS)
        processed_seasons = 0
        
        for year in HISTORICAL_SEASONS:
            processed_seasons += 1
            print(f"\rProcessing {year} data ({processed_seasons}/{total_seasons} seasons)", end="")
            
            if year in self.calendars and self.calendars[year]:
                # Find this GP in the calendar
                gp_events = [race for race in self.calendars[year] if race['gp_name'] == gp_name]
                
                if not gp_events:
                    logger.info(f"{gp_name} not found in {year} calendar")
                    continue
                
                race = gp_events[0]
                
                try:
                    # Load the race session
                    session = fastf1.get_session(year, gp_name, 'R')
                    session.load(laps=False, telemetry=False, weather=False)
                    
                    # Get results
                    results = []
                    for _, row in session.results.iterrows():
                        result = {
                            'position': int(row['Position']) if pd.notna(row['Position']) else None,
                            'driver_code': row['Abbreviation'],
                            'driver_name': f"{row['FirstName']} {row['LastName']}",
                            'team': row['TeamName'],
                            'status': row['Status'],
                            'points': float(row['Points']) if pd.notna(row['Points']) else 0
                        }
                        results.append(result)
                    
                    # Get pole position and fastest lap
                    pole_position = None
                    try:
                        if 'GridPosition' in session.results.columns:
                            # Use grid position from race results if available
                            pole_driver_row = session.results[session.results['GridPosition'] == 1]
                            if not pole_driver_row.empty:
                                pole_driver = pole_driver_row.iloc[0]
                                pole_position = {
                                    'driver_code': pole_driver['Abbreviation'],
                                    'driver_name': f"{pole_driver['FirstName']} {pole_driver['LastName']}",
                                    'team': pole_driver['TeamName']
                                }
                    except:
                        pass
                    
                    # Compile season data
                    season_data = {
                        'year': year,
                        'date': race['date'],
                        'results': results,
                        'pole_position': pole_position
                    }
                    
                    circuit_history['seasons'][year] = season_data
                    logger.info(f"Added {year} {gp_name} circuit history")
                    
                except Exception as e:
                    logger.warning(f"Could not load data for {year} {gp_name}: {str(e)}")
        
        print("\nData collection complete.")
        return circuit_history
    
    def get_team_performance_history(self, team_name):
        """
        Get a team's performance history across multiple seasons
        
        Args:
            team_name (str): Team name
            
        Returns:
            dict: Team performance history across seasons
        """
        logger.info(f"Retrieving performance history for {team_name} across {HISTORICAL_SEASONS}")
        print(f"\nGathering data for {team_name} across seasons 2021-2025...")
        
        # Cache path for team data
        cache_file = os.path.join(self.historical_cache_dir, f"team_{team_name.replace(' ', '_')}.pkl")
        
        # Check if we have cached data for this team
        team_history = None
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    team_history = pickle.load(f)
                logger.info(f"Loaded cached performance history for {team_name}")
                print(f"Found cached data for {team_name}")
                return team_history
            except Exception as e:
                logger.warning(f"Failed to load cached data for {team_name}: {str(e)}")
                team_history = None
        
        # Get calendars if not already loaded
        if not self.calendars:
            self.get_all_seasons_calendars()
        
        team_history = {
            'team': team_name,
            'seasons': {}
        }
        
        # Team name variations
        team_variations = [team_name]
        if team_name == "Red Bull Racing":
            team_variations.extend(["Red Bull", "Red Bull Racing Honda"])
        elif team_name == "Mercedes":
            team_variations.extend(["Mercedes-AMG Petronas", "Mercedes-AMG Petronas F1 Team"])
        elif team_name == "Ferrari":
            team_variations.extend(["Scuderia Ferrari", "Scuderia Ferrari Mission Winnow"])
        elif team_name == "McLaren":
            team_variations.extend(["McLaren F1 Team", "McLaren Mercedes"])
        elif team_name == "Aston Martin":
            team_variations.extend(["Aston Martin Aramco", "Racing Point"])
        elif team_name == "Alpine":
            team_variations.extend(["Alpine F1 Team", "Renault"])
        
        total_seasons = len(HISTORICAL_SEASONS)
        processed_seasons = 0
        
        for year in HISTORICAL_SEASONS:
            processed_seasons += 1
            print(f"\rProcessing {year} data ({processed_seasons}/{total_seasons} seasons)", end="")
            
            season_data = {
                'year': year,
                'races': [],
                'drivers': []
            }
            
            if year in self.calendars and self.calendars[year]:
                try:
                    # Get first race to find team drivers
                    first_race = self.calendars[year][0]['gp_name']
                    first_session = fastf1.get_session(year, first_race, 'R')
                    first_session.load(laps=False, telemetry=False, weather=False)
                    
                    # Find team drivers
                    team_drivers = []
                    for _, driver in first_session.results.iterrows():
                        if any(team_var in driver['TeamName'] for team_var in team_variations):
                            team_drivers.append({
                                'driver_code': driver['Abbreviation'],
                                'driver_name': f"{driver['FirstName']} {driver['LastName']}"
                            })
                    
                    season_data['drivers'] = team_drivers
                    
                    # Get performance for each race
                    for race in self.calendars[year]:
                        gp_name = race['gp_name']
                        
                        try:
                            # Load the race session
                            session = fastf1.get_session(year, gp_name, 'R')
                            session.load(laps=False, telemetry=False, weather=False)
                            
                            # Find team results
                            team_results = []
                            for _, driver in session.results.iterrows():
                                if any(team_var in driver['TeamName'] for team_var in team_variations):
                                    result = {
                                        'driver_code': driver['Abbreviation'],
                                        'position': int(driver['Position']) if pd.notna(driver['Position']) else None,
                                        'points': float(driver['Points']) if pd.notna(driver['Points']) else 0,
                                        'status': driver['Status']
                                    }
                                    team_results.append(result)
                            
                            # Calculate team points for this race
                            team_points = sum(result['points'] for result in team_results)
                            
                            # Compile race data
                            race_data = {
                                'gp_name': gp_name,
                                'round': race['round'],
                                'date': race['date'],
                                'country': race['country'],
                                'results': team_results,
                                'team_points': team_points
                            }
                            
                            season_data['races'].append(race_data)
                            logger.info(f"Added {year} {gp_name} data for {team_name}")
                            
                        except Exception as e:
                            logger.warning(f"Could not load data for {year} {gp_name}: {str(e)}")
                    
                    # Calculate season statistics
                    if season_data['races']:
                        total_points = sum(race['team_points'] for race in season_data['races'])
                        podiums = sum(1 for race in season_data['races'] 
                                      for result in race['results'] 
                                      if result['position'] and result['position'] <= 3)
                        wins = sum(1 for race in season_data['races'] 
                                   for result in race['results'] 
                                   if result['position'] == 1)
                        
                        season_data['statistics'] = {
                            'total_points': total_points,
                            'podiums': podiums,
                            'wins': wins,
                            'races_completed': len(season_data['races'])
                        }
                    
                    team_history['seasons'][year] = season_data
                    
                except Exception as e:
                    logger.error(f"Error processing {year} season for {team_name}: {str(e)}")
        
        print("\nData collection complete.")
        
        # Save to cache if we have data
        if team_history['seasons']:
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(team_history, f)
                logger.info(f"Saved performance history for {team_name} to cache")
            except Exception as e:
                logger.warning(f"Failed to save performance history to cache: {str(e)}")
        
        return team_history

    def compare_seasons(self, driver_code=None, team_name=None, years=None):
        """
        Compare performance across multiple seasons
        
        Args:
            driver_code (str, optional): Driver code to compare
            team_name (str, optional): Team name to compare
            years (list, optional): List of years to compare, defaults to all historical seasons
            
        Returns:
            dict: Comparative analysis across seasons
        """
        if not years:
            years = HISTORICAL_SEASONS
            
        logger.info(f"Comparing seasons {years} for {'driver ' + driver_code if driver_code else 'team ' + team_name if team_name else 'all'}")
        print("Comparing data across seasons...")
        
        if driver_code:
            # Get driver history
            driver_history = self.get_driver_performance_history(driver_code)
            
            # Extract data for comparison
            comparison = {
                'driver': driver_code,
                'years': years,
                'points_by_season': {},
                'wins_by_season': {},
                'podiums_by_season': {},
                'positions_by_race': {}
            }
            
            for year in years:
                if year in driver_history['seasons']:
                    season = driver_history['seasons'][year]
                    if 'statistics' in season:
                        comparison['points_by_season'][year] = season['statistics']['points']
                        comparison['wins_by_season'][year] = season['statistics']['wins']
                        comparison['podiums_by_season'][year] = season['statistics']['podiums']
                    
                    # Track positions by race
                    for race in season['races']:
                        gp_name = race['gp_name']
                        if gp_name not in comparison['positions_by_race']:
                            comparison['positions_by_race'][gp_name] = {}
                        
                        if race['result'] and race['result']['position']:
                            comparison['positions_by_race'][gp_name][year] = race['result']['position']
            
            return comparison
            
        elif team_name:
            # Get team history
            team_history = self.get_team_performance_history(team_name)
            
            # Extract data for comparison
            comparison = {
                'team': team_name,
                'years': years,
                'points_by_season': {},
                'wins_by_season': {},
                'podiums_by_season': {},
                'points_by_race': {}
            }
            
            for year in years:
                if year in team_history['seasons']:
                    season = team_history['seasons'][year]
                    if 'statistics' in season:
                        comparison['points_by_season'][year] = season['statistics']['total_points']
                        comparison['wins_by_season'][year] = season['statistics']['wins']
                        comparison['podiums_by_season'][year] = season['statistics']['podiums']
                    
                    # Track points by race
                    for race in season['races']:
                        gp_name = race['gp_name']
                        if gp_name not in comparison['points_by_race']:
                            comparison['points_by_race'][gp_name] = {}
                        
                        comparison['points_by_race'][gp_name][year] = race['team_points']
            
            return comparison
        
        else:
            # Compare overall championship standings
            comparison = {
                'years': years,
                'driver_champions': {},
                'team_champions': {}
            }
            
            print("Loading championship data...")
            
            for year in years:
                try:
                    # Use cached data where possible
                    cache_file = os.path.join(self.historical_cache_dir, f"champions_{year}.pkl")
                    if os.path.exists(cache_file):
                        try:
                            with open(cache_file, 'rb') as f:
                                year_data = pickle.load(f)
                                comparison['driver_champions'][year] = year_data['driver']
                                comparison['team_champions'][year] = year_data['team']
                                continue
                        except:
                            pass
                    
                    # Try to determine champions
                    champion_driver = None
                    champion_team = None
                    
                    # Get first race to load season
                    if year in self.calendars and self.calendars[year]:
                        last_race = self.calendars[year][-1]['gp_name']
                        
                        # Use last race of the season for final standings
                        session = fastf1.get_session(year, last_race, 'R')
                        session.load(laps=False, telemetry=False, weather=False)
                        
                        # Get driver standings
                        driver_standings = fastf1.api.driver_standings(year)
                        if driver_standings is not None and len(driver_standings) > 0:
                            champion = driver_standings.iloc[0]
                            champion_driver = {
                                'name': champion['FullName'],
                                'code': champion['Abbreviation'],
                                'points': champion['Points']
                            }
                        
                        # Get constructor standings
                        team_standings = fastf1.api.constructor_standings(year)
                        if team_standings is not None and len(team_standings) > 0:
                            champion_team_data = team_standings.iloc[0]
                            champion_team = {
                                'name': champion_team_data['Name'],
                                'points': champion_team_data['Points']
                            }
                        
                        # Save to cache
                        try:
                            with open(cache_file, 'wb') as f:
                                pickle.dump({'driver': champion_driver, 'team': champion_team}, f)
                        except:
                            pass
                    
                    comparison['driver_champions'][year] = champion_driver
                    comparison['team_champions'][year] = champion_team
                    
                except Exception as e:
                    logger.warning(f"Could not determine champions for {year}: {str(e)}")
            
            return comparison 