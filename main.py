"""
main.py - Entry point for the Library Management System
Simply launches the GUI application.
"""

import os
import sys

# Ensure the working directory is the project root
# so that data files are created in the right place.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import launch

if __name__ == "__main__":
    launch()
