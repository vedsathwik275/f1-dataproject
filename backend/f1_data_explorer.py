import fastf1
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create cache directory if it doesn't exist
CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Enable FastF1 cache
fastf1.Cache.enable_cache(CACHE_DIR)

def get_openf1_session_data(year, round_number):
    """Fetch session data from OpenF1 API"""
    url = f"https://api.openf1.org/v1/sessions?year={year}&round={round_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Print response for debugging
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Content: {response.text[:200]}...")  # Print first 200 chars
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OpenF1 API: {e}")
        return []

def get_fastf1_lap_times(year, gp_name, session='Q'):
    """Fetch lap times using FastF1"""
    try:
        # Load the session
        print(f"Loading {year} {gp_name} {session} session...")
        session = fastf1.get_session(year, gp_name, session)
        session.load()
        
        # Get lap times for all drivers
        laps = session.laps
        return laps
    except Exception as e:
        print(f"Error loading FastF1 session: {e}")
        return None

def main():
    # Example: Analyze 2023 Bahrain GP Qualifying (using previous year's data)
    YEAR = 2024
    ROUND = 1
    GP_NAME = 'Bahrain'
    
    print(f"\nAnalyzing {YEAR} {GP_NAME} Grand Prix")
    print("======================================")
    
    print("\nFetching data from OpenF1 API...")
    openf1_data = get_openf1_session_data(YEAR, ROUND)
    if openf1_data:
        print("\nSession information from OpenF1:")
        for session in openf1_data:
            print(f"Type: {session.get('session_type', 'N/A')}, Date: {session.get('date', 'N/A')}")
    
    print("\nFetching data from FastF1 API...")
    laps_data = get_fastf1_lap_times(YEAR, GP_NAME, 'Q')
    
    if laps_data is not None and not laps_data.empty:
        try:
            # Create a simple visualization of qualifying lap times
            plt.figure(figsize=(12, 6))
            sns.boxplot(data=laps_data, x='Driver', y='LapTime', palette='viridis')
            plt.title(f'{YEAR} {GP_NAME} GP - Qualifying Lap Times')
            plt.xticks(rotation=45)
            plt.ylabel('Lap Time (seconds)')
            plt.tight_layout()
            plt.savefig('qualifying_laptimes.png')
            print("\nCreated visualization: qualifying_laptimes.png")
        except Exception as e:
            print(f"\nError creating visualization: {e}")
    else:
        print("\nNo lap data available to create visualization.")

if __name__ == "__main__":
    main() 