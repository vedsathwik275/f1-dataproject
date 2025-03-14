"""
FastF1 Client Module

This module provides a client for interacting with the FastF1 API
to retrieve Formula 1 session data, telemetry, and more.
"""

import fastf1
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

class FastF1Client:
    """Client for interacting with the FastF1 API"""
    
    def __init__(self, cache_dir='cache'):
        """
        Initialize the FastF1 client
        
        Args:
            cache_dir (str): Directory to use for caching FastF1 data
        """
        # Enable FastF1 cache
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        fastf1.Cache.enable_cache(cache_dir)
        
        self.session_cache = {}  # Cache for loaded sessions
    
    def _get_session(self, year, gp_name, session_type='R'):
        """
        Get a FastF1 session object
        
        Args:
            year (int): Year of the session
            gp_name (str): Name of the Grand Prix
            session_type (str): Session type ('R' for race, 'Q' for qualifying, 'FP1', 'FP2', 'FP3', 'S' for sprint)
            
        Returns:
            fastf1.core.Session or None: The session object, or None if not found
        """
        # Check if session is already in cache
        cache_key = f"{year}_{gp_name}_{session_type}"
        if cache_key in self.session_cache:
            return self.session_cache[cache_key]
        
        try:
            print(f"[CHECKPOINT] Loading {year} {gp_name} {session_type} session from FastF1...")
            session = fastf1.get_session(year, gp_name, session_type)
            session.load()
            
            # Cache the session
            self.session_cache[cache_key] = session
            print(f"[SUCCESS] Session loaded successfully")
            return session
        except Exception as e:
            print(f"[ERROR] Failed to load session: {e}")
            return None
    
    def get_round_number(self, year, gp_name):
        """
        Get the round number for a Grand Prix
        
        Args:
            year (int): Year of the Grand Prix
            gp_name (str): Name of the Grand Prix
            
        Returns:
            int or None: Round number, or None if not found
        """
        try:
            schedule = fastf1.get_event_schedule(year)
            for idx, event in schedule.iterrows():
                if gp_name.lower() in event['EventName'].lower():
                    return event['RoundNumber']
            return None
        except Exception as e:
            print(f"Error getting round number: {e}")
            return None
    
    def get_race_calendar(self, year):
        """
        Get the race calendar for a specific year
        
        Args:
            year (int): Year to get calendar for
            
        Returns:
            list: List of races in the calendar with metadata
        """
        try:
            print(f"[CHECKPOINT] Fetching race calendar for {year}...")
            schedule = fastf1.get_event_schedule(year)
            
            if schedule.empty:
                print(f"[WARNING] No race calendar found for {year}")
                return []
            
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
            
            print(f"[SUCCESS] Found {len(calendar)} races in {year} calendar")
            return calendar
            
        except Exception as e:
            print(f"[ERROR] Failed to get race calendar: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_drivers(self, year):
        """
        Get all drivers for a specific year
        
        Args:
            year (int): The year to get drivers for
            
        Returns:
            list: List of driver information dictionaries
        """
        try:
            # Get the first race of the season to extract driver information
            calendar = self.get_race_calendar(year)
            if not calendar:
                return []
            
            first_race = calendar[0]['gp_name']
            session = self._get_session(year, first_race, 'R')
            
            if session is None:
                return []
            
            print(f"[CHECKPOINT] Extracting driver information for {year}...")
            
            drivers = []
            for driver_id, driver_info in session.get_driver_info().items():
                driver = {
                    'number': driver_info['DriverNumber'],
                    'code': driver_info['Abbreviation'],
                    'name': f"{driver_info['FirstName']} {driver_info['LastName']}",
                    'team': driver_info['TeamName']
                }
                drivers.append(driver)
            
            print(f"[SUCCESS] Found {len(drivers)} drivers for {year}")
            return drivers
        except Exception as e:
            print(f"[ERROR] Failed to fetch drivers: {e}")
            return []
    
    def get_driver_session_data(self, year, gp_name, driver_code, session_type='R'):
        """
        Get session data for a specific driver
        
        Args:
            year (int): Year of the session
            gp_name (str): Name of the Grand Prix
            driver_code (str): Driver code (e.g., 'VER', 'HAM')
            session_type (str): Session type ('R' for race, 'Q' for qualifying, etc.)
            
        Returns:
            dict: Dictionary containing driver session data
        """
        session = self._get_session(year, gp_name, session_type)
        if session is None:
            return None
        
        try:
            print(f"[CHECKPOINT] Extracting {driver_code}'s data from {year} {gp_name} {session_type}...")
            
            # Get driver laps
            driver_laps = session.laps.pick_driver(driver_code)
            
            if driver_laps.empty:
                print(f"[WARNING] No lap data found for {driver_code}")
                return None
            
            # Get fastest lap
            try:
                fastest_lap = driver_laps.pick_fastest()
                fastest_lap_time = fastest_lap['LapTime'].total_seconds()
                fastest_lap_number = fastest_lap['LapNumber']
            except:
                fastest_lap_time = None
                fastest_lap_number = None
            
            # Prepare lap data
            lap_data = []
            for _, lap in driver_laps.iterrows():
                if lap['LapTime'] is not pd.NaT:  # Skip laps with no time
                    lap_info = {
                        'lap_number': lap['LapNumber'],
                        'lap_time': lap['LapTime'].total_seconds(),
                        'sector_1': lap['Sector1Time'].total_seconds() if lap['Sector1Time'] is not pd.NaT else None,
                        'sector_2': lap['Sector2Time'].total_seconds() if lap['Sector2Time'] is not pd.NaT else None,
                        'sector_3': lap['Sector3Time'].total_seconds() if lap['Sector3Time'] is not pd.NaT else None,
                        'compound': lap['Compound'] if 'Compound' in lap else None,
                        'tyre_life': lap['TyreLife'] if 'TyreLife' in lap else None,
                        'fresh_tyre': lap['FreshTyre'] if 'FreshTyre' in lap else None
                    }
                    lap_data.append(lap_info)
            
            # Extract session result
            if session_type == 'R':
                try:
                    result = session.results.loc[session.results['Abbreviation'] == driver_code].iloc[0]
                    position = result['Position']
                    status = result['Status']
                except:
                    position = None
                    status = None
            else:
                position = None
                status = None
            
            # Get driver info
            driver_info = session.get_driver(driver_code)
            
            # Compile all data
            driver_data = {
                'driver': driver_code,
                'name': f"{driver_info['FirstName']} {driver_info['LastName']}",
                'team': driver_info['TeamName'],
                'year': year,
                'gp_name': gp_name,
                'session_type': session_type,
                'fastest_lap_time': fastest_lap_time,
                'fastest_lap_number': fastest_lap_number,
                'position': position,
                'status': status,
                'laps': lap_data
            }
            
            print(f"[SUCCESS] Extracted {len(lap_data)} laps of data for {driver_code}")
            return driver_data
        except Exception as e:
            print(f"[ERROR] Failed to extract driver data: {e}")
            return None
    
    def get_race_data(self, year, gp_name):
        """
        Get data for a specific race
        
        Args:
            year (int): Year of the race
            gp_name (str): Name of the Grand Prix
            
        Returns:
            dict: Dictionary containing race data
        """
        session = self._get_session(year, gp_name, 'R')
        if session is None:
            return None
        
        try:
            print(f"[CHECKPOINT] Extracting race data for {year} {gp_name}...")
            
            # Get race results
            results = session.results
            
            if results.empty:
                print(f"[WARNING] No results found for {year} {gp_name}")
                return None
            
            # Prepare driver results
            driver_results = []
            for _, result in results.iterrows():
                driver_result = {
                    'position': result['Position'],
                    'driver_number': result['DriverNumber'],
                    'driver_code': result['Abbreviation'],
                    'driver_name': f"{result['FirstName']} {result['LastName']}",
                    'team': result['TeamName'],
                    'grid': result['GridPosition'],
                    'status': result['Status'],
                    'points': result['Points']
                }
                driver_results.append(driver_result)
            
            # Safely extract race information
            event_info = session.event.to_dict() if hasattr(session, 'event') else {}
            
            # Check for different possible field names for circuit
            circuit_name = None
            if 'CircuitName' in event_info:
                circuit_name = event_info['CircuitName']
            elif 'OfficialName' in event_info:
                circuit_name = event_info['OfficialName']
            elif 'Location' in event_info:
                circuit_name = event_info['Location']
            else:
                circuit_name = gp_name + " Circuit"  # Fallback
                
            # Check for country
            country = event_info.get('Country', '')
            
            # Create race info dictionary
            race_info = {
                'year': year,
                'gp_name': gp_name,
                'date': session.date.strftime('%Y-%m-%d') if hasattr(session, 'date') else '',
                'circuit': circuit_name,
                'country': country,
                'results': driver_results
            }
            
            print(f"[SUCCESS] Extracted race data with {len(driver_results)} driver results")
            return race_info
        except Exception as e:
            print(f"[ERROR] Failed to extract race data: {e}")
            import traceback
            traceback.print_exc()  # Print the full traceback for debugging
            return None
    
    def get_qualifying_data(self, year, gp_name):
        """
        Get data for a qualifying session
        
        Args:
            year (int): Year of the qualifying session
            gp_name (str): Name of the Grand Prix
            
        Returns:
            dict: Dictionary containing qualifying data
        """
        session = self._get_session(year, gp_name, 'Q')
        if session is None:
            return None
        
        try:
            print(f"[CHECKPOINT] Extracting qualifying data for {year} {gp_name}...")
            
            # Get qualifying results
            results = session.results
            
            if results.empty:
                print(f"[WARNING] No qualifying results found for {year} {gp_name}")
                return None
            
            # Prepare driver results with qualifying times
            driver_results = []
            for _, result in results.iterrows():
                q1_time = result['Q1'] if result['Q1'] is not pd.NaT else None
                q2_time = result['Q2'] if result['Q2'] is not pd.NaT else None
                q3_time = result['Q3'] if result['Q3'] is not pd.NaT else None
                
                driver_result = {
                    'position': result['Position'],
                    'driver_number': result['DriverNumber'],
                    'driver_code': result['Abbreviation'],
                    'driver_name': f"{result['FirstName']} {result['LastName']}",
                    'team': result['TeamName'],
                    'q1_time': q1_time.total_seconds() if q1_time else None,
                    'q2_time': q2_time.total_seconds() if q2_time else None,
                    'q3_time': q3_time.total_seconds() if q3_time else None
                }
                driver_results.append(driver_result)
            
            # Get all laps by driver
            all_laps = session.laps
            
            # Organize laps by driver
            driver_laps = {}
            for driver in driver_results:
                driver_code = driver['driver_code']
                driver_lap_data = all_laps.pick_driver(driver_code)
                
                laps = []
                for _, lap in driver_lap_data.iterrows():
                    if lap['LapTime'] is not pd.NaT:  # Skip laps with no time
                        lap_info = {
                            'lap_number': lap['LapNumber'],
                            'lap_time': lap['LapTime'].total_seconds(),
                            'sector_1': lap['Sector1Time'].total_seconds() if lap['Sector1Time'] is not pd.NaT else None,
                            'sector_2': lap['Sector2Time'].total_seconds() if lap['Sector2Time'] is not pd.NaT else None,
                            'sector_3': lap['Sector3Time'].total_seconds() if lap['Sector3Time'] is not pd.NaT else None,
                            'compound': lap['Compound'] if 'Compound' in lap else None
                        }
                        laps.append(lap_info)
                
                driver_laps[driver_code] = laps
            
            # Extract qualifying information
            qualifying_info = {
                'year': year,
                'gp_name': gp_name,
                'date': session.date.strftime('%Y-%m-%d'),
                'circuit': session.event['CircuitName'],
                'country': session.event['Country'],
                'results': driver_results,
                'laps': driver_laps
            }
            
            print(f"[SUCCESS] Extracted qualifying data with {len(driver_results)} driver results")
            return qualifying_info
        except Exception as e:
            print(f"[ERROR] Failed to extract qualifying data: {e}")
            return None
    
    def get_telemetry_data(self, year, gp_name, driver_code, lap_number, session_type='R'):
        """
        Get telemetry data for a specific lap
        
        Args:
            year (int): Year of the session
            gp_name (str): Name of the Grand Prix
            driver_code (str): Driver code (e.g., 'VER', 'HAM')
            lap_number (int): Lap number to get telemetry for
            session_type (str): Session type ('R' for race, 'Q' for qualifying, etc.)
            
        Returns:
            dict: Dictionary containing telemetry data
        """
        session = self._get_session(year, gp_name, session_type)
        if session is None:
            return None
        
        try:
            print(f"[CHECKPOINT] Extracting telemetry data for {driver_code}'s lap {lap_number}...")
            
            # Get the specified lap
            lap = session.laps.pick_driver(driver_code).pick_lap(lap_number)
            
            if lap.empty:
                print(f"[WARNING] No data found for {driver_code}'s lap {lap_number}")
                return None
            
            # Get telemetry data
            telemetry = lap.get_telemetry()
            
            if telemetry.empty:
                print(f"[WARNING] No telemetry data available for {driver_code}'s lap {lap_number}")
                return None
            
            # Convert telemetry data to a list of dictionaries
            telemetry_data = []
            for _, data_point in telemetry.iterrows():
                point = {
                    'time': data_point['Time'].total_seconds(),
                    'speed': data_point['Speed'],
                    'rpm': data_point['RPM'] if 'RPM' in data_point else None,
                    'gear': data_point['nGear'] if 'nGear' in data_point else None,
                    'throttle': data_point['Throttle'] if 'Throttle' in data_point else None,
                    'brake': data_point['Brake'] if 'Brake' in data_point else None,
                    'drs': data_point['DRS'] if 'DRS' in data_point else None,
                    'distance': data_point['Distance'] if 'Distance' in data_point else None,
                    'x': data_point['X'] if 'X' in data_point else None,
                    'y': data_point['Y'] if 'Y' in data_point else None
                }
                telemetry_data.append(point)
            
            # Compile lap information with telemetry
            lap_info = {
                'driver': driver_code,
                'year': year,
                'gp_name': gp_name,
                'session_type': session_type,
                'lap_number': lap_number,
                'lap_time': lap['LapTime'].total_seconds() if lap['LapTime'] is not pd.NaT else None,
                'sector_1': lap['Sector1Time'].total_seconds() if lap['Sector1Time'] is not pd.NaT else None,
                'sector_2': lap['Sector2Time'].total_seconds() if lap['Sector2Time'] is not pd.NaT else None,
                'sector_3': lap['Sector3Time'].total_seconds() if lap['Sector3Time'] is not pd.NaT else None,
                'compound': lap['Compound'] if 'Compound' in lap else None,
                'tyre_life': lap['TyreLife'] if 'TyreLife' in lap else None,
                'telemetry': telemetry_data
            }
            
            print(f"[SUCCESS] Extracted telemetry data with {len(telemetry_data)} data points")
            return lap_info
        except Exception as e:
            print(f"[ERROR] Failed to extract telemetry data: {e}")
            return None
    
    def get_session_data(self, year, gp_name, session_type, driver_code):
        """
        Get session data for a specific driver
        
        Args:
            year (int): Year of the session
            gp_name (str): Grand Prix name
            session_type (str): Session type (e.g., 'R' for race, 'Q' for qualifying)
            driver_code (str): Driver code
            
        Returns:
            dict: Dictionary containing driver data for the session
        """
        try:
            # Create the session
            session = fastf1.get_session(year, gp_name, session_type)
            
            # Load the session data
            session.load()
            
            # Get the driver data
            driver_data = session.laps.pick_driver(driver_code)
            
            if driver_data.empty:
                print(f"[ERROR] No data found for driver {driver_code} in {year} {gp_name} {session_type}")
                return None
            
            # Get telemetry data if available
            telemetry = None
            try:
                fastest_lap = driver_data.pick_fastest()
                if not fastest_lap.empty:
                    telemetry = fastest_lap.get_telemetry()
            except Exception as e:
                print(f"[WARNING] Could not get telemetry data: {e}")
            
            # Create a dictionary with the data
            result = {
                'driver': driver_code,
                'name': session.get_driver(driver_code)['FullName'] if driver_code in session.drivers else 'Unknown',
                'team': session.get_driver(driver_code)['TeamName'] if driver_code in session.drivers else 'Unknown',
                'year': year,
                'gp_name': gp_name,
                'session_type': session_type,
                'fastest_lap_time': driver_data['LapTime'].min().total_seconds() if not driver_data['LapTime'].empty else None,
                'fastest_lap_number': driver_data.loc[driver_data['LapTime'].idxmin()]['LapNumber'] if not driver_data['LapTime'].empty else None,
                'position': session.results[session.results['Abbreviation'] == driver_code]['Position'].values[0] if not session.results.empty and driver_code in session.results['Abbreviation'].values else None,
                'status': session.results[session.results['Abbreviation'] == driver_code]['Status'].values[0] if not session.results.empty and driver_code in session.results['Abbreviation'].values else None,
                'laps': []
            }
            
            # Add lap data
            for _, lap in driver_data.iterrows():
                lap_data = {
                    'lap_number': lap['LapNumber'],
                    'lap_time': lap['LapTime'].total_seconds() if pd.notna(lap['LapTime']) else None,
                    'sector_1': lap['Sector1Time'].total_seconds() if pd.notna(lap['Sector1Time']) else None,
                    'sector_2': lap['Sector2Time'].total_seconds() if pd.notna(lap['Sector2Time']) else None,
                    'sector_3': lap['Sector3Time'].total_seconds() if pd.notna(lap['Sector3Time']) else None,
                    'compound': lap['Compound'],
                    'tyre_life': lap['TyreLife'],
                    'fresh_tyre': lap['FreshTyre'],
                    'time': lap['Time'].isoformat() if pd.notna(lap['Time']) else None,
                    'track_status': lap['TrackStatus']
                }
                result['laps'].append(lap_data)
            
            # Add telemetry data if available
            if telemetry is not None and not telemetry.empty:
                result['telemetry'] = {
                    'time': [t.total_seconds() for t in telemetry['Time']],
                    'speed': telemetry['Speed'].tolist(),
                    'throttle': telemetry['Throttle'].tolist(),
                    'brake': telemetry['Brake'].tolist(),
                    'gear': telemetry['nGear'].tolist(),
                    'rpm': telemetry['RPM'].tolist(),
                    'distance': telemetry['Distance'].tolist()
                }
            
            return result
            
        except Exception as e:
            print(f"[ERROR] Failed to get session data: {str(e)}")
            import traceback
            traceback.print_exc()
            return None 