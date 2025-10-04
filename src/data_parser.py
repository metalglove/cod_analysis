"""
Data parsing utilities for Call of Duty game data analysis.

This module provides functions to parse HTML files containing 
Call of Duty game statistics and convert them to pandas DataFrames.
"""

import pandas as pd
from bs4 import BeautifulSoup
import logging
from typing import List, Optional, Dict, Any
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CODDataParser:
    """Parser for Call of Duty HTML game data files."""
    
    def __init__(self, supported_games: Optional[List[str]] = None):
        """
        Initialize the parser with supported games.
        
        Args:
            supported_games: List of supported game names. If None, uses default list.
        """
        self.supported_games = supported_games or [
            " Call of Duty: Black Ops 6", 
            " Call of Duty: Black Ops Cold War", 
            " Call of Duty: Modern Warfare",
            " Call of Duty: Modern Warfare II", 
            " Call of Duty: Modern Warfare III", 
            " Call of Duty: Vanguard"
        ]
        
    def parse_single_file(self, filename: str, player_name: Optional[str] = None) -> pd.DataFrame:
        """
        Parse a single HTML file containing game data.
        
        Args:
            filename: Path to the HTML file
            player_name: Name of the player (optional, can be added later)
            
        Returns:
            DataFrame containing parsed game data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If no valid data is found in the file
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
            
        logger.info(f"Parsing file: {filename}")
        
        try:
            with open(filename, "r", encoding="utf8") as file:
                html_content = file.read()
        except Exception as e:
            logger.error(f"Error reading file {filename}: {e}")
            raise
            
        soup = BeautifulSoup(html_content, "html.parser")
        df = pd.DataFrame()
        games_processed = []
        
        tables = soup.find_all('table')
        logger.info(f"Found {len(tables)} tables in {filename}")
        
        for table in tables:
            try:
                game_data = self._parse_table(table, games_processed)
                if game_data is not None:
                    df = pd.concat([df, game_data], ignore_index=True)
            except Exception as e:
                logger.warning(f"Error parsing table: {e}")
                continue
                
        if df.empty:
            logger.warning(f"No valid game data found in {filename}")
            return pd.DataFrame()
            
        if player_name:
            df['Player'] = player_name
            
        logger.info(f"Successfully parsed {len(df)} records from {filename}")
        return df
        
    def _parse_table(self, table, games_processed: List[str]) -> Optional[pd.DataFrame]:
        """
        Parse a single table element.
        
        Args:
            table: BeautifulSoup table element
            games_processed: List of already processed games
            
        Returns:
            DataFrame with table data or None if not a valid game table
        """
        # Check if this is a multiplayer match data table
        previous_h2 = table.find_previous('h2')
        if not (previous_h2 and previous_h2.get_text() == 'Multiplayer Match Data (reverse chronological)'):
            return None
            
        # Get the game name
        previous_h1 = table.find_previous('h1')
        if not previous_h1:
            return None
            
        game_name = previous_h1.get_text()
        
        if game_name not in self.supported_games or game_name in games_processed:
            return None
            
        logger.info(f"Processing game: {game_name}")
        
        # Extract headers
        headers = [header.get_text().strip() for header in table.find_all('th')]
        if not headers:
            logger.warning(f"No headers found for {game_name}")
            return None
            
        # Extract rows
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = [col.get_text().strip() for col in row.find_all('td')]
            if cols:  # Only add non-empty rows
                rows.append(cols)
                
        if not rows:
            logger.warning(f"No data rows found for {game_name}")
            return None
            
        logger.info(f"Found {len(rows)} matches for {game_name}")
        
        # Create DataFrame
        try:
            data = pd.DataFrame(columns=headers, data=rows)
            data['Game Name'] = game_name
            games_processed.append(game_name)
            return data
        except Exception as e:
            logger.error(f"Error creating DataFrame for {game_name}: {e}")
            return None
            
    def parse_multiple_files(self, file_player_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Parse multiple HTML files and combine them into a single DataFrame.
        
        Args:
            file_player_mapping: Dictionary mapping file paths to player names
            
        Returns:
            Combined DataFrame with all parsed data
        """
        all_data = []
        
        for filename, player_name in file_player_mapping.items():
            try:
                df = self.parse_single_file(filename, player_name)
                if not df.empty:
                    all_data.append(df)
            except Exception as e:
                logger.error(f"Failed to parse {filename}: {e}")
                continue
                
        if not all_data:
            logger.warning("No valid data found in any files")
            return pd.DataFrame()
            
        # Combine all DataFrames
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Remove duplicates based on timestamp and player
        original_size = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['UTC Timestamp', 'Player'], keep='first')
        final_size = len(combined_df)
        
        if original_size != final_size:
            logger.info(f"Removed {original_size - final_size} duplicate records")
            
        # Sort by timestamp
        if 'UTC Timestamp' in combined_df.columns:
            combined_df = combined_df.sort_values('UTC Timestamp')
            
        logger.info(f"Successfully combined data: {final_size} total records")
        return combined_df
        

def parse_games(filename: str) -> pd.DataFrame:
    """
    Legacy function for backward compatibility.
    
    Args:
        filename: Path to HTML file
        
    Returns:
        DataFrame with parsed game data
    """
    parser = CODDataParser()
    return parser.parse_single_file(filename)


def load_player_data(data_files: Dict[str, str]) -> pd.DataFrame:
    """
    Convenience function to load and combine player data files.
    
    Args:
        data_files: Dictionary mapping file paths to player names
        
    Returns:
        Combined and cleaned DataFrame
    """
    parser = CODDataParser()
    return parser.parse_multiple_files(data_files)
