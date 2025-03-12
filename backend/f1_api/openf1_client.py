"""
OpenF1 Client Module

This module provides a client for interacting with the OpenF1 API
to retrieve Formula 1 session data, driver information, and more.
"""

import requests
import json
import pandas as pd
from datetime import datetime
import os
import time

class OpenF1Client:
    """Client for interacting with the OpenF1 API"""
    
    BASE_URL = "https://api.openf1.org/v1"
    
    def __init__(self, cache_dir=None):
        """
        Initialize OpenF1 client
        
        Args:
            cache_dir (str, optional): Directory to cache API responses
        """
        self.cache_dir = cache_dir
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def get_session_data(self, year, round_number=None, gp_name=None):
        """
        Get session data for a specific event
        
        Args:
            year (int): Year of the session
            round_number (int, optional): Round number
            gp_name (str, optional): Grand Prix name
            
        Returns:
            dict: Session data
        """
        print(f"[CHECKPOINT] Fetching session data for {year} {'' if round_number is None else f'Round {round_number}'} from OpenF1...")
        
        # Check if we're requesting 2024 data which might not be fully available yet
        current_year = datetime.now().year
        if year == current_year:
            print(f"[INFO] Requesting current season ({year}) data from OpenF1. Some data may be limited or unavailable.")
        elif year > current_year:
            print(f"[WARNING] Requesting future season ({year}) data from OpenF1. This data is unlikely to be available.")
        
        # Try to get data from sessions endpoint
        sessions_data = self._fetch_sessions(year, round_number, gp_name)
        
        # If no session data found but we have a gp_name, try to convert it to a round number
        if not sessions_data.get('sessions') and gp_name:
            mapped_round = self._map_gp_name_to_round(year, gp_name)
            if mapped_round and mapped_round != round_number:
                print(f"[INFO] Trying alternative round number ({mapped_round}) for {gp_name}...")
                sessions_data = self._fetch_sessions(year, mapped_round, None)
        
        # If still no data, try an alternative approach for newer seasons
        if not sessions_data.get('sessions') and year >= 2023:
            print(f"[INFO] Trying alternative approach for {year} season data...")
            # Try to get data directly using event name
            if gp_name:
                formatted_gp = gp_name.lower().replace(' ', '_')
                sessions_data = self._fetch_by_event_name(year, formatted_gp)
        
        return sessions_data
    
    def _fetch_sessions(self, year, round_number=None, gp_name=None):
        """Fetch sessions data from OpenF1 API"""
        # Construct query parameters
        params = {}
        if year:
            params['year'] = year
        if round_number:
            params['round_number'] = round_number
        elif gp_name:
            # Try to find matching circuit/event
            params['circuit_key'] = gp_name.lower().replace(' ', '_')
        
        # Make API request
        sessions_url = f"{self.BASE_URL}/sessions"
        print(f"[CHECKPOINT] Making request to OpenF1 API: {sessions_url}")
        
        try:
            response = requests.get(sessions_url, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            sessions_data = response.json()
            print(f"[SUCCESS] Received {len(sessions_data)} records from OpenF1 API")
            
            # Process the sessions data
            result = {
                'sessions': []
            }
            
            if sessions_data:
                # Group sessions by meeting_key
                meetings = {}
                for session in sessions_data:
                    meeting_key = session.get('meeting_key')
                    if meeting_key:
                        if meeting_key not in meetings:
                            meetings[meeting_key] = []
                        meetings[meeting_key].append(session)
                
                # Process each meeting
                for meeting_key, meeting_sessions in meetings.items():
                    # Fetch additional data for each session
                    for session in meeting_sessions:
                        session_data = self._fetch_session_details(session)
                        result['sessions'].append(session_data)
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch sessions from OpenF1 API: {str(e)}")
            return {'sessions': [], 'error': str(e)}
    
    def _fetch_by_event_name(self, year, event_name):
        """
        Fetch data using direct event name approach
        
        This is a fallback method for newer seasons
        """
        # Try a more direct approach - some combination of these parameters might work
        params = {
            'year': year,
            'meeting_name': event_name,
            'meeting_key': f"{year}_{event_name}"
        }
        
        try:
            # Try with meeting_key approach first
            sessions_url = f"{self.BASE_URL}/sessions"
            response = requests.get(sessions_url, params={'meeting_key': params['meeting_key']})
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    print(f"[SUCCESS] Found data using meeting_key: {params['meeting_key']}")
                    return self._process_raw_sessions(data)
            
            # Try with year and circuit/meeting name combination
            for key in ['meeting_name', 'circuit_key', 'circuit_short_name']:
                response = requests.get(sessions_url, params={'year': year, key: event_name})
                if response.status_code == 200:
                    data = response.json()
                    if data and len(data) > 0:
                        print(f"[SUCCESS] Found data using {key}: {event_name}")
                        return self._process_raw_sessions(data)
            
            print(f"[WARNING] Could not find data for {year} {event_name} using alternative approaches")
            return {'sessions': []}
            
        except Exception as e:
            print(f"[ERROR] Error in fallback method: {str(e)}")
            return {'sessions': [], 'error': str(e)}
    
    def _process_raw_sessions(self, sessions_data):
        """Process raw sessions data into the expected format"""
        result = {'sessions': []}
        
        for session in sessions_data:
            session_data = self._fetch_session_details(session)
            result['sessions'].append(session_data)
        
        return result
    
    def _map_gp_name_to_round(self, year, gp_name):
        """Map Grand Prix name to round number using a lookup table"""
        # This is a simple mapping for common races
        # Could be expanded or made dynamic in the future
        gp_name_lower = gp_name.lower()
        
        # Basic mapping table - this could be expanded or loaded from a file
        mappings = {
            'bahrain': 1,
            'saudi': 2, 'saudi arabia': 2, 'saudi arabian': 2,
            'australia': 3, 'australian': 3,
            'japan': 4, 'japanese': 4,
            'china': 5, 'chinese': 5,
            'miami': 6,
            'emilia': 7, 'emilia romagna': 7, 'imola': 7,
            'monaco': 8,
            'canada': 9, 'canadian': 9,
            'spain': 10, 'spanish': 10,
            'austria': 11, 'austrian': 11,
            'great britain': 12, 'british': 12, 'silverstone': 12,
            'hungary': 13, 'hungarian': 13,
            'belgium': 14, 'belgian': 14, 'spa': 14,
            'netherlands': 15, 'dutch': 15, 'zandvoort': 15,
            'monza': 16, 'italian': 16, 'italy': 16,
            'azerbaijan': 17, 'baku': 17,
            'singapore': 18,
            'united states': 19, 'us': 19, 'usa': 19, 'austin': 19,
            'mexico': 20, 'mexican': 20,
            'brazil': 21, 'brazilian': 21, 'sao paulo': 21,
            'las vegas': 22,
            'qatar': 23,
            'abu dhabi': 24
        }
        
        # Check for matches
        for key, value in mappings.items():
            if key in gp_name_lower:
                return value
        
        return None
    
    def _fetch_session_details(self, session):
        """
        Fetch additional details for a specific session
        
        Args:
            session (dict): Basic session information
            
        Returns:
            dict: Enhanced session data with additional details
        """
        session_data = {
            'meeting_name': session.get('meeting_name', ''),
            'meeting_official_name': session.get('meeting_official_name', ''),
            'circuit_key': session.get('circuit_key', ''),
            'circuit_short_name': session.get('circuit_short_name', ''),
            'country_name': session.get('country_name', ''),
            'country_code': session.get('country_code', ''),
            'session_key': session.get('session_key', ''),
            'session_name': session.get('session_name', ''),
            'session_type': session.get('session_type', ''),
            'date_start': session.get('date_start', ''),
            'year': session.get('year'),
            'laps': [],
            'drivers': [],
            'stints': [],
            'weather': [],
            'status': []
        }
        
        # Fetch lap data
        session_key = session.get('session_key')
        if session_key:
            # Add rate limiting to avoid overwhelming the API
            time.sleep(0.5)
            
            laps = self._fetch_laps(session_key)
            if laps:
                session_data['laps'] = laps
            
            # Add rate limiting between requests
            time.sleep(0.5)
            
            # Fetch stint data
            stints = self._fetch_stints(session_key)
            if stints:
                session_data['stints'] = stints
            
            # Add rate limiting between requests
            time.sleep(0.5)
            
            # Fetch driver data
            drivers = self._fetch_drivers(session_key)
            if drivers:
                session_data['drivers'] = drivers
            
            # Add rate limiting between requests
            time.sleep(0.5)
            
            # Fetch weather data
            weather = self._fetch_weather(session_key)
            if weather:
                session_data['weather'] = weather
            
            # Add rate limiting between requests
            time.sleep(0.5)
            
            # Fetch session status data
            status = self._fetch_session_status(session_key)
            if status:
                session_data['status'] = status
        
        return session_data
    
    def _fetch_laps(self, session_key):
        """
        Fetch lap data for a specific session
        
        Args:
            session_key (str): Session key
            
        Returns:
            list: Lap data
        """
        try:
            url = f"{self.BASE_URL}/laps"
            response = requests.get(url, params={'session_key': session_key})
            
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] Fetched {len(data)} laps from OpenF1 API")
                return data
            else:
                print(f"[WARNING] Failed to fetch lap data: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] Error fetching lap data: {str(e)}")
            return []
    
    def _fetch_stints(self, session_key):
        """
        Fetch stint data for a specific session
        
        Args:
            session_key (str): Session key
            
        Returns:
            list: Stint data
        """
        try:
            url = f"{self.BASE_URL}/stints"
            response = requests.get(url, params={'session_key': session_key})
            
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] Fetched {len(data)} stints from OpenF1 API")
                return data
            else:
                print(f"[WARNING] Failed to fetch stint data: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] Error fetching stint data: {str(e)}")
            return []
    
    def _fetch_drivers(self, session_key):
        """
        Fetch driver data for a specific session
        
        Args:
            session_key (str): Session key
            
        Returns:
            list: Driver data
        """
        try:
            url = f"{self.BASE_URL}/drivers"
            response = requests.get(url, params={'session_key': session_key})
            
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] Fetched {len(data)} drivers from OpenF1 API")
                return data
            else:
                print(f"[WARNING] Failed to fetch driver data: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] Error fetching driver data: {str(e)}")
            return []
    
    def _fetch_weather(self, session_key):
        """
        Fetch weather data for a specific session
        
        Args:
            session_key (str): Session key
            
        Returns:
            list: Weather data
        """
        try:
            url = f"{self.BASE_URL}/weather"
            response = requests.get(url, params={'session_key': session_key})
            
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] Fetched {len(data)} weather records from OpenF1 API")
                return data
            else:
                print(f"[WARNING] Failed to fetch weather data: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] Error fetching weather data: {str(e)}")
            return []
    
    def _fetch_session_status(self, session_key):
        """
        Fetch session status data for a specific session
        
        Args:
            session_key (str): Session key
            
        Returns:
            list: Session status data
        """
        try:
            url = f"{self.BASE_URL}/session_status"
            response = requests.get(url, params={'session_key': session_key})
            
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] Fetched {len(data)} status records from OpenF1 API")
                return data
            else:
                print(f"[WARNING] Failed to fetch session status data: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] Error fetching session status data: {str(e)}")
            return []
    
    def get_driver_data(self, year, round_number, driver_code):
        """
        Get driver data from OpenF1 API
        
        Args:
            year (int): Year of the session
            round_number (int): Round number
            driver_code (str): Driver code (e.g., 'VER', 'HAM')
            
        Returns:
            dict: Dictionary containing driver data
        """
        # First get session information to get session keys
        session_data = self.get_session_data(year, round_number)
        
        if not session_data or not session_data.get('sessions'):
            return None
        
        print(f"[CHECKPOINT] Fetching data for driver {driver_code} in {year} Round {round_number}...")
        
        all_driver_data = {
            'driver_code': driver_code,
            'year': year,
            'round': round_number,
            'sessions': []
        }
        
        # For each session, get driver data
        for session in session_data['sessions']:
            session_meeting_key = session.get('meeting_key')
            session_key = session.get('session_key')
            session_name = session.get('session_name')
            
            if not session_meeting_key or not session_key:
                continue
            
            # Get driver information
            driver_params = {
                'meeting_key': session_meeting_key,
                'session_key': session_key,
                'driver_number': self._get_driver_number(driver_code, year, round_number)
            }
            
            # Get driver times
            lap_data = self._make_request('laps', driver_params)
            
            # Get driver stints
            stint_data = self._make_request('stints', driver_params)
            
            # Get driver position data (telemetry)
            position_data = self._make_request('position', driver_params)
            
            # Get tire information
            stint_data = self._make_request('stints', driver_params)
            
            # Add session data to result
            session_driver_data = {
                'session_name': session_name,
                'meeting_key': session_meeting_key,
                'session_key': session_key,
                'laps': lap_data,
                'stints': stint_data,
                'positions': position_data
            }
            
            all_driver_data['sessions'].append(session_driver_data)
        
        return all_driver_data
    
    def get_lap_data(self, year, round_number, session_type=None):
        """
        Get lap data from OpenF1 API
        
        Args:
            year (int): Year of the session
            round_number (int): Round number
            session_type (str, optional): Session type (e.g., 'Q', 'R')
            
        Returns:
            dict: Dictionary containing lap data for all drivers
        """
        # First get session information to get session keys
        session_data = self.get_session_data(year, round_number, session_type)
        
        if not session_data or not session_data.get('sessions'):
            return None
        
        target_session = None
        if session_type and session_data['sessions']:
            # Find the specific session
            for session in session_data['sessions']:
                if session_type == 'R' and session.get('session_name') == 'Race':
                    target_session = session
                    break
                elif session_type == 'Q' and session.get('session_name') == 'Qualifying':
                    target_session = session
                    break
                elif session_type == session.get('session_name'):
                    target_session = session
                    break
        
        if not target_session and session_data['sessions']:
            # Just use the first session if no specific one was found
            target_session = session_data['sessions'][0]
        
        if not target_session:
            return None
        
        session_meeting_key = target_session.get('meeting_key')
        session_key = target_session.get('session_key')
        session_name = target_session.get('session_name')
        
        if not session_meeting_key or not session_key:
            return None
        
        print(f"[CHECKPOINT] Fetching lap data for {year} Round {round_number} {session_name}...")
        
        # Get lap information for all drivers
        lap_params = {
            'meeting_key': session_meeting_key,
            'session_key': session_key
        }
        
        lap_data = self._make_request('laps', lap_params)
        
        # Get driver information to map driver numbers to names/codes
        driver_data = self._make_request('drivers', {'year': year})
        
        # Create a map of driver numbers to driver info
        driver_map = {}
        for driver in driver_data:
            driver_number = driver.get('driver_number')
            if driver_number:
                driver_map[driver_number] = driver
        
        # Add driver information to each lap
        for lap in lap_data:
            driver_number = lap.get('driver_number')
            if driver_number and driver_number in driver_map:
                lap['driver_code'] = driver_map[driver_number].get('driver_code')
                lap['driver_name'] = driver_map[driver_number].get('full_name')
                lap['team_name'] = driver_map[driver_number].get('team_name')
        
        # Organize data by driver
        drivers_lap_data = {}
        for lap in lap_data:
            driver_code = lap.get('driver_code')
            if not driver_code:
                continue
                
            if driver_code not in drivers_lap_data:
                drivers_lap_data[driver_code] = []
            
            drivers_lap_data[driver_code].append(lap)
        
        # Create the result
        result = {
            'year': year,
            'round': round_number,
            'session_name': session_name,
            'meeting_key': session_meeting_key,
            'session_key': session_key,
            'all_laps': lap_data,
            'driver_laps': drivers_lap_data
        }
        
        return result
    
    def get_tire_data(self, year, round_number, session_type=None):
        """
        Get tire usage data from OpenF1 API
        
        Args:
            year (int): Year of the session
            round_number (int): Round number
            session_type (str, optional): Session type (e.g., 'Q', 'R')
            
        Returns:
            dict: Dictionary containing tire data for all drivers
        """
        # First get session information to get session keys
        session_data = self.get_session_data(year, round_number, session_type)
        
        if not session_data or not session_data.get('sessions'):
            return None
        
        target_session = None
        if session_type and session_data['sessions']:
            # Find the specific session
            for session in session_data['sessions']:
                if session_type == 'R' and session.get('session_name') == 'Race':
                    target_session = session
                    break
                elif session_type == 'Q' and session.get('session_name') == 'Qualifying':
                    target_session = session
                    break
                elif session_type == session.get('session_name'):
                    target_session = session
                    break
        
        if not target_session and session_data['sessions']:
            # Just use the first session if no specific one was found
            target_session = session_data['sessions'][0]
        
        if not target_session:
            return None
        
        session_meeting_key = target_session.get('meeting_key')
        session_key = target_session.get('session_key')
        session_name = target_session.get('session_name')
        
        if not session_meeting_key or not session_key:
            return None
        
        print(f"[CHECKPOINT] Fetching tire data for {year} Round {round_number} {session_name}...")
        
        # Get tire information for all drivers
        stint_params = {
            'meeting_key': session_meeting_key,
            'session_key': session_key
        }
        
        stint_data = self._make_request('stints', stint_params)
        
        # Get driver information to map driver numbers to names/codes
        driver_data = self._make_request('drivers', {'year': year})
        
        # Create a map of driver numbers to driver info
        driver_map = {}
        for driver in driver_data:
            driver_number = driver.get('driver_number')
            if driver_number:
                driver_map[driver_number] = driver
        
        # Add driver information to each stint
        for stint in stint_data:
            driver_number = stint.get('driver_number')
            if driver_number and driver_number in driver_map:
                stint['driver_code'] = driver_map[driver_number].get('driver_code')
                stint['driver_name'] = driver_map[driver_number].get('full_name')
                stint['team_name'] = driver_map[driver_number].get('team_name')
        
        # Organize data by driver
        drivers_stint_data = {}
        for stint in stint_data:
            driver_code = stint.get('driver_code')
            if not driver_code:
                continue
                
            if driver_code not in drivers_stint_data:
                drivers_stint_data[driver_code] = []
            
            drivers_stint_data[driver_code].append(stint)
        
        # Create the result
        result = {
            'year': year,
            'round': round_number,
            'session_name': session_name,
            'meeting_key': session_meeting_key,
            'session_key': session_key,
            'all_stints': stint_data,
            'driver_stints': drivers_stint_data
        }
        
        return result
    
    def _get_driver_number(self, driver_code, year, round_number=1):
        """
        Get a driver's number from their code
        
        Args:
            driver_code (str): Driver code (e.g., 'VER', 'HAM')
            year (int): Year to look up driver information
            round_number (int, optional): Round number to use for the lookup
            
        Returns:
            int or None: Driver number, or None if not found
        """
        # Get driver information
        params = {
            'year': year,
            'round': round_number
        }
        
        drivers = self._make_request('drivers', params)
        
        # Find the driver with the matching code
        for driver in drivers:
            if driver.get('driver_code') == driver_code:
                return driver.get('driver_number')
        
        return None
    
    def get_driver_list(self, year):
        """
        Get a list of all drivers for a specific year
        
        Args:
            year (int): Year to get drivers for
            
        Returns:
            list: List of driver dictionaries
        """
        print(f"[CHECKPOINT] Fetching driver list for {year} from OpenF1...")
        
        params = {'year': year}
        drivers = self._make_request('drivers', params)
        
        return drivers 