# F1 Data Analysis Project

A comprehensive Formula 1 data analysis and visualization tool that leverages both FastF1 and OpenF1 APIs to provide deep insights into race performance, driver statistics, and more.

## Features

- **Driver Performance Analysis**: Analyze a driver's performance across sessions, including lap times, sector times, and tire strategies.
- **Race Results Visualization**: Visualize race results with detailed finishing order, grid vs. finish position comparisons, and more.
- **Driver Comparisons**: Compare two drivers head-to-head with lap time and sector time differences.
- **Qualifying Analysis**: Analyze qualifying sessions with progression through Q1, Q2, and Q3, and lap time improvements.
- **Interactive Terminal Interface**: Easy-to-use command-line interface for accessing all features.

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
- `help` - Show the help message
- `exit` - Exit the application

### Available Drivers (2023 Season)

The following is a list of common driver codes and their respective teams for the 2023 season:

| Driver Code | Driver Name           | Team                |
|-------------|----------------------|---------------------|
| VER         | Max Verstappen       | Red Bull Racing     |
| PER         | Sergio Perez         | Red Bull Racing     |
| HAM         | Lewis Hamilton       | Mercedes           |
| RUS         | George Russell       | Mercedes           |
| LEC         | Charles Leclerc      | Ferrari            |
| SAI         | Carlos Sainz         | Ferrari            |
| ALO         | Fernando Alonso      | Aston Martin       |
| STR         | Lance Stroll         | Aston Martin       |
| NOR         | Lando Norris         | McLaren            |
| PIA         | Oscar Piastri        | McLaren            |
| GAS         | Pierre Gasly         | Alpine             |
| OCO         | Esteban Ocon         | Alpine             |
| HUL         | Nico Hulkenberg      | Haas F1 Team       |
| MAG         | Kevin Magnussen      | Haas F1 Team       |
| BOT         | Valtteri Bottas      | Alfa Romeo         |
| ZHO         | Guanyu Zhou          | Alfa Romeo         |
| TSU         | Yuki Tsunoda         | AlphaTauri         |
| DEV         | Nyck de Vries        | AlphaTauri/RB       |
| RIC         | Daniel Ricciardo     | AlphaTauri/RB       |
| ALB         | Alexander Albon      | Williams           |
| SAR         | Logan Sargeant       | Williams           |

### Available Drivers (2024 Season)

The following is a list of common driver codes and their respective teams for the 2024 season:

| Driver Code | Driver Name           | Team                |
|-------------|----------------------|---------------------|
| VER         | Max Verstappen       | Red Bull Racing     |
| PER         | Sergio Perez         | Red Bull Racing     |
| HAM         | Lewis Hamilton       | Mercedes           |
| RUS         | George Russell       | Mercedes           |
| LEC         | Charles Leclerc      | Ferrari            |
| SAI         | Carlos Sainz         | Ferrari            |
| ALO         | Fernando Alonso      | Aston Martin       |
| STR         | Lance Stroll         | Aston Martin       |
| NOR         | Lando Norris         | McLaren            |
| PIA         | Oscar Piastri        | McLaren            |
| GAS         | Pierre Gasly         | Alpine             |
| OCO         | Esteban Ocon         | Alpine             |
| HUL         | Nico Hulkenberg      | Haas F1 Team       |
| MAG         | Kevin Magnussen      | Haas F1 Team       |
| BOT         | Valtteri Bottas      | Kick Sauber        |
| ZHO         | Guanyu Zhou          | Kick Sauber        |
| TSU         | Yuki Tsunoda         | RB                 |
| RIC         | Daniel Ricciardo     | RB                 |
| ALB         | Alexander Albon      | Williams           |
| SAR         | Logan Sargeant       | Williams           |
| BEA         | Franco Colapinto     | Williams           |

### 2024 Race Calendar

| Round | Grand Prix Name        | Circuit                | Date        |
|-------|------------------------|------------------------|-------------|
| 1     | Bahrain                | Bahrain International  | Mar 02      |
| 2     | Saudi Arabia           | Jeddah                 | Mar 09      |
| 3     | Australia              | Albert Park           | Mar 24      |
| 4     | Japan                  | Suzuka                | Apr 07      |
| 5     | China                  | Shanghai              | Apr 21      |
| 6     | Miami                  | Miami International   | May 05      |
| 7     | Emilia Romagna (Imola) | Autodromo Enzo e Dino Ferrari | May 19 |
| 8     | Monaco                 | Circuit de Monaco     | May 26      |
| 9     | Canada                 | Circuit Gilles Villeneuve | Jun 09  |
| 10    | Spain                  | Circuit de Barcelona-Catalunya | Jun 23 |
| 11    | Austria                | Red Bull Ring         | Jun 30      |
| 12    | Britain                | Silverstone           | Jul 07      |
| 13    | Hungary                | Hungaroring           | Jul 21      |
| 14    | Belgium                | Spa-Francorchamps     | Jul 28      |
| 15    | Netherlands            | Zandvoort             | Aug 25      |
| 16    | Italy                  | Monza                 | Sep 01      |
| 17    | Azerbaijan             | Baku City Circuit     | Sep 15      |
| 18    | Singapore              | Marina Bay            | Sep 22      |
| 19    | United States          | Circuit of the Americas | Oct 20    |
| 20    | Mexico                 | Autodromo Hermanos Rodriguez | Oct 27 |
| 21    | Brazil                 | Interlagos            | Nov 03      |
| 22    | Las Vegas              | Las Vegas Street Circuit | Nov 23   |
| 23    | Qatar                  | Lusail International  | Dec 01      |
| 24    | Abu Dhabi              | Yas Marina            | Dec 08      |

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
    └── visualizations.py  # Visualization utilities
```

## Data Sources

### FastF1 API
FastF1 is a Python package that provides access to Formula 1 session data, including:
- Detailed session data (lap times, sector times)
- Telemetry data (speed, throttle, brake, DRS)
- Car data (RPM, gear)
- Weather data
- Track position

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
   - Enter year (e.g., '2024', '2023')
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
   - Enter year (e.g., '2024', '2023')
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
   - Enter year (e.g., '2024', '2023')
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
   - Enter year (e.g., '2024', '2023')
   - Enter Grand Prix name (e.g., 'Bahrain', 'Monaco')

Example output will show:
- Qualifying results with positions
- Session progression (Q1 → Q2 → Q3)
- Lap time improvements between sessions

### List Available Races
Get a list of all races for a specific year:
1. Run `python run_f1_analyzer.py`
2. Enter `list_races`
3. Follow the prompt:
   - Enter year (e.g., '2024', '2023')

### List Available Drivers
Get a list of all drivers for a specific year:
1. Run `python run_f1_analyzer.py`
2. Enter `list_drivers`
3. Follow the prompts:
   - Enter year (e.g., '2024', '2023')
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

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is open source and available under the MIT License. 