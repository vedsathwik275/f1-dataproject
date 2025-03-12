"""
OpenF1 Client Module

This module provides a client for interacting with the OpenF1 API
to retrieve Formula 1 session data, driver information, and more.
"""

import requests
import json
import pandas as pd
from datetime import datetime

class OpenF1Client:
    """Client for interacting with the OpenF1 API"""
    
    def __init__(self, base_url="https://api.openf1.org/v1"):
        """
        Initialize the OpenF1 client
        
        Args:
            base_url (str): Base URL for the OpenF1 API
        """
        self.base_url = base_url
    
    def _make_request(self, endpoint, params=None):
        """
        Make a request to the OpenF1 API
        
        Args:
            endpoint (str): API endpoint to request
            params (dict, optional): Query parameters to include in the request
            
        Returns:
            list: JSON response data as a list of dictionaries
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            print(f"[CHECKPOINT] Making request to OpenF1 API: {url}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            print(f"[SUCCESS] Received {len(data)} records from OpenF1 API")
            return data
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch data from OpenF1 API: {e}")
            return []
    
    def get_session_data(self, year, round_number, session_type=None):
        """
        Get session data from OpenF1 API
        
        Args:
            year (int): Year of the session
            round_number (int): Round number
            session_type (str, optional): Session type (e.g., 'Q', 'R')
            
        Returns:
            dict: Dictionary containing session data
        """
        params = {
            'year': year,
            'round': round_number
        }
        
        if session_type:
            if session_type == 'R':
                session_name = 'Race'
            elif session_type == 'Q':
                session_name = 'Qualifying'
            elif session_type == 'FP1':
                session_name = 'Practice 1'
            elif session_type == 'FP2':
                session_name = 'Practice 2'
            elif session_type == 'FP3':
                session_name = 'Practice 3'
            elif session_type == 'S':
                session_name = 'Sprint'
            else:
                session_name = session_type
                
            params['session_name'] = session_name
        
        print(f"[CHECKPOINT] Fetching session data for {year} Round {round_number} from OpenF1...")
        
        # Get session information
        sessions = self._make_request('sessions', params)
        
        if not sessions:
            print(f"[WARNING] No session data found for {year} Round {round_number}")
            return None
        
        # For each session, get additional data
        for session in sessions:
            session_meeting_key = session.get('meeting_key')
            session_key = session.get('session_key')
            
            if not session_meeting_key or not session_key:
                continue
            
            # Get weather data for the session
            weather_params = {
                'meeting_key': session_meeting_key,
                'session_key': session_key
            }
            weather_data = self._make_request('weather', weather_params)
            
            # Get session status information
            status_data = self._make_request('session_status', weather_params)
            
            # Add this data to the session
            session['weather'] = weather_data
            session['status'] = status_data
        
        # Return the enriched session data
        result = {
            'year': year,
            'round': round_number,
            'sessions': sessions
        }
        
        return result
    
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