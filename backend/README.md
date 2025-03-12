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
- `available_races` - List available races for a given year
- `available_drivers` - List available drivers for a given year
- `help` - Show the help message
- `exit` - Exit the application

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
3. Follow the prompts to select driver, race, and session

Example output will show:
- Lap time progression throughout the race
- Sector time analysis
- Tire compound usage
- Key performance metrics

### Race Analysis
Analyze a complete race:
1. Run `python run_f1_analyzer.py`
2. Enter `race_analysis`
3. Follow the prompts to select year and Grand Prix

### Driver Comparison
Compare two drivers head-to-head:
1. Run `python run_f1_analyzer.py`
2. Enter `compare_drivers`
3. Follow the prompts to select two drivers, race, and session

## Visualization Output

All visualizations are saved to the `assets/visualizations/` directory with descriptive filenames.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is open source and available under the MIT License. 