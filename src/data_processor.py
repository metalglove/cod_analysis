"""
Data processing utilities for Call of Duty game data analysis.

This module provides functions for cleaning, transforming, and feature engineering
on Call of Duty game statistics data.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class CODDataProcessor:
    """Processor for Call of Duty game data cleaning and feature engineering."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.required_columns = [
            'Player', 'Match ID', 'Game Name', 'UTC Timestamp', 'Kills', 'Deaths',
            'Game Type', 'Match Start Timestamp', 'Match End Timestamp', 'Map',
            'Match Outcome', 'Skill', 'Score', 'Shots', 'Hits', 'Assists',
            'Longest Streak', 'Headshots', 'Damage Done', 'Match XP'
        ]
        
    def clean_and_process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and process the raw game data.
        
        Args:
            df: Raw DataFrame from parser
            
        Returns:
            Cleaned and processed DataFrame with additional features
        """
        if df.empty:
            logger.warning("Empty DataFrame provided to processor")
            return df
            
        logger.info(f"Processing {len(df)} records")
        
        # Select required columns (ignore missing ones)
        available_cols = [col for col in self.required_columns if col in df.columns]
        df_processed = df[available_cols].copy()
        
        # Convert data types
        df_processed = self._convert_data_types(df_processed)
        
        # Create derived features
        df_processed = self._create_features(df_processed)
        
        # Handle outliers
        df_processed = self._handle_outliers(df_processed)
        
        logger.info(f"Processing complete: {len(df_processed)} records")
        return df_processed
        
    def _convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to appropriate data types."""
        df = df.copy()
        
        # Timestamp conversions
        timestamp_cols = ['UTC Timestamp', 'Match Start Timestamp', 'Match End Timestamp']
        for col in timestamp_cols:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except Exception as e:
                    logger.warning(f"Error converting {col} to datetime: {e}")
                    
        # Numeric conversions
        numeric_conversions = {
            'Kills': 'int',
            'Deaths': 'int',
            'Score': 'int',
            'Assists': 'int',
            'Headshots': 'int',
            'Skill': 'float',
            'Shots': 'float',
            'Hits': 'float',
            'Damage Done': 'float'
        }
        
        for col, dtype in numeric_conversions.items():
            if col in df.columns:
                try:
                    if dtype == 'int':
                        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                    else:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    logger.warning(f"Error converting {col} to {dtype}: {e}")
                    
        # Special handling for Longest Streak and Match XP
        if 'Longest Streak' in df.columns:
            df['Longest Streak'] = df['Longest Streak'].notna().astype(int)
            
        if 'Match XP' in df.columns:
            df['Match XP'] = pd.to_numeric(df['Match XP'], errors='coerce')
            df['Match XP'] = df['Match XP'].where(df['Match XP'] > 0, np.nan)
            
        return df
        
    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create derived features from the base data."""
        df = df.copy()
        
        # K/D Ratio
        if 'Kills' in df.columns and 'Deaths' in df.columns:
            # Avoid division by zero
            df['KD_Ratio'] = df['Kills'] / df['Deaths'].replace(0, 1)
            
        # K+A/D Ratio (Kills + Assists / Deaths)
        if all(col in df.columns for col in ['Kills', 'Assists', 'Deaths']):
            df['KAD_Ratio'] = (df['Kills'] + df['Assists']) / df['Deaths'].replace(0, 1)
            
        # Accuracy percentage
        if 'Shots' in df.columns and 'Hits' in df.columns:
            df['Accuracy'] = (df['Hits'] / df['Shots'].replace(0, np.nan)) * 100
            
        # Headshot percentage
        if 'Headshots' in df.columns and 'Kills' in df.columns:
            df['Headshot_Percentage'] = (df['Headshots'] / df['Kills'].replace(0, np.nan)) * 100
            
        # Score Per Minute (SPM)
        if all(col in df.columns for col in ['Score', 'Match Start Timestamp', 'Match End Timestamp']):
            try:
                duration_seconds = (df['Match End Timestamp'] - df['Match Start Timestamp']).dt.total_seconds()
                duration_minutes = duration_seconds / 60
                df['SPM'] = df['Score'] / duration_minutes.replace(0, np.nan)
            except Exception as e:
                logger.warning(f"Error calculating SPM: {e}")
                
        # Kills Per Minute (KPM)
        if 'Kills' in df.columns and 'SPM' in df.columns:
            try:
                duration_seconds = (df['Match End Timestamp'] - df['Match Start Timestamp']).dt.total_seconds()
                duration_minutes = duration_seconds / 60
                df['KPM'] = df['Kills'] / duration_minutes.replace(0, np.nan)
            except Exception as e:
                logger.warning(f"Error calculating KPM: {e}")
                
        # Damage per kill
        if 'Damage Done' in df.columns and 'Kills' in df.columns:
            df['Damage_Per_Kill'] = df['Damage Done'] / df['Kills'].replace(0, np.nan)
            
        # Win rate (binary outcome)
        if 'Match Outcome' in df.columns:
            df['Win'] = (df['Match Outcome'].str.lower() == 'victory').astype(int)
            
        # Score efficiency (Score per shot)
        if 'Score' in df.columns and 'Shots' in df.columns:
            df['Score_Per_Shot'] = df['Score'] / df['Shots'].replace(0, np.nan)
            
        return df
        
    def _handle_outliers(self, df: pd.DataFrame, z_threshold: float = 3.0) -> pd.DataFrame:
        """
        Handle outliers using z-score method.
        
        Args:
            df: DataFrame to process
            z_threshold: Z-score threshold for outlier detection
            
        Returns:
            DataFrame with outliers handled
        """
        df = df.copy()
        
        # Columns to check for outliers
        outlier_columns = ['Kills', 'Deaths', 'Score', 'SPM', 'KD_Ratio', 'Accuracy', 'Damage Done']
        outlier_columns = [col for col in outlier_columns if col in df.columns]
        
        outliers_found = 0
        
        for col in outlier_columns:
            if df[col].dtype in ['int64', 'float64', 'Int64']:
                # Calculate z-scores
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = z_scores > z_threshold
                
                if outliers.sum() > 0:
                    outliers_found += outliers.sum()
                    logger.info(f"Found {outliers.sum()} outliers in {col}")
                    
                    # Option 1: Cap outliers at percentiles (more conservative)
                    q99 = df[col].quantile(0.99)
                    q01 = df[col].quantile(0.01)
                    df[col] = df[col].clip(lower=q01, upper=q99)
                    
        if outliers_found > 0:
            logger.info(f"Total outliers handled: {outliers_found}")
            
        return df
        
    def create_rolling_averages(self, df: pd.DataFrame, windows: List[int] = [5, 10, 20]) -> pd.DataFrame:
        """
        Create rolling averages for key performance metrics.
        
        Args:
            df: Processed DataFrame
            windows: List of window sizes for rolling averages
            
        Returns:
            DataFrame with rolling average columns added
        """
        df = df.copy()
        
        # Ensure data is sorted by timestamp for each player
        df = df.sort_values(['Player', 'UTC Timestamp'])
        
        # Metrics to calculate rolling averages for
        metrics = ['KD_Ratio', 'SPM', 'Accuracy', 'Score', 'Kills']
        metrics = [col for col in metrics if col in df.columns]
        
        for window in windows:
            for metric in metrics:
                col_name = f'{metric}_MA_{window}'
                df[col_name] = df.groupby('Player')[metric].transform(
                    lambda x: x.rolling(window=window, min_periods=1).mean()
                )
                
        return df
        
    def calculate_performance_trends(self, df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
        """
        Calculate performance trends over time.
        
        Args:
            df: Processed DataFrame
            window: Window size for trend calculation
            
        Returns:
            DataFrame with trend indicators
        """
        df = df.copy()
        df = df.sort_values(['Player', 'UTC Timestamp'])
        
        trend_metrics = ['KD_Ratio', 'SPM', 'Skill']
        trend_metrics = [col for col in trend_metrics if col in df.columns]
        
        for metric in trend_metrics:
            # Calculate the slope of the trend line over the window
            def calculate_trend(series):
                if len(series) < 2:
                    return 0
                x = np.arange(len(series))
                slope = np.polyfit(x, series, 1)[0]
                return slope
                
            trend_col = f'{metric}_Trend'
            df[trend_col] = df.groupby('Player')[metric].transform(
                lambda x: x.rolling(window=window).apply(calculate_trend, raw=False)
            )
            
        return df


def process_cod_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function for processing COD data.
    
    Args:
        df: Raw DataFrame from parser
        
    Returns:
        Fully processed DataFrame
    """
    processor = CODDataProcessor()
    return processor.clean_and_process(df)


def add_advanced_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add advanced features like rolling averages and trends.
    
    Args:
        df: Processed DataFrame
        
    Returns:
        DataFrame with advanced features
    """
    processor = CODDataProcessor()
    df = processor.create_rolling_averages(df)
    df = processor.calculate_performance_trends(df)
    return df
