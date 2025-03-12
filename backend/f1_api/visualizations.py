"""
Visualizations Module

This module provides functions for creating visualizations from processed F1 data.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

# Set up visualization settings
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("talk")

# Define F1 color palette
F1_COLORS = {
    'Mercedes': '#00D2BE',
    'Red Bull': '#0600EF',
    'Ferrari': '#DC0000',
    'Racing Point': '#F596C8',
    'Aston Martin': '#006F62',
    'Alpine': '#0090FF',
    'Renault': '#FFF500',
    'AlphaTauri': '#2B4562',
    'McLaren': '#FF8700',
    'Haas': '#FFFFFF',
    'Alfa Romeo': '#900000',
    'Williams': '#005AFF',
    'AlphaTauri Honda': '#2B4562',
    'Alfa Romeo Racing': '#900000',
    'Racing Point BWT': '#F596C8'
}

# Create assets directory if it doesn't exist
ASSETS_DIR = os.path.join('assets', 'visualizations')
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

def create_visualization(data, analysis_type, filename_prefix):
    """
    Create visualization based on the analysis type
    
    Args:
        data (dict): Processed data for visualization
        analysis_type (str): Type of analysis/visualization to create
        filename_prefix (str): Prefix for the output file
        
    Returns:
        str: Path to the created visualization file
    """
    if analysis_type == 'driver_performance':
        return visualize_driver_performance(data, filename_prefix)
    elif analysis_type == 'race_analysis':
        return visualize_race_results(data, filename_prefix)
    elif analysis_type == 'driver_comparison':
        return visualize_driver_comparison(data, filename_prefix)
    elif analysis_type == 'qualifying_analysis':
        return visualize_qualifying_results(data, filename_prefix)
    else:
        print(f"Unknown analysis type: {analysis_type}")
        return None

def visualize_driver_performance(data, filename_prefix):
    """
    Create visualization of driver performance
    
    Args:
        data (dict): Processed driver performance data
        filename_prefix (str): Prefix for the output file
        
    Returns:
        str: Path to the created visualization file
    """
    # Extract data
    driver_code = data['driver_info']['code']
    driver_name = data['driver_info']['name']
    team = data['driver_info']['team']
    year = data['session_info']['year']
    gp_name = data['session_info']['gp_name']
    session_type = data['session_info']['session_type']
    
    # Convert session type to full name
    session_name = {
        'R': 'Race',
        'Q': 'Qualifying',
        'FP1': 'Practice 1',
        'FP2': 'Practice 2',
        'FP3': 'Practice 3',
        'S': 'Sprint'
    }.get(session_type, session_type)
    
    # Get data for plotting
    lap_numbers = [lap['lap_number'] for lap in data['lap_times']]
    lap_times = [lap['lap_time'] for lap in data['lap_times']]
    
    # Create a pandas DataFrame for easier plotting
    df = pd.DataFrame({
        'Lap': lap_numbers,
        'LapTime': lap_times
    })
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 15))
    gs = gridspec.GridSpec(3, 2, height_ratios=[2, 1, 1])
    
    # Plot lap times
    ax1 = plt.subplot(gs[0, :])
    sns.lineplot(x='Lap', y='LapTime', data=df, marker='o', color=F1_COLORS.get(team, 'blue'), linewidth=2, ax=ax1)
    ax1.set_title(f"{driver_name} ({driver_code}) - {year} {gp_name} {session_name}", fontsize=16)
    ax1.set_xlabel('Lap Number', fontsize=12)
    ax1.set_ylabel('Lap Time (seconds)', fontsize=12)
    ax1.grid(True)
    
    # Highlight fastest lap
    if data['performance']['fastest_lap_number'] in lap_numbers:
        fastest_lap_idx = lap_numbers.index(data['performance']['fastest_lap_number'])
        ax1.plot(data['performance']['fastest_lap_number'], lap_times[fastest_lap_idx], 'ro', markersize=10, label='Fastest Lap')
        ax1.legend()
    
    # Plot sector times if available
    if data['sector_times']:
        ax2 = plt.subplot(gs[1, 0])
        
        sector_df = pd.DataFrame([
            {
                'Lap': sector['lap_number'],
                'Sector': 'Sector 1',
                'Time': sector['sector_1']
            } for sector in data['sector_times']
        ] + [
            {
                'Lap': sector['lap_number'],
                'Sector': 'Sector 2',
                'Time': sector['sector_2']
            } for sector in data['sector_times']
        ] + [
            {
                'Lap': sector['lap_number'],
                'Sector': 'Sector 3',
                'Time': sector['sector_3']
            } for sector in data['sector_times']
        ])
        
        sns.lineplot(x='Lap', y='Time', hue='Sector', data=sector_df, marker='o', ax=ax2)
        ax2.set_title('Sector Times', fontsize=14)
        ax2.set_xlabel('Lap Number', fontsize=12)
        ax2.set_ylabel('Sector Time (seconds)', fontsize=12)
        ax2.grid(True)
    
    # Plot tire compounds if available
    if data['tire_data']:
        ax3 = plt.subplot(gs[1, 1])
        
        # Define tire compound colors
        compound_colors = {
            'SOFT': 'red',
            'MEDIUM': 'yellow',
            'HARD': 'white',
            'INTERMEDIATE': 'green',
            'WET': 'blue'
        }
        
        # Create a tire usage plot
        for i, tire in enumerate(data['tire_data']):
            compound = tire['compound']
            laps = tire['laps']
            if laps:
                ax3.plot([min(laps), max(laps)], [i, i], linewidth=10, 
                        color=compound_colors.get(compound, 'gray'), 
                        solid_capstyle='butt', 
                        label=f"{compound} (Life: {tire['tyre_life']})")
        
        ax3.set_yticks(range(len(data['tire_data'])))
        ax3.set_yticklabels([])
        ax3.set_title('Tire Compounds Used', fontsize=14)
        ax3.set_xlabel('Lap Number', fontsize=12)
        ax3.grid(True)
        ax3.legend()
    
    # Add information text box
    info_text = (
        f"Driver: {driver_name} ({driver_code})\n"
        f"Team: {team}\n"
        f"Session: {year} {gp_name} {session_name}\n"
    )
    
    if data['performance']['position'] is not None:
        info_text += f"Position: {data['performance']['position']}\n"
    
    if data['performance']['fastest_lap_time'] is not None:
        fastest_time = str(timedelta(seconds=data['performance']['fastest_lap_time']))[:-3]
        info_text += f"Fastest Lap: {fastest_time} (Lap {data['performance']['fastest_lap_number']})\n"
    
    if data['performance']['status'] is not None:
        info_text += f"Status: {data['performance']['status']}\n"
    
    ax4 = plt.subplot(gs[2, :])
    ax4.axis('off')
    ax4.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=14, 
             bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=1'))
    
    # Adjust layout and save figure
    plt.tight_layout()
    
    # Create filename and save
    filename = f"{filename_prefix}.png"
    filepath = os.path.join(ASSETS_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    
    plt.close(fig)
    return filepath

def visualize_race_results(data, filename_prefix):
    """
    Create visualization of race results
    
    Args:
        data (dict): Processed race data
        filename_prefix (str): Prefix for the output file
        
    Returns:
        str: Path to the created visualization file
    """
    # Extract data
    year = data['race_info']['year']
    gp_name = data['race_info']['gp_name']
    circuit = data['race_info']['circuit']
    results = data['results']
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 15))
    gs = gridspec.GridSpec(2, 2, height_ratios=[3, 2])
    
    # Plot race results (finishing positions)
    ax1 = plt.subplot(gs[0, :])
    
    # Create a DataFrame for the results
    results_df = pd.DataFrame(results)
    
    # Get only the top 10 or fewer if there are less than 10 results
    top_n = min(10, len(results_df))
    top_results = results_df.head(top_n)
    
    # Extract team colors
    team_colors = [F1_COLORS.get(team, '#333333') for team in top_results['team']]
    
    # Create a horizontal bar chart
    bars = ax1.barh(range(top_n), [1] * top_n, color=team_colors, height=0.6)
    
    # Add driver names and positions
    for i, (_, row) in enumerate(top_results.iterrows()):
        ax1.text(0.02, i, f"{row['position']}. {row['driver_code']} - {row['team']}", 
                 va='center', color='white', fontweight='bold', fontsize=12)
        
        # Add driver points
        if 'points' in row:
            ax1.text(0.9, i, f"{row['points']} pts", 
                    va='center', ha='right', color='white', fontweight='bold', fontsize=12)
    
    ax1.set_title(f"{year} {gp_name} Grand Prix - Top {top_n} Results", fontsize=16)
    ax1.set_yticks([])
    ax1.set_xticks([])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    
    # Show grid-to-finish positions if we have more than 10 drivers
    if len(results_df) > 0:
        ax2 = plt.subplot(gs[1, 0])
        
        # Create data for grid vs finish
        grid_finish_df = results_df[['driver_code', 'grid', 'position']]
        grid_finish_df['grid'] = pd.to_numeric(grid_finish_df['grid'], errors='coerce')
        grid_finish_df['position'] = pd.to_numeric(grid_finish_df['position'], errors='coerce')
        
        # Remove any rows with NaN values
        grid_finish_df = grid_finish_df.dropna()
        
        # Plot grid vs finish with lines connecting them
        for _, row in grid_finish_df.iterrows():
            ax2.plot([1, 2], [row['grid'], row['position']], 'o-', 
                    color=F1_COLORS.get(results_df.loc[results_df['driver_code'] == row['driver_code'], 'team'].iloc[0], '#333333'),
                    linewidth=2, markersize=8)
            ax2.text(1, row['grid'], row['driver_code'], ha='right', va='center', fontsize=10)
            ax2.text(2, row['position'], row['driver_code'], ha='left', va='center', fontsize=10)
        
        ax2.set_xlim(0.5, 2.5)
        ax2.set_xticks([1, 2])
        ax2.set_xticklabels(['Grid', 'Finish'])
        ax2.set_title('Grid vs Finish Positions', fontsize=14)
        ax2.set_ylabel('Position', fontsize=12)
        ax2.invert_yaxis()  # Invert y-axis to have position 1 at the top
        ax2.grid(True)
    
    # Add information about the race
    ax3 = plt.subplot(gs[1, 1])
    ax3.axis('off')
    
    info_text = (
        f"Race: {year} {gp_name} Grand Prix\n"
        f"Circuit: {circuit}\n"
        f"Date: {data['race_info'].get('date', 'N/A')}\n"
        f"Country: {data['race_info'].get('country', 'N/A')}\n"
    )
    
    # Add weather information if available
    if 'weather' in data and data['weather']:
        # Get the most common weather condition
        weather_conditions = [w.get('air_temperature') for w in data['weather'] if w.get('air_temperature')]
        if weather_conditions:
            avg_temp = sum(weather_conditions) / len(weather_conditions)
            info_text += f"Average Temperature: {avg_temp:.1f}°C\n"
    
    ax3.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=14, 
             bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=1'))
    
    # Adjust layout and save figure
    plt.tight_layout()
    
    # Create filename and save
    filename = f"{filename_prefix}.png"
    filepath = os.path.join(ASSETS_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    
    plt.close(fig)
    return filepath

def visualize_driver_comparison(data, filename_prefix):
    """
    Create visualization comparing two drivers
    
    Args:
        data (dict): Processed driver comparison data
        filename_prefix (str): Prefix for the output file
        
    Returns:
        str: Path to the created visualization file
    """
    # Check if we have an error
    if 'error' in data:
        print(f"Error: {data['error']}")
        return None
    
    # Extract data
    year = data['session_info']['year']
    gp_name = data['session_info']['gp_name']
    session_type = data['session_info']['session_type']
    
    driver1 = data['drivers'][0]
    driver2 = data['drivers'][1]
    
    # Convert session type to full name
    session_name = {
        'R': 'Race',
        'Q': 'Qualifying',
        'FP1': 'Practice 1',
        'FP2': 'Practice 2',
        'FP3': 'Practice 3',
        'S': 'Sprint'
    }.get(session_type, session_type)
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 15))
    gs = gridspec.GridSpec(3, 2, height_ratios=[2, 2, 1])
    
    # Plot lap times for both drivers
    ax1 = plt.subplot(gs[0, :])
    
    # Create DataFrames for each driver's lap times
    df1 = pd.DataFrame(driver1['lap_times'])
    df2 = pd.DataFrame(driver2['lap_times'])
    
    if not df1.empty and not df2.empty:
        # Plot both drivers' lap times
        line1 = ax1.plot(df1['lap_number'], df1['lap_time'], 'o-', 
                        color=F1_COLORS.get(driver1['team'], 'blue'), 
                        linewidth=2, markersize=6, 
                        label=f"{driver1['code']} ({driver1['team']})")
        
        line2 = ax1.plot(df2['lap_number'], df2['lap_time'], 'o-', 
                        color=F1_COLORS.get(driver2['team'], 'red'), 
                        linewidth=2, markersize=6, 
                        label=f"{driver2['code']} ({driver2['team']})")
        
        ax1.set_title(f"Lap Time Comparison: {driver1['code']} vs {driver2['code']} - {year} {gp_name} {session_name}", fontsize=16)
        ax1.set_xlabel('Lap Number', fontsize=12)
        ax1.set_ylabel('Lap Time (seconds)', fontsize=12)
        ax1.grid(True)
        ax1.legend()
    
    # Plot lap time differences
    ax2 = plt.subplot(gs[1, 0])
    
    if data['lap_time_diff']:
        # Create a DataFrame for the differences
        diff_df = pd.DataFrame(data['lap_time_diff'])
        
        # Plot the time differences
        bars = ax2.bar(diff_df['lap_number'], diff_df['time_diff'], 
                      color=['green' if x < 0 else 'red' for x in diff_df['time_diff']])
        
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax2.set_title(f"Lap Time Difference ({driver1['code']} - {driver2['code']})", fontsize=14)
        ax2.set_xlabel('Lap Number', fontsize=12)
        ax2.set_ylabel('Time Difference (seconds)', fontsize=12)
        ax2.grid(True)
        
        # Add annotation explaining the colors
        ax2.text(0.02, 0.95, 
                f"Green: {driver1['code']} faster\nRed: {driver2['code']} faster", 
                transform=ax2.transAxes, fontsize=12, 
                bbox=dict(facecolor='white', alpha=0.8))
    
    # Plot sector time differences
    ax3 = plt.subplot(gs[1, 1])
    
    if data['sector_time_diff']:
        # Create a DataFrame for the sector differences
        sector_diff_df = pd.DataFrame(data['sector_time_diff'])
        
        # Melt the DataFrame to get it in the right format for seaborn
        melted_df = pd.melt(sector_diff_df, id_vars=['lap_number'], 
                           value_vars=['sector_1_diff', 'sector_2_diff', 'sector_3_diff'],
                           var_name='Sector', value_name='Time Difference')
        
        # Map sector names to cleaner labels
        melted_df['Sector'] = melted_df['Sector'].map({
            'sector_1_diff': 'Sector 1',
            'sector_2_diff': 'Sector 2',
            'sector_3_diff': 'Sector 3'
        })
        
        # Plot the sector time differences
        sns.barplot(x='lap_number', y='Time Difference', hue='Sector', data=melted_df, ax=ax3)
        
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax3.set_title(f"Sector Time Differences ({driver1['code']} - {driver2['code']})", fontsize=14)
        ax3.set_xlabel('Lap Number', fontsize=12)
        ax3.set_ylabel('Time Difference (seconds)', fontsize=12)
        ax3.grid(True)
    
    # Add information text box
    info_text = (
        f"Session: {year} {gp_name} {session_name}\n\n"
        f"Driver 1: {driver1['name']} ({driver1['code']})\n"
        f"Team: {driver1['team']}\n"
    )
    
    if driver1['fastest_lap_time'] is not None:
        fastest_time1 = str(timedelta(seconds=driver1['fastest_lap_time']))[:-3]
        info_text += f"Fastest Lap: {fastest_time1} (Lap {driver1['fastest_lap_number']})\n\n"
    
    info_text += (
        f"Driver 2: {driver2['name']} ({driver2['code']})\n"
        f"Team: {driver2['team']}\n"
    )
    
    if driver2['fastest_lap_time'] is not None:
        fastest_time2 = str(timedelta(seconds=driver2['fastest_lap_time']))[:-3]
        info_text += f"Fastest Lap: {fastest_time2} (Lap {driver2['fastest_lap_number']})\n"
    
    # Calculate fastest lap time difference if both drivers have fastest lap times
    if driver1['fastest_lap_time'] is not None and driver2['fastest_lap_time'] is not None:
        fastest_diff = driver1['fastest_lap_time'] - driver2['fastest_lap_time']
        faster_driver = driver1['code'] if fastest_diff < 0 else driver2['code']
        abs_diff = abs(fastest_diff)
        diff_str = str(timedelta(seconds=abs_diff))[:-3]
        
        info_text += f"\nFastest Lap Difference: {diff_str} ({faster_driver} faster)"
    
    ax4 = plt.subplot(gs[2, :])
    ax4.axis('off')
    ax4.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=14, 
             bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=1'))
    
    # Adjust layout and save figure
    plt.tight_layout()
    
    # Create filename and save
    filename = f"{filename_prefix}.png"
    filepath = os.path.join(ASSETS_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    
    plt.close(fig)
    return filepath

def visualize_qualifying_results(data, filename_prefix):
    """
    Create visualization of qualifying results
    
    Args:
        data (dict): Processed qualifying data
        filename_prefix (str): Prefix for the output file
        
    Returns:
        str: Path to the created visualization file
    """
    # Extract data
    year = data['qualifying_info']['year']
    gp_name = data['qualifying_info']['gp_name']
    circuit = data['qualifying_info']['circuit']
    results = data['results']
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 15))
    gs = gridspec.GridSpec(2, 2, height_ratios=[3, 2])
    
    # Plot qualifying results (grid positions)
    ax1 = plt.subplot(gs[0, :])
    
    # Create a DataFrame for the results
    results_df = pd.DataFrame(results)
    
    # Convert time columns to numeric values (seconds)
    if 'q1_time' in results_df.columns:
        results_df['q1_time'] = pd.to_numeric(results_df['q1_time'], errors='coerce')
    if 'q2_time' in results_df.columns:
        results_df['q2_time'] = pd.to_numeric(results_df['q2_time'], errors='coerce')
    if 'q3_time' in results_df.columns:
        results_df['q3_time'] = pd.to_numeric(results_df['q3_time'], errors='coerce')
    
    # Add a column for the best time (used for sorting)
    results_df['best_time'] = results_df[['q1_time', 'q2_time', 'q3_time']].min(axis=1, skipna=True)
    
    # Sort by position for plotting
    results_df = results_df.sort_values('position')
    
    # Get the top 10 or all results if there are fewer than 10
    top_n = min(10, len(results_df))
    top_results = results_df.head(top_n)
    
    # Plot Q3 times for top 10 (or Q2 or Q1 if Q3 not available)
    bar_data = []
    bar_colors = []
    for _, row in top_results.iterrows():
        if not pd.isna(row.get('q3_time')):
            bar_data.append(row['q3_time'])
            session = 'Q3'
        elif not pd.isna(row.get('q2_time')):
            bar_data.append(row['q2_time'])
            session = 'Q2'
        elif not pd.isna(row.get('q1_time')):
            bar_data.append(row['q1_time'])
            session = 'Q1'
        else:
            bar_data.append(0)
            session = 'Unknown'
        
        bar_colors.append(F1_COLORS.get(row['team'], '#333333'))
    
    # Horizontal bar chart for qualifying times
    bars = ax1.barh(range(len(bar_data)), bar_data, color=bar_colors, height=0.6)
    
    # Add driver names and positions
    for i, (_, row) in enumerate(top_results.iterrows()):
        # Format the time as MM:SS.sss
        if bar_data[i] > 0:
            time_str = str(timedelta(seconds=bar_data[i]))[:-3]
            ax1.text(bar_data[i] + 0.1, i, f"{row['driver_code']} - {time_str}", 
                    va='center', fontsize=12)
        
        # Add position number and team
        ax1.text(-3, i, f"{row['position']}. {row['team']}", ha='right', va='center', fontsize=12,
                color=F1_COLORS.get(row['team'], '#333333'))
    
    ax1.set_title(f"{year} {gp_name} Qualifying - Top {top_n} Results", fontsize=16)
    ax1.set_yticks([])
    ax1.set_xlabel('Lap Time (seconds)', fontsize=12)
    ax1.grid(True, axis='x')
    
    # Get pole time for relative comparison
    if top_results.shape[0] > 0:
        pole_time = top_results.iloc[0]['best_time']
        
        # Highlight pole position
        ax1.axvline(x=pole_time, color='red', linestyle='--', linewidth=1, alpha=0.7)
        ax1.text(pole_time, -0.8, 'Pole', ha='right', va='center', color='red', fontsize=10)
    
    # Plot session progression (Q1 → Q2 → Q3)
    ax2 = plt.subplot(gs[1, 0])
    
    # Collect data for all qualifying sessions
    q1_data = data['q1_times']
    q2_data = data['q2_times']
    q3_data = data['q3_times']
    
    # Create a DataFrame for session progression
    progression_data = []
    
    # Process Q1 data
    for item in q1_data:
        progression_data.append({
            'driver_code': item['driver_code'],
            'session': 'Q1',
            'time': item['time']
        })
    
    # Process Q2 data
    for item in q2_data:
        progression_data.append({
            'driver_code': item['driver_code'],
            'session': 'Q2',
            'time': item['time']
        })
    
    # Process Q3 data
    for item in q3_data:
        progression_data.append({
            'driver_code': item['driver_code'],
            'session': 'Q3',
            'time': item['time']
        })
    
    if progression_data:
        # Convert to DataFrame
        progression_df = pd.DataFrame(progression_data)
        
        # Get top 5 drivers (by final position) for clearer visualization
        top_drivers = results_df.head(5)['driver_code'].tolist()
        
        # Filter for only these drivers
        progression_df_filtered = progression_df[progression_df['driver_code'].isin(top_drivers)]
        
        # Plot the progression
        sns.lineplot(x='session', y='time', hue='driver_code', style='driver_code',
                    markers=True, linewidth=2, markersize=10,
                    data=progression_df_filtered, ax=ax2)
        
        ax2.set_title('Qualifying Session Progression (Top 5 Drivers)', fontsize=14)
        ax2.set_xlabel('Session', fontsize=12)
        ax2.set_ylabel('Lap Time (seconds)', fontsize=12)
        ax2.grid(True)
    
    # Plot lap time improvements from Q1→Q2 and Q2→Q3
    ax3 = plt.subplot(gs[1, 1])
    
    if data['lap_time_improvements']:
        # Convert to DataFrame
        improvements_df = pd.DataFrame(data['lap_time_improvements'])
        
        # Create a new column for session transition
        improvements_df['transition'] = improvements_df['from_session'] + '→' + improvements_df['to_session']
        
        # Group by driver and transition, get the max improvement
        grouped_improvements = improvements_df.groupby(['driver_code', 'transition'])['improvement'].max().reset_index()
        
        # Plot improvements
        sns.barplot(x='driver_code', y='improvement', hue='transition', data=grouped_improvements, ax=ax3)
        
        ax3.set_title('Lap Time Improvements Between Sessions', fontsize=14)
        ax3.set_xlabel('Driver', fontsize=12)
        ax3.set_ylabel('Improvement (seconds)', fontsize=12)
        ax3.grid(True)
        plt.xticks(rotation=45)
    
    # Adjust layout and save figure
    plt.tight_layout()
    
    # Create filename and save
    filename = f"{filename_prefix}.png"
    filepath = os.path.join(ASSETS_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    
    plt.close(fig)
    return filepath 