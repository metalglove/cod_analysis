"""
Configuration constants and settings for Call of Duty game data analysis.

This module contains all the constants, game lists, map names, and default
settings used throughout the COD analysis project.
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime

# =============================================================================
# GAME CONFIGURATIONS
# =============================================================================

# Supported Call of Duty games
SUPPORTED_GAMES = [
    " Call of Duty: Black Ops 6",
    " Call of Duty: Black Ops Cold War", 
    " Call of Duty: Modern Warfare",
    " Call of Duty: Modern Warfare II",
    " Call of Duty: Modern Warfare III",
    " Call of Duty: Vanguard"
]

# Game abbreviations for cleaner displays
GAME_ABBREVIATIONS = {
    " Call of Duty: Black Ops 6": "BO6",
    " Call of Duty: Black Ops Cold War": "BOCW",
    " Call of Duty: Modern Warfare": "MW",
    " Call of Duty: Modern Warfare II": "MW2",
    " Call of Duty: Modern Warfare III": "MW3",
    " Call of Duty: Vanguard": "Vanguard"
}

# Game release dates (for temporal analysis)
GAME_RELEASE_DATES = {
    " Call of Duty: Black Ops 6": datetime(2024, 10, 25),
    " Call of Duty: Black Ops Cold War": datetime(2020, 11, 13),
    " Call of Duty: Modern Warfare": datetime(2019, 10, 25),
    " Call of Duty: Modern Warfare II": datetime(2022, 10, 28),
    " Call of Duty: Modern Warfare III": datetime(2023, 11, 10),
    " Call of Duty: Vanguard": datetime(2021, 11, 5)
}

# =============================================================================
# PLAYER CONFIGURATIONS
# =============================================================================

# Default players in the analysis
DEFAULT_PLAYERS = ["Mystyy", "Glovali", "Risky", "Anima"]

# Player display colors for visualizations
PLAYER_COLORS = {
    "Mystyy": "#1f77b4",    # Blue
    "Glovali": "#ff7f0e",   # Orange
    "Risky": "#2ca02c",     # Green
    "Anima": "#d62728"      # Red
}

# Player aliases (in case of name variations)
PLAYER_ALIASES = {
    "Mystyy": ["Mystyy", "mystyy"],
    "Glovali": ["Glovali", "glovali", "Gloval"],
    "Risky": ["Risky", "risky"],
    "Anima": ["Anima", "anima"]
}

# =============================================================================
# MAP CONFIGURATIONS
# =============================================================================

# Black Ops 6 Maps
BO6_MAPS = [
    "Babylon", "Derelict", "Extraction", "Hideout", "Lowtown", 
    "Nuketown", "Payback", "Protocol", "Red Card", "Rewind", 
    "SCUD", "Skyline", "Subsonic", "Vault", "Vorkuta"
]

# Modern Warfare III Maps
MW3_MAPS = [
    "16-Bit", "Abandoned", "Highrise", "Karachi", "Estate",
    "Favela", "Invasion", "Quarry", "Rundown", "Scrapyard",
    "Skidrow", "Sub Base", "Terminal", "Underpass", "Wasteland"
]

# Modern Warfare II Maps  
MW2_MAPS = [
    "Al Bagra Fortress", "Ashika Island", "Breenbergh Hotel",
    "Crown Raceway", "Embassy", "Farm 18", "Himmelbjerget",
    "Mercado Las Almas", "Museum", "Santa Seña Border Crossing",
    "Shoot House", "Taraq", "Valderas Museum", "Zarqwa Hydroelectric"
]

# Combined map list for general analysis
ALL_MAPS = {
    " Call of Duty: Black Ops 6": BO6_MAPS,
    " Call of Duty: Modern Warfare III": MW3_MAPS,
    " Call of Duty: Modern Warfare II": MW2_MAPS,
}

# =============================================================================
# GAME MODE CONFIGURATIONS
# =============================================================================

# Core game modes
CORE_GAME_MODES = [
    "Team Deathmatch", "Domination", "Hardpoint", "Search and Destroy",
    "Kill Confirmed", "Control", "Headquarters"
]

# Objective-based game modes
OBJECTIVE_MODES = [
    "Domination", "Hardpoint", "Control", "Headquarters", "Demolition"
]

# Elimination-based game modes
ELIMINATION_MODES = [
    "Team Deathmatch", "Kill Confirmed", "Free-for-All"
]

# Tactical game modes
TACTICAL_MODES = [
    "Search and Destroy", "Cyber Attack", "Gunfight"
]

# =============================================================================
# PERFORMANCE METRICS CONFIGURATIONS
# =============================================================================

# Core performance metrics
CORE_METRICS = [
    "Kills", "Deaths", "KD_Ratio", "Score", "SPM", "Accuracy", 
    "Skill", "Assists", "Headshots", "Damage Done"
]

# Advanced calculated metrics
ADVANCED_METRICS = [
    "KAD_Ratio", "Headshot_Percentage", "KPM", "Damage_Per_Kill",
    "Score_Per_Shot", "Win_Rate"
]

# Metrics that are "higher is better"
HIGHER_IS_BETTER = [
    "Kills", "KD_Ratio", "KAD_Ratio", "Score", "SPM", "Accuracy",
    "Skill", "Assists", "Headshots", "Headshot_Percentage", 
    "KPM", "Win_Rate", "Score_Per_Shot"
]

# Metrics that are "lower is better"
LOWER_IS_BETTER = [
    "Deaths", "Damage_Per_Kill"
]

# Metric display names (for prettier charts)
METRIC_DISPLAY_NAMES = {
    "KD_Ratio": "K/D Ratio",
    "KAD_Ratio": "K+A/D Ratio", 
    "SPM": "Score Per Minute",
    "KPM": "Kills Per Minute",
    "Headshot_Percentage": "Headshot %",
    "Damage_Per_Kill": "Damage Per Kill",
    "Score_Per_Shot": "Score Per Shot",
    "Win_Rate": "Win Rate %"
}

# =============================================================================
# ANALYSIS CONFIGURATIONS
# =============================================================================

# Default date ranges for analysis
ANALYSIS_DATE_RANGES = {
    "last_week": 7,
    "last_month": 30,
    "last_quarter": 90,
    "last_year": 365
}

# Statistical significance level
SIGNIFICANCE_LEVEL = 0.05

# Effect size thresholds (Cohen's d)
EFFECT_SIZE_THRESHOLDS = {
    "small": 0.2,
    "medium": 0.5, 
    "large": 0.8
}

# Correlation strength thresholds
CORRELATION_THRESHOLDS = {
    "very_weak": 0.2,
    "weak": 0.4,
    "moderate": 0.6,
    "strong": 0.8
}

# Outlier detection thresholds
OUTLIER_Z_THRESHOLD = 3.0
OUTLIER_IQR_MULTIPLIER = 1.5

# =============================================================================
# VISUALIZATION CONFIGURATIONS  
# =============================================================================

# Default figure sizes
FIGURE_SIZES = {
    "small": (8, 6),
    "medium": (12, 8),
    "large": (16, 10),
    "wide": (20, 8),
    "dashboard": (16, 12)
}

# Color palettes
COLOR_PALETTES = {
    "default": "husl",
    "performance": "RdYlGn",
    "heatmap": "coolwarm",
    "categorical": "Set2"
}

# Chart style settings
CHART_STYLE = {
    "style": "whitegrid",
    "font_scale": 1.1,
    "rc": {
        "figure.figsize": FIGURE_SIZES["medium"],
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 11
    }
}

# =============================================================================
# DATA PROCESSING CONFIGURATIONS
# =============================================================================

# Required columns for processing
REQUIRED_COLUMNS = [
    "Player", "Match ID", "Game Name", "UTC Timestamp", "Kills", "Deaths",
    "Game Type", "Match Start Timestamp", "Match End Timestamp", "Map",
    "Match Outcome", "Skill", "Score", "Shots", "Hits", "Assists",
    "Longest Streak", "Headshots", "Damage Done", "Match XP"
]

# Columns that should be numeric
NUMERIC_COLUMNS = {
    "Kills": "int",
    "Deaths": "int", 
    "Score": "int",
    "Assists": "int",
    "Headshots": "int",
    "Skill": "float",
    "Shots": "float", 
    "Hits": "float",
    "Damage Done": "float",
    "Match XP": "float"
}

# Columns that should be datetime
DATETIME_COLUMNS = [
    "UTC Timestamp", "Match Start Timestamp", "Match End Timestamp"
]

# =============================================================================
# FILE PATHS AND DATA SOURCES
# =============================================================================

# Default data directory
DATA_DIRECTORY = "data"

# Expected HTML file patterns
HTML_FILE_PATTERNS = [
    "*-ACTIVISION_ACCOUNT.html",
    "*_ACTIVISION_ACCOUNT.html"
]

# Output directories
OUTPUT_DIRECTORIES = {
    "charts": "output/charts",
    "reports": "output/reports", 
    "data": "output/processed_data"
}

# =============================================================================
# SPECIAL EVENT CONFIGURATIONS
# =============================================================================

# Special events or patches that might affect performance
SPECIAL_EVENTS = {
    " Call of Duty: Black Ops 6": {
        "2box_patch": {
            "date": datetime(2024, 12, 4, 19, 0),
            "description": "2box patch release",
            "color": "red"
        },
        "skin_purchase": {
            "date": datetime(2024, 12, 23, 20, 30),
            "description": "Bought skin",
            "color": "green"
        }
    }
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_game_maps(game_name: str) -> List[str]:
    """Get maps for a specific game."""
    return ALL_MAPS.get(game_name, [])

def get_player_color(player_name: str) -> str:
    """Get color for a specific player."""
    return PLAYER_COLORS.get(player_name, "#000000")

def get_metric_display_name(metric: str) -> str:
    """Get display name for a metric."""
    return METRIC_DISPLAY_NAMES.get(metric, metric.replace("_", " ").title())

def is_higher_better(metric: str) -> bool:
    """Check if higher values are better for a metric."""
    return metric in HIGHER_IS_BETTER

def get_default_file_mapping() -> Dict[str, str]:
    """Get default file to player mapping.""" 
    return {
        "data/33833496-ACTIVISION_ACCOUNT.html": "Glovali",
        "data/33815277-ACTIVISION_ACCOUNT.html": "Mystyy", 
        "data/33810648-ACTIVISION_ACCOUNT.html": "Risky",
        "data/33757681-ACTIVISION_ACCOUNT.html": "Anima"
    }
