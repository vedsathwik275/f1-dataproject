#!/usr/bin/env python3
"""
F1 Calendar Fetcher

A standalone script to fetch and display the Formula 1 race calendar for 2025.
"""

import os
import sys
import fastf1
import pandas as pd
from datetime import datetime

def setup_cache():
    """Set up cache directory for FastF1"""
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)
    return cache_dir

def get_race_calendar(year=2025):
    """
    Get the F1 race calendar for the specified year
    
    Args:
        year (int): Year to get calendar for
    
    Returns:
        list: List of races in the calendar with metadata
    """
    try:
        print(f"Fetching race calendar for {year}...")
        schedule = fastf1.get_event_schedule(year)
        
        if schedule.empty:
            print(f"No race calendar found for {year}")
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
        
        print(f"Found {len(calendar)} races in {year} calendar")
        return calendar
        
    except Exception as e:
        print(f"Error fetching race calendar: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def print_calendar(calendar):
    """Print the race calendar in a formatted way"""
    if not calendar:
        print("No calendar data available")
        return
    
    print("\n===== 2025 FORMULA 1 RACE CALENDAR =====\n")
    print(f"{'ROUND':<6} {'DATE':<12} {'GRAND PRIX':<30} {'COUNTRY':<15}\n")
    
    for race in calendar:
        round_num = race.get('round', 'N/A')
        date = race.get('date', 'TBC')
        gp_name = race.get('gp_name', 'Unknown Grand Prix')
        country = race.get('country', 'N/A')
        
        print(f"{round_num:<6} {date:<12} {gp_name:<30} {country:<15}")
    
    print("\n==== SESSION DETAILS ====\n")
    for race in calendar:
        gp_name = race.get('gp_name', 'Unknown Grand Prix')
        sessions = race.get('sessions', {})
        
        if sessions:
            print(f"\n{gp_name}:")
            
            for session_type, session_info in sessions.items():
                session_name = {
                    'FP1': 'Practice 1',
                    'FP2': 'Practice 2',
                    'FP3': 'Practice 3',
                    'Q': 'Qualifying',
                    'S': 'Sprint',
                    'R': 'Race'
                }.get(session_type, session_type)
                
                date = session_info.get('date', 'TBC')
                time = session_info.get('time', 'TBC')
                
                print(f"  {session_name:<12}: {date} {time}")

def main():
    """Main function"""
    try:
        # Setup cache
        cache_dir = setup_cache()
        print(f"FastF1 cache enabled in {cache_dir}")
        
        # Get current year as default
        current_year = 2025
        
        # Get race calendar
        calendar = get_race_calendar(current_year)
        
        # Print calendar
        print_calendar(calendar)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 