#!/usr/bin/env python3
"""
Run F1 Analyzer Application

This script runs the F1 Data Analyzer application.
"""

import sys
from f1_analyzer import F1Analyzer

def main():
    """Run the F1 Analyzer application."""
    print("Starting F1 Data Analyzer...")
    analyzer = F1Analyzer()
    analyzer.run()

if __name__ == "__main__":
    main() 