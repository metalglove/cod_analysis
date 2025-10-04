# Call of Duty Performance Analysis

A Python toolkit for analyzing Call of Duty gameplay performance with statistical analysis and visualizations.

## Features

### Analytics
- Statistical analysis including hypothesis testing and correlation analysis
- Performance metrics like K/D ratios, skill ratings, win rates, and custom metrics
- Trend analysis showing performance evolution over time
- Anomaly detection to identify unusual performances
- Player ranking system with weighted scoring

### Visualizations
- Interactive charts with Plotly
- Radar charts for multi-player comparisons
- Correlation matrix heatmaps
- Time series plots with moving averages
- Distribution plots and box plots

### Architecture
- Modular design with separate components for parsing, processing, visualization, and statistics
- HTML parsing for Activision account exports
- Data cleaning and feature engineering
- Customizable chart themes and statistical parameters

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd cod_analysis
   ```

2. Set up the environment:
   ```bash
   ./setup_env.sh
   ```

3. Activate the environment:
   ```bash
   source cod_analysis_env/bin/activate
   ```

4. Start the analysis:
   ```bash
   jupyter lab notebooks/enhanced_analysis.ipynb
   ```

## Project Structure

```
cod_analysis/
├── notebooks/                    # Jupyter notebooks
│   ├── analysis.ipynb           # Original analysis notebook
│   └── enhanced_analysis.ipynb  # Enhanced analysis with advanced features
├── src/                         # Source code modules
│   ├── __init__.py             # Package initialization
│   ├── data_parser.py          # HTML parsing and data extraction
│   ├── data_processor.py       # Data cleaning and feature engineering
│   ├── visualization.py        # Advanced plotting and charts
│   ├── cod_statistics.py       # Statistical analysis and testing
│   ├── config.py               # Configuration and constants
│   └── extract_data.py         # Data extraction utilities
├── data/                        # Raw HTML data files
├── output/                      # Generated outputs
│   ├── charts/                 # Saved visualizations
│   ├── reports/                # Analysis reports
│   └── data/                   # Processed datasets
├── cod_analysis_env/           # Virtual environment
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── setup_env.sh               # Environment setup script
└── README.md                  # This file
```

## Supported Games

- Call of Duty: Black Ops 6
- Call of Duty: Black Ops Cold War
- Call of Duty: Modern Warfare
- Call of Duty: Modern Warfare II
- Call of Duty: Modern Warfare III
- Call of Duty: Vanguard

## Getting Your Data

### Option 1: Using Real Data
1. Export your match history from Activision account as HTML files
2. Place HTML files in the `data/` directory
3. Run the enhanced analysis notebook

### Option 2: Extract from Existing Analysis
If you already have a working analysis notebook:

1. Add extraction code to your original notebook:
   ```python
   # Add this cell to your original analysis after data processing
   def extract_and_export_data():
       # Check if processed data exists
       if 'dfa' not in globals():
           print("Processed data not found. Run data processing cells first.")
           return
       
       # Export the data
       output_file = 'extracted_cod_data.csv'
       dfa.to_csv(output_file, index=False)
       print(f"Data exported to: {output_file}")
       return output_file
   
   extract_and_export_data()
   ```

2. Copy the exported CSV to your notebooks directory

3. Run the enhanced analysis - it will automatically detect your real data

## Usage Examples

### Basic Analysis
```python
# Add path to modules
import sys
import os
sys.path.append('../src')

from data_parser import load_player_data
from data_processor import process_cod_data
from visualization import CODVisualizer

# Load and process data
file_mapping = {"../data/player.html": "PlayerName"}
raw_data = load_player_data(file_mapping)
processed_data = process_cod_data(raw_data)

# Create visualizations
visualizer = CODVisualizer()
fig = visualizer.plot_performance_over_time(processed_data, 'KD_Ratio')
```

### Statistical Analysis
```python
from cod_statistics import CODStatisticalAnalyzer

analyzer = CODStatisticalAnalyzer()
comparison = analyzer.compare_players_performance(processed_data, 'KD_Ratio')
trends = analyzer.analyze_performance_trends(processed_data, 'Player1', 'SPM')
```

## Performance Metrics

### Core Metrics
- K/D Ratio: Kills per death
- SPM: Score per minute  
- Accuracy: Hit percentage
- Skill: Game-provided skill rating
- KPM: Kills per minute
- Win Rate: Match victory percentage

### Advanced Metrics
- K+A/D Ratio: (Kills + Assists) per death
- Headshot %: Percentage of kills that are headshots
- Damage per Kill: Average damage dealt per elimination
- Score per Shot: Efficiency metric
- Rolling Averages: Smoothed performance trends
- Percentile Rankings: Relative performance positioning

## Development

### Code Quality
The project includes development tools:

```bash
# Activate environment
source cod_analysis_env/bin/activate

# Format code
black src/*.py

# Check style
flake8 src/*.py

# Type checking
mypy src/*.py

# Run tests
pytest
```

### Adding New Features

1. New Metrics: Add to `CORE_METRICS` in `src/config.py` and implement in `src/data_processor.py`
2. New Visualizations: Add methods to `CODVisualizer` class in `src/visualization.py`
3. New Games: Add to `SUPPORTED_GAMES` in `src/config.py`
4. New Statistics: Add methods to `CODStatisticalAnalyzer` class in `src/cod_statistics.py`

## Configuration

Key settings in `src/config.py`:

- Players and Colors: Customize player names and visualization colors
- Games and Maps: Add new games or map lists  
- Statistical Thresholds: Adjust significance levels and effect sizes
- Visualization Settings: Modify chart styles and sizes

## Analysis Features

### Statistical Analysis
- Hypothesis testing for player comparisons
- Correlation analysis between metrics
- Effect size calculations (Cohen's d)
- Confidence intervals and significance testing
- Trend analysis with seasonal decomposition

### Visualization Suite
- Interactive time series plots
- Multi-player radar chart comparisons
- Performance correlation heatmaps
- Distribution analysis (box plots, histograms)
- Anomaly detection visualizations

### Performance Insights
- Player ranking across multiple metrics
- Game mode performance comparison
- Map-specific performance analysis
- Weapon and playstyle insights
- Performance trend identification

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes in the appropriate `src/` module
4. Update notebooks if needed
5. Run tests and quality checks
6. Submit a pull request

## License

This project is for educational and personal use. Respect Activision's terms of service when obtaining data.

## Troubleshooting

### Common Issues

1. Import Errors: 
   - Ensure virtual environment is activated
   - Check that `sys.path.append('../src')` is included in notebooks

2. Module Not Found: 
   - Verify you're running notebooks from the `notebooks/` directory
   - Check that `src/` directory contains all Python modules

3. Data Loading Issues:
   - Ensure data files are in the correct format
   - Check file paths in configuration

4. Visualization Issues: 
   - Install appropriate backends for matplotlib
   - Ensure all visualization dependencies are installed

### Getting Help

1. Check the enhanced analysis notebook for detailed examples
2. Review error messages and logs carefully
3. Ensure data files are in the expected format
4. Verify all dependencies are installed correctly
