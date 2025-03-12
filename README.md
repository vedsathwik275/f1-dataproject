# F1 Data Analysis Project

A comprehensive Formula 1 data analysis and visualization tool that leverages both FastF1 and OpenF1 APIs to provide deep insights into race performance, driver statistics, and more.

## Features

- **Driver Performance Analysis**: Analyze a driver's performance across sessions, including lap times, sector times, and tire strategies.
- **Race Results Visualization**: Visualize race results with detailed finishing order, grid vs. finish position comparisons, and more.
- **Driver Comparisons**: Compare two drivers head-to-head with lap time and sector time differences.
- **Qualifying Analysis**: Analyze qualifying sessions with progression through Q1, Q2, and Q3, and lap time improvements.
- **Interactive Terminal Interface**: Easy-to-use command-line interface for accessing all features.
- **Multi-Season Analysis (2021-2025)**: Analyze historical performance across multiple seasons for drivers, teams, and circuits.
- **Season Comparison**: Compare championship standings and results across seasons.
- **Detailed Calendar View**: View complete race calendars for any season with upcoming race information.

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the F1 Data Analyzer application:
```bash
python run_f1_analyzer.py
```

### Available Commands

- `driver_performance` - Analyze a specific driver's performance for a race
- `race_analysis` - Analyze a specific race
- `compare_drivers` - Compare two drivers' performance
- `qualifying_analysis` - Analyze qualifying session
- `list_races` - List available races for a given year
- `list_drivers` - List available drivers for a given year
- `multi_season_driver` - Analyze a driver's performance across multiple seasons (2021-2025)
- `multi_season_team` - Analyze a team's performance across multiple seasons (2021-2025)
- `circuit_history` - Analyze a circuit's history across multiple seasons (2021-2025)
- `season_comparison` - Compare championship standings across multiple seasons (2021-2025)
- `get_calendar` - Display the full F1 calendar for a specified year
- `help` - Show the help message
- `exit` - Exit the application

### Available Drivers (2025 Season)

The following is a list of common driver codes and their respective teams for the 2025 season:

| Driver Code | Driver Name           | Team                |
|-------------|----------------------|---------------------|
| VER         | Max Verstappen       | Red Bull Racing     |
| PER         | Sergio Perez         | Red Bull Racing     |
| HAM         | Lewis Hamilton       | Ferrari             |
| RUS         | George Russell       | Mercedes            |
| LEC         | Charles Leclerc      | Ferrari            |
| SAI         | Carlos Sainz         | Williams           |
| ALO         | Fernando Alonso      | Aston Martin       |
| STR         | Lance Stroll         | Aston Martin       |
| NOR         | Lando Norris         | McLaren            |
| PIA         | Oscar Piastri        | McLaren            |
| GAS         | Pierre Gasly         | Alpine             |
| OCO         | Esteban Ocon         | Haas F1 Team       |
| HUL         | Nico Hulkenberg      | Kick Sauber        |
| MAG         | Kevin Magnussen      | Haas F1 Team       |
| BOT         | Valtteri Bottas      | Kick Sauber        |
| ZHO         | Guanyu Zhou          | Kick Sauber        |
| TSU         | Yuki Tsunoda         | RB                 |
| RIC         | Daniel Ricciardo     | RB                 |
| ALB         | Alexander Albon      | Williams           |
| BEA         | Franco Colapinto     | Williams           |
| BEA         | Andrea Kimi Antonelli| Mercedes           |
| LAW         | Liam Lawson          | RB                 |

### 2025 Race Calendar

| Round | Grand Prix Name        | Circuit                | Date        |
|-------|------------------------|------------------------|-------------|
| 1     | Australian Grand Prix  | Albert Park           | Mar 16      |
| 2     | Chinese Grand Prix     | Shanghai              | Mar 23      |
| 3     | Japanese Grand Prix    | Suzuka                | Apr 06      |
| 4     | Bahrain Grand Prix     | Bahrain International | Apr 13      |
| 5     | Saudi Arabian Grand Prix| Jeddah               | Apr 20      |
| 6     | Miami Grand Prix       | Miami International   | May 04      |
| 7     | Emilia Romagna Grand Prix| Imola               | May 18      |
| 8     | Monaco Grand Prix      | Circuit de Monaco     | May 25      |
| 9     | Spanish Grand Prix     | Circuit de Barcelona-Catalunya | Jun 01 |
| 10    | Canadian Grand Prix    | Circuit Gilles Villeneuve | Jun 15  |
| 11    | Austrian Grand Prix    | Red Bull Ring         | Jun 29      |
| 12    | British Grand Prix     | Silverstone           | Jul 06      |
| 13    | Belgian Grand Prix     | Spa-Francorchamps     | Jul 27      |
| 14    | Hungarian Grand Prix   | Hungaroring           | Aug 03      |
| 15    | Dutch Grand Prix       | Zandvoort             | Aug 31      |
| 16    | Italian Grand Prix     | Monza                 | Sep 07      |
| 17    | Azerbaijan Grand Prix  | Baku City Circuit     | Sep 21      |
| 18    | Singapore Grand Prix   | Marina Bay            | Oct 05      |
| 19    | United States Grand Prix| Circuit of the Americas | Oct 19    |
| 20    | Mexico City Grand Prix | Autodromo Hermanos Rodriguez | Oct 26 |
| 21    | São Paulo Grand Prix   | Interlagos            | Nov 09      |
| 22    | Las Vegas Grand Prix   | Las Vegas Street Circuit | Nov 22   |
| 23    | Qatar Grand Prix       | Lusail International  | Nov 30      |
| 24    | Abu Dhabi Grand Prix   | Yas Marina            | Dec 07      |

### Session Types

When analyzing data, you can specify the following session types:

| Code | Session Type       | Description                        |
|------|-------------------|------------------------------------|
| R    | Race              | Main Grand Prix race               |
| Q    | Qualifying        | All qualifying sessions (Q1, Q2, Q3) |
| FP1   | Practice 1        | First practice session             |
| FP2   | Practice 2        | Second practice session            |
| FP3   | Practice 3        | Third practice session             |
| S    | Sprint            | Sprint race (at selected events)   |
| SQ   | Sprint Qualifying | Sprint qualifying session          |

## Project Structure

```
backend/
├── f1_analyzer.py         # Main application file
├── run_f1_analyzer.py     # Script to run the application
├── requirements.txt       # Dependencies
├── README.md              # This file
├── assets/                # Visualization output directory
│   └── visualizations/    # Generated visualizations
├── cache/                 # FastF1 cache directory
└── f1_api/                # API modules
    ├── __init__.py        # Package initialization
    ├── fastf1_client.py   # FastF1 API client
    ├── openf1_client.py   # OpenF1 API client
    ├── data_processor.py  # Data processing utilities
    ├── visualizations.py  # Visualization utilities
    └── historical_data.py # Multi-season analysis module
```

## Data Sources

### FastF1 API
FastF1 is a Python package that provides access to Formula 1 session data, including:
- Detailed session data (lap times, sector times)
- Telemetry data (speed, throttle, brake, DRS)
- Car data (RPM, gear)
- Weather data
- Track position
- Historical data from past seasons

### OpenF1 API
OpenF1 is a free and open API that provides access to Formula 1 data, including:
- Session information
- Live timing data
- Driver information
- Team information
- Weather data

## Examples

### Driver Performance Analysis
Get detailed performance analysis for a specific driver in a race:
1. Run `python run_f1_analyzer.py`
2. Enter `driver_performance`
3. Follow the prompts:
   - Enter driver code (e.g., 'VER', 'HAM')
   - Enter year (e.g., '2025', '2024')
   - Enter Grand Prix name (e.g., 'Bahrain', 'Monaco')
   - Enter session type (e.g., 'R' for race, 'Q' for qualifying)

Example output will show:
- Lap time progression throughout the race
- Sector time analysis
- Tire compound usage
- Key performance metrics

### Race Analysis
Analyze a complete race:
1. Run `python run_f1_analyzer.py`
2. Enter `race_analysis`
3. Follow the prompts:
   - Enter year (e.g., '2025', '2024')
   - Enter Grand Prix name (e.g., 'Bahrain', 'Monaco')

Example output will show:
- Race results with finishing positions
- Grid vs. finish position comparison
- Race information and statistics

### Driver Comparison
Compare two drivers head-to-head:
1. Run `python run_f1_analyzer.py`
2. Enter `compare_drivers`
3. Follow the prompts:
   - Enter first driver code (e.g., 'VER')
   - Enter second driver code (e.g., 'HAM')
   - Enter year (e.g., '2025', '2024')
   - Enter Grand Prix name (e.g., 'Bahrain', 'Monaco')
   - Enter session type (e.g., 'R' for race, 'Q' for qualifying)

Example output will show:
- Lap time comparison between the two drivers
- Lap time differences
- Sector time differences
- Performance statistics comparison

### Qualifying Analysis
Analyze a qualifying session:
1. Run `python run_f1_analyzer.py`
2. Enter `qualifying_analysis`
3. Follow the prompts:
   - Enter year (e.g., '2025', '2024')
   - Enter Grand Prix name (e.g., 'Bahrain', 'Monaco')

Example output will show:
- Qualifying results with positions
- Session progression (Q1 → Q2 → Q3)
- Lap time improvements between sessions

### Multi-Season Driver Analysis
Analyze a driver's performance across multiple seasons (2021-2025):
1. Run `python run_f1_analyzer.py`
2. Enter `multi_season_driver`
3. Follow the prompts:
   - Enter driver code (e.g., 'VER', 'HAM')
   - Optionally filter by Grand Prix name

Example output will show:
- Season-by-season performance metrics
- Total wins, podiums, and points across seasons
- Best and worst performing seasons
- Performance trends over time

### Team Performance Analysis
Analyze a team's performance across multiple seasons (2021-2025):
1. Run `python run_f1_analyzer.py`
2. Enter `multi_season_team`
3. Follow the prompt:
   - Enter team name (e.g., 'Red Bull Racing', 'Mercedes')

Example output will show:
- Season-by-season team performance
- Driver lineups by season
- Championship position trends
- Win and podium statistics

### Circuit History Analysis
Analyze the history of a specific circuit across seasons (2021-2025):
1. Run `python run_f1_analyzer.py`
2. Enter `circuit_history`
3. Follow the prompt:
   - Enter Grand Prix name (e.g., 'Monaco', 'Monza')

Example output will show:
- Winners for each season
- Pole positions and fastest laps
- Most successful drivers at the circuit
- Podium results for each year

### Championship Comparison
Compare championship results across seasons (2021-2025):
1. Run `python run_f1_analyzer.py`
2. Enter `season_comparison`

Example output will show:
- Driver champions by year
- Constructor champions by year
- Points comparisons
- Championship trends

### Get F1 Calendar
View the complete F1 calendar for any year:
1. Run `python run_f1_analyzer.py`
2. Enter `get_calendar`
3. Follow the prompt:
   - Enter year (e.g., '2025', '2024')

Example output will show:
- Complete race schedule with dates and locations
- Upcoming race information for current season
- Session schedule for the next race
- Circuit and country information

### List Available Races
Get a list of all races for a specific year:
1. Run `python run_f1_analyzer.py`
2. Enter `list_races`
3. Follow the prompt:
   - Enter year (e.g., '2025', '2024')

### List Available Drivers
Get a list of all drivers for a specific year:
1. Run `python run_f1_analyzer.py`
2. Enter `list_drivers`
3. Follow the prompts:
   - Enter year (e.g., '2025', '2024')
   - Enter Grand Prix name (optional, press Enter to use the most recent race)

## Visualization Output

All visualizations are saved to the `assets/visualizations/` directory with descriptive filenames in the format:
- Driver performance: `{DRIVER_CODE}_{YEAR}_{GP_NAME}_{SESSION_TYPE}.png`
- Race analysis: `{YEAR}_{GP_NAME}_race.png`
- Driver comparison: `{DRIVER1}_vs_{DRIVER2}_{YEAR}_{GP_NAME}_{SESSION_TYPE}.png`
- Qualifying analysis: `{YEAR}_{GP_NAME}_qualifying.png`

## Troubleshooting

### Common Issues

1. **Missing data for recent races**: The OpenF1 API may not have complete data for the current season. In such cases, the application will fall back to using only FastF1 data.

2. **Session not found**: Make sure you're using the correct Grand Prix name. You can use the `list_races` command to see available races.

3. **Driver not found**: Make sure you're using the correct driver code. You can use the `list_drivers` command to see available drivers.

4. **Package not found errors**: Make sure you've installed all dependencies by running `pip install -r requirements.txt`.

5. **"No module named 'fastf1'"**: Ensure you've activated your virtual environment before running the application.

6. **Slow data loading for historical analysis**: Multi-season analysis can be data-intensive. First-time analysis will be slower as data is cached. Subsequent runs will be faster.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is open source and available under the MIT License. 