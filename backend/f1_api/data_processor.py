"""
Data Processor Module

This module provides functions for processing and combining data from the FastF1 and OpenF1 APIs.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

def process_data(fastf1_data, openf1_data, analysis_type):
    """
    Process data from FastF1 and OpenF1 APIs
    
    Args:
        fastf1_data: Data from FastF1 API
        openf1_data: Data from OpenF1 API
        analysis_type (str): Type of analysis to perform
        
    Returns:
        dict: Processed data ready for visualization
    """
    if analysis_type == 'driver_performance':
        return process_driver_performance(fastf1_data, openf1_data)
    elif analysis_type == 'race_analysis':
        return process_race_analysis(fastf1_data, openf1_data)
    elif analysis_type == 'driver_comparison':
        return process_driver_comparison(fastf1_data, openf1_data)
    elif analysis_type == 'qualifying_analysis':
        return process_qualifying_analysis(fastf1_data, openf1_data)
    else:
        # Default processing
        return {
            'fastf1_data': fastf1_data,
            'openf1_data': openf1_data,
            'analysis_type': analysis_type
        }

def process_driver_performance(fastf1_data, openf1_data):
    """
    Process driver performance data
    
    Args:
        fastf1_data: Driver data from FastF1 API
        openf1_data: Driver data from OpenF1 API
        
    Returns:
        dict: Processed driver performance data
    """
    result = {
        'driver_info': {
            'code': fastf1_data.get('driver'),
            'name': fastf1_data.get('name'),
            'team': fastf1_data.get('team')
        },
        'session_info': {
            'year': fastf1_data.get('year'),
            'gp_name': fastf1_data.get('gp_name'),
            'session_type': fastf1_data.get('session_type')
        },
        'performance': {
            'fastest_lap_time': fastf1_data.get('fastest_lap_time'),
            'fastest_lap_number': fastf1_data.get('fastest_lap_number'),
            'position': fastf1_data.get('position'),
            'status': fastf1_data.get('status')
        },
        'lap_times': [],
        'sector_times': [],
        'tire_data': []
    }
    
    # Process lap times
    laps = fastf1_data.get('laps', [])
    
    # Calculate median lap time to help filter outliers (ignore zeros and nulls)
    valid_times = [lap.get('lap_time') for lap in laps if lap.get('lap_time') and lap.get('lap_time') > 0]
    if valid_times:
        median_lap_time = sorted(valid_times)[len(valid_times) // 2]
        # Set a reasonable threshold to filter out formation laps, in-lap, out-lap
        # Usually these can be several times longer than normal laps
        max_valid_time = median_lap_time * 1.5
    else:
        max_valid_time = float('inf')
    
    for lap in laps:
        lap_time = lap.get('lap_time')
        
        # Skip laps with no time or extremely long laps
        if not lap_time or lap_time <= 0 or lap_time > max_valid_time:
            continue
            
        # Add lap time data
        result['lap_times'].append({
            'lap_number': lap.get('lap_number'),
            'lap_time': lap_time
        })
        
        # Add sector time data if available and reasonable
        s1 = lap.get('sector_1')
        s2 = lap.get('sector_2')
        s3 = lap.get('sector_3')
        
        if (s1 is not None and s2 is not None and s3 is not None and
            s1 > 0 and s2 > 0 and s3 > 0 and
            s1 + s2 + s3 <= lap_time * 1.05):  # Allow for small rounding errors
            
            result['sector_times'].append({
                'lap_number': lap.get('lap_number'),
                'sector_1': s1,
                'sector_2': s2,
                'sector_3': s3
            })
    
    # Sort lap times and sector times by lap number
    result['lap_times'].sort(key=lambda x: x['lap_number'])
    result['sector_times'].sort(key=lambda x: x['lap_number'])
    
    # Process tire data
    tire_stints = {}
    for lap in laps:
        compound = lap.get('compound')
        lap_number = lap.get('lap_number')
        
        if not compound or not lap_number:
            continue
            
        # Group by compound
        if compound not in tire_stints:
            tire_stints[compound] = []
            
        # Add lap to the compound's list
        tire_stints[compound].append(lap_number)
    
    # Convert to stints (continuous lap ranges)
    for compound, lap_numbers in tire_stints.items():
        # Sort laps
        lap_numbers.sort()
        
        # Find continuous ranges
        stints = []
        current_stint = []
        
        for lap in lap_numbers:
            if not current_stint or lap == current_stint[-1] + 1:
                current_stint.append(lap)
            else:
                if current_stint:
                    stints.append(current_stint)
                current_stint = [lap]
        
        # Add the last stint
        if current_stint:
            stints.append(current_stint)
        
        # Add to result
        for stint in stints:
            result['tire_data'].append({
                'compound': compound,
                'tyre_life': len(stint),  # Approximation of tire life
                'fresh_tyre': True,  # Assuming first stint starts with fresh tires
                'laps': stint
            })
    
    # Add OpenF1 data if available
    if openf1_data:
        session_data = []
        
        # Match session type to OpenF1 session name
        session_type_map = {
            'R': 'Race',
            'Q': 'Qualifying',
            'FP1': 'Practice 1',
            'FP2': 'Practice 2',
            'FP3': 'Practice 3',
            'S': 'Sprint'
        }
        
        target_session_name = session_type_map.get(fastf1_data.get('session_type'))
        
        # Find matching session in OpenF1 data
        if target_session_name and openf1_data.get('sessions'):
            for session in openf1_data['sessions']:
                if session.get('session_name') == target_session_name:
                    session_data.append(session)
        
        # Process lap data from OpenF1
        if session_data:
            openf1_lap_times = []
            for session in session_data:
                for lap in session.get('laps', []):
                    lap_time = lap.get('lap_time')
                    if lap_time:
                        openf1_lap_times.append({
                            'lap_number': lap.get('lap_number'),
                            'lap_time': lap_time,
                            'sector_1': lap.get('sector1_time'),
                            'sector_2': lap.get('sector2_time'),
                            'sector_3': lap.get('sector3_time')
                        })
            
            result['openf1_lap_times'] = openf1_lap_times
            
            # Process stint data from OpenF1
            openf1_stints = []
            for session in session_data:
                for stint in session.get('stints', []):
                    compound = stint.get('compound')
                    if compound:
                        openf1_stints.append({
                            'compound': compound,
                            'lap_start': stint.get('lap_from'),
                            'lap_end': stint.get('lap_to')
                        })
            
            result['openf1_stints'] = openf1_stints
    
    return result

def process_race_analysis(fastf1_data, openf1_data):
    """
    Process race data for analysis
    
    Args:
        fastf1_data: Race data from FastF1 API
        openf1_data: Race data from OpenF1 API
        
    Returns:
        dict: Processed race analysis data
    """
    result = {
        'race_info': {
            'year': fastf1_data.get('year'),
            'gp_name': fastf1_data.get('gp_name'),
            'date': fastf1_data.get('date'),
            'circuit': fastf1_data.get('circuit'),
            'country': fastf1_data.get('country')
        },
        'results': fastf1_data.get('results', []),
        'positions': [],
        'lap_times': [],
        'pit_stops': []
    }
    
    # Add OpenF1 data if available
    if openf1_data and openf1_data.get('sessions'):
        race_session = None
        
        # Find the race session
        for session in openf1_data['sessions']:
            if session.get('session_name') == 'Race':
                race_session = session
                break
        
        if race_session:
            # Add weather data
            result['weather'] = race_session.get('weather', [])
            
            # Add session status data
            result['session_status'] = race_session.get('status', [])
    
    return result

def process_driver_comparison(drivers_data, openf1_data=None):
    """
    Process data for driver comparison
    
    Args:
        drivers_data: List of driver data from FastF1 API
        openf1_data: Data from OpenF1 API (not used in this function)
        
    Returns:
        dict: Processed driver comparison data
    """
    if not isinstance(drivers_data, list) or len(drivers_data) < 2:
        return {'error': 'Need at least two drivers for comparison'}
    
    driver1_data = drivers_data[0]
    driver2_data = drivers_data[1]
    
    # Extract basic information
    result = {
        'session_info': {
            'year': driver1_data.get('year'),
            'gp_name': driver1_data.get('gp_name'),
            'session_type': driver1_data.get('session_type')
        },
        'drivers': [
            {
                'code': driver1_data.get('driver'),
                'name': driver1_data.get('name'),
                'team': driver1_data.get('team'),
                'fastest_lap_time': driver1_data.get('fastest_lap_time'),
                'fastest_lap_number': driver1_data.get('fastest_lap_number'),
                'position': driver1_data.get('position'),
                'status': driver1_data.get('status'),
                'lap_times': [],
                'sector_times': []
            },
            {
                'code': driver2_data.get('driver'),
                'name': driver2_data.get('name'),
                'team': driver2_data.get('team'),
                'fastest_lap_time': driver2_data.get('fastest_lap_time'),
                'fastest_lap_number': driver2_data.get('fastest_lap_number'),
                'position': driver2_data.get('position'),
                'status': driver2_data.get('status'),
                'lap_times': [],
                'sector_times': []
            }
        ],
        'lap_time_diff': [],  # Lap time differences
        'sector_time_diff': []  # Sector time differences
    }
    
    # Process lap times and sector times for both drivers
    for idx, driver_data in enumerate([driver1_data, driver2_data]):
        laps = driver_data.get('laps', [])
        for lap in laps:
            # Add lap time data
            result['drivers'][idx]['lap_times'].append({
                'lap_number': lap.get('lap_number'),
                'lap_time': lap.get('lap_time')
            })
            
            # Add sector time data if available
            if lap.get('sector_1') is not None and lap.get('sector_2') is not None and lap.get('sector_3') is not None:
                result['drivers'][idx]['sector_times'].append({
                    'lap_number': lap.get('lap_number'),
                    'sector_1': lap.get('sector_1'),
                    'sector_2': lap.get('sector_2'),
                    'sector_3': lap.get('sector_3')
                })
    
    # Calculate lap time differences where both drivers have completed the same lap
    driver1_lap_times = {lap['lap_number']: lap['lap_time'] for lap in result['drivers'][0]['lap_times']}
    driver2_lap_times = {lap['lap_number']: lap['lap_time'] for lap in result['drivers'][1]['lap_times']}
    
    common_laps = set(driver1_lap_times.keys()).intersection(set(driver2_lap_times.keys()))
    
    for lap_number in sorted(common_laps):
        time_diff = driver1_lap_times[lap_number] - driver2_lap_times[lap_number]
        result['lap_time_diff'].append({
            'lap_number': lap_number,
            'time_diff': time_diff  # Positive means driver1 is slower
        })
    
    # Calculate sector time differences similarly
    driver1_sectors = {}
    for sector_data in result['drivers'][0]['sector_times']:
        lap_num = sector_data['lap_number']
        driver1_sectors[lap_num] = {
            'sector_1': sector_data['sector_1'],
            'sector_2': sector_data['sector_2'],
            'sector_3': sector_data['sector_3']
        }
    
    driver2_sectors = {}
    for sector_data in result['drivers'][1]['sector_times']:
        lap_num = sector_data['lap_number']
        driver2_sectors[lap_num] = {
            'sector_1': sector_data['sector_1'],
            'sector_2': sector_data['sector_2'],
            'sector_3': sector_data['sector_3']
        }
    
    common_sector_laps = set(driver1_sectors.keys()).intersection(set(driver2_sectors.keys()))
    
    for lap_number in sorted(common_sector_laps):
        sector1_diff = driver1_sectors[lap_number]['sector_1'] - driver2_sectors[lap_number]['sector_1']
        sector2_diff = driver1_sectors[lap_number]['sector_2'] - driver2_sectors[lap_number]['sector_2']
        sector3_diff = driver1_sectors[lap_number]['sector_3'] - driver2_sectors[lap_number]['sector_3']
        
        result['sector_time_diff'].append({
            'lap_number': lap_number,
            'sector_1_diff': sector1_diff,
            'sector_2_diff': sector2_diff,
            'sector_3_diff': sector3_diff
        })
    
    return result

def process_qualifying_analysis(fastf1_data, openf1_data):
    """
    Process qualifying data for analysis
    
    Args:
        fastf1_data: Qualifying data from FastF1 API
        openf1_data: Qualifying data from OpenF1 API
        
    Returns:
        dict: Processed qualifying analysis data
    """
    result = {
        'qualifying_info': {
            'year': fastf1_data.get('year'),
            'gp_name': fastf1_data.get('gp_name'),
            'date': fastf1_data.get('date'),
            'circuit': fastf1_data.get('circuit'),
            'country': fastf1_data.get('country')
        },
        'results': fastf1_data.get('results', []),
        'laps_by_driver': fastf1_data.get('laps', {}),
        'q1_times': [],
        'q2_times': [],
        'q3_times': [],
        'lap_time_improvements': []
    }
    
    # Extract Q1, Q2, Q3 times
    for driver_result in result['results']:
        # Q1 times
        if driver_result.get('q1_time'):
            result['q1_times'].append({
                'driver_code': driver_result.get('driver_code'),
                'time': driver_result.get('q1_time')
            })
        
        # Q2 times
        if driver_result.get('q2_time'):
            result['q2_times'].append({
                'driver_code': driver_result.get('driver_code'),
                'time': driver_result.get('q2_time')
            })
        
        # Q3 times
        if driver_result.get('q3_time'):
            result['q3_times'].append({
                'driver_code': driver_result.get('driver_code'),
                'time': driver_result.get('q3_time')
            })
    
    # Calculate improvements from Q1->Q2 and Q2->Q3
    q1_times_by_driver = {item['driver_code']: item['time'] for item in result['q1_times']}
    q2_times_by_driver = {item['driver_code']: item['time'] for item in result['q2_times']}
    q3_times_by_driver = {item['driver_code']: item['time'] for item in result['q3_times']}
    
    # Q1 to Q2 improvements
    for driver_code in set(q1_times_by_driver.keys()).intersection(set(q2_times_by_driver.keys())):
        improvement = q1_times_by_driver[driver_code] - q2_times_by_driver[driver_code]
        if improvement > 0:  # Only count positive improvements
            result['lap_time_improvements'].append({
                'driver_code': driver_code,
                'from_session': 'Q1',
                'to_session': 'Q2',
                'improvement': improvement
            })
    
    # Q2 to Q3 improvements
    for driver_code in set(q2_times_by_driver.keys()).intersection(set(q3_times_by_driver.keys())):
        improvement = q2_times_by_driver[driver_code] - q3_times_by_driver[driver_code]
        if improvement > 0:  # Only count positive improvements
            result['lap_time_improvements'].append({
                'driver_code': driver_code,
                'from_session': 'Q2',
                'to_session': 'Q3',
                'improvement': improvement
            })
    
    # Add OpenF1 data if available
    if openf1_data and openf1_data.get('sessions'):
        quali_session = None
        
        # Find the qualifying session
        for session in openf1_data['sessions']:
            if session.get('session_name') == 'Qualifying':
                quali_session = session
                break
        
        if quali_session:
            # Add weather data
            result['weather'] = quali_session.get('weather', [])
            
            # Add session status data
            result['session_status'] = quali_session.get('status', [])
    
    return result 