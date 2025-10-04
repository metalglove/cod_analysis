"""
COD Analysis Package

A comprehensive Call of Duty performance analysis toolkit with advanced statistics,
visualizations, and data processing capabilities.

Modules:
    - data_parser: HTML parsing and data extraction
    - data_processor: Data cleaning and feature engineering
    - visualization: Advanced plotting and charts
    - cod_statistics: Statistical analysis and hypothesis testing
    - config: Configuration settings and constants
"""

__version__ = "1.0.0"
__author__ = "COD Analysis Team"

# Import main classes for easy access
from .data_parser import CODDataParser
from .data_processor import CODDataProcessor
from .visualization import CODVisualizer
from .cod_statistics import CODStatisticalAnalyzer

__all__ = [
    'CODDataParser',
    'CODDataProcessor', 
    'CODVisualizer',
    'CODStatisticalAnalyzer'
]
