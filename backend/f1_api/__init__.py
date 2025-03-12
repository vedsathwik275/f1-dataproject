"""
F1 API Package

This package provides interfaces for interacting with Formula 1 data APIs,
including FastF1 and OpenF1, as well as tools for processing and visualizing
the data.
"""

__version__ = '0.1.0'

# Import key modules for easier access
from .fastf1_client import FastF1Client
from .openf1_client import OpenF1Client
from .data_processor import process_data
from .visualizations import create_visualization
from .historical_data import HistoricalDataManager, HISTORICAL_SEASONS 