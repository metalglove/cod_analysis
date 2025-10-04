"""
Visualization utilities for Call of Duty game data analysis.

This module provides functions for creating various charts and plots
to visualize Call of Duty game performance data.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Set default style
plt.style.use('default')
sns.set_palette("husl")


class CODVisualizer:
    """Visualizer for Call of Duty game data."""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8), style: str = 'whitegrid'):
        """
        Initialize the visualizer.
        
        Args:
            figsize: Default figure size
            style: Seaborn style to use
        """
        self.figsize = figsize
        self.style = style
        sns.set_style(style)
        
        # Color palette for players
        self.player_colors = {
            'Mystyy': '#1f77b4',
            'Glovali': '#ff7f0e', 
            'Risky': '#2ca02c',
            'Anima': '#d62728'
        }
        
    def plot_performance_over_time(self, df: pd.DataFrame, metric: str, 
                                 game_name: Optional[str] = None,
                                 date_range: Optional[Tuple[str, str]] = None,
                                 show_trend: bool = True) -> plt.Figure:
        """
        Plot performance metric over time for all players.
        
        Args:
            df: Processed DataFrame
            metric: Metric to plot (e.g., 'KD_Ratio', 'SPM', 'Skill')
            game_name: Specific game to filter for
            date_range: Tuple of (start_date, end_date) strings
            show_trend: Whether to show trend lines
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Filter data
        plot_data = df.copy()
        if game_name:
            plot_data = plot_data[plot_data['Game Name'] == game_name]
        if date_range:
            plot_data = plot_data[
                (plot_data['UTC Timestamp'] >= date_range[0]) & 
                (plot_data['UTC Timestamp'] <= date_range[1])
            ]
            
        if plot_data.empty:
            ax.text(0.5, 0.5, 'No data available', transform=ax.transAxes, 
                   ha='center', va='center', fontsize=16)
            return fig
            
        # Plot each player
        for player in plot_data['Player'].unique():
            player_data = plot_data[plot_data['Player'] == player]
            if metric in player_data.columns and not player_data[metric].isna().all():
                color = self.player_colors.get(player, None)
                
                # Scatter plot
                ax.scatter(player_data['UTC Timestamp'], player_data[metric], 
                          label=player, alpha=0.6, color=color)
                
                # Trend line
                if show_trend and len(player_data) > 1:
                    ax.plot(player_data['UTC Timestamp'], player_data[metric], 
                           color=color, alpha=0.3, linewidth=1)
                    
        ax.set_xlabel('Date')
        ax.set_ylabel(metric.replace('_', ' ').title())
        ax.set_title(f'{metric.replace("_", " ").title()} Over Time' + 
                    (f' - {game_name}' if game_name else ''))
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
        
    def plot_player_comparison(self, df: pd.DataFrame, metrics: List[str],
                             game_name: Optional[str] = None) -> plt.Figure:
        """
        Create a radar chart comparing players across multiple metrics.
        
        Args:
            df: Processed DataFrame
            metrics: List of metrics to compare
            game_name: Specific game to filter for
            
        Returns:
            matplotlib Figure object
        """
        # Filter data
        plot_data = df.copy()
        if game_name:
            plot_data = plot_data[plot_data['Game Name'] == game_name]
            
        # Calculate mean values for each player
        player_stats = plot_data.groupby('Player')[metrics].mean()
        
        # Normalize to 0-100 scale for radar chart
        normalized_stats = player_stats.copy()
        for metric in metrics:
            if metric in normalized_stats.columns:
                min_val = normalized_stats[metric].min()
                max_val = normalized_stats[metric].max()
                if max_val != min_val:
                    normalized_stats[metric] = ((normalized_stats[metric] - min_val) / 
                                              (max_val - min_val)) * 100
                else:
                    normalized_stats[metric] = 50
                    
        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        fig, ax = plt.subplots(figsize=self.figsize, subplot_kw=dict(projection='polar'))
        
        for player in normalized_stats.index:
            values = normalized_stats.loc[player].tolist()
            values += values[:1]  # Complete the circle
            
            color = self.player_colors.get(player, None)
            ax.plot(angles, values, 'o-', linewidth=2, label=player, color=color)
            ax.fill(angles, values, alpha=0.25, color=color)
            
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics])
        ax.set_ylim(0, 100)
        ax.set_title(f'Player Comparison' + (f' - {game_name}' if game_name else ''))
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        return fig
        
    def plot_performance_distribution(self, df: pd.DataFrame, metric: str,
                                    group_by: str = 'Player') -> plt.Figure:
        """
        Plot distribution of performance metric using box plots and violin plots.
        
        Args:
            df: Processed DataFrame
            metric: Metric to plot
            group_by: Column to group by (e.g., 'Player', 'Game Name', 'Map')
            
        Returns:
            matplotlib Figure object
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Box plot
        sns.boxplot(data=df, x=group_by, y=metric, ax=ax1)
        ax1.set_title(f'{metric.replace("_", " ").title()} Distribution (Box Plot)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Violin plot
        sns.violinplot(data=df, x=group_by, y=metric, ax=ax2)
        ax2.set_title(f'{metric.replace("_", " ").title()} Distribution (Violin Plot)')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
        
    def plot_correlation_matrix(self, df: pd.DataFrame, 
                              metrics: Optional[List[str]] = None) -> plt.Figure:
        """
        Plot correlation matrix of performance metrics.
        
        Args:
            df: Processed DataFrame
            metrics: List of metrics to include (if None, uses numeric columns)
            
        Returns:
            matplotlib Figure object
        """
        if metrics is None:
            # Select numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # Remove some non-performance columns
            exclude_cols = ['Match ID', 'Win']
            metrics = [col for col in numeric_cols if col not in exclude_cols]
            
        correlation_data = df[metrics].corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        mask = np.triu(np.ones_like(correlation_data, dtype=bool))
        
        sns.heatmap(correlation_data, mask=mask, annot=True, cmap='coolwarm', 
                   center=0, ax=ax, fmt='.2f')
        ax.set_title('Performance Metrics Correlation Matrix')
        
        plt.tight_layout()
        return fig
        
    def plot_game_mode_performance(self, df: pd.DataFrame, metric: str = 'KD_Ratio') -> plt.Figure:
        """
        Compare performance across different game modes.
        
        Args:
            df: Processed DataFrame
            metric: Metric to compare
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Filter for common game modes
        common_modes = df['Game Type'].value_counts().head(6).index.tolist()
        mode_data = df[df['Game Type'].isin(common_modes)]
        
        sns.boxplot(data=mode_data, x='Game Type', y=metric, hue='Player', ax=ax)
        ax.set_title(f'{metric.replace("_", " ").title()} by Game Mode')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
        
    def plot_map_performance(self, df: pd.DataFrame, metric: str = 'KD_Ratio',
                           top_n: int = 10) -> plt.Figure:
        """
        Compare performance across different maps.
        
        Args:
            df: Processed DataFrame
            metric: Metric to compare
            top_n: Number of top maps to show
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # Get top N maps by frequency
        top_maps = df['Map'].value_counts().head(top_n).index.tolist()
        map_data = df[df['Map'].isin(top_maps)]
        
        sns.boxplot(data=map_data, x='Map', y=metric, hue='Player', ax=ax)
        ax.set_title(f'{metric.replace("_", " ").title()} by Map (Top {top_n})')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
        
    def plot_win_rate_analysis(self, df: pd.DataFrame) -> plt.Figure:
        """
        Analyze win rates across different dimensions.
        
        Args:
            df: Processed DataFrame with 'Win' column
            
        Returns:
            matplotlib Figure object
        """
        if 'Win' not in df.columns:
            # Create win column if it doesn't exist
            df['Win'] = (df['Match Outcome'].str.lower() == 'victory').astype(int)
            
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Win rate by player
        win_rate_player = df.groupby('Player')['Win'].mean() * 100
        win_rate_player.plot(kind='bar', ax=ax1, color=list(self.player_colors.values()))
        ax1.set_title('Win Rate by Player (%)')
        ax1.set_ylabel('Win Rate (%)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Win rate by game
        win_rate_game = df.groupby('Game Name')['Win'].mean() * 100
        win_rate_game.plot(kind='bar', ax=ax2)
        ax2.set_title('Win Rate by Game (%)')
        ax2.set_ylabel('Win Rate (%)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Win rate by game mode
        common_modes = df['Game Type'].value_counts().head(5).index
        mode_winrate = df[df['Game Type'].isin(common_modes)].groupby('Game Type')['Win'].mean() * 100
        mode_winrate.plot(kind='bar', ax=ax3)
        ax3.set_title('Win Rate by Game Mode (%)')
        ax3.set_ylabel('Win Rate (%)')
        ax3.tick_params(axis='x', rotation=45)
        
        # KD vs Win Rate scatter
        kd_winrate = df.groupby(['Player', 'Match ID']).agg({
            'KD_Ratio': 'mean',
            'Win': 'first'
        }).reset_index()
        
        for player in kd_winrate['Player'].unique():
            player_data = kd_winrate[kd_winrate['Player'] == player]
            color = self.player_colors.get(player, None)
            ax4.scatter(player_data['KD_Ratio'], player_data['Win'], 
                       label=player, alpha=0.6, color=color)
                       
        ax4.set_xlabel('K/D Ratio')
        ax4.set_ylabel('Win (1) / Loss (0)')
        ax4.set_title('K/D Ratio vs Match Outcome')
        ax4.legend()
        
        plt.tight_layout()
        return fig


def create_performance_dashboard(df: pd.DataFrame, player: str, 
                               game_name: Optional[str] = None) -> List[plt.Figure]:
    """
    Create a comprehensive performance dashboard for a specific player.
    
    Args:
        df: Processed DataFrame
        player: Player name
        game_name: Specific game to focus on
        
    Returns:
        List of matplotlib Figure objects
    """
    visualizer = CODVisualizer()
    
    # Filter data for player
    player_data = df[df['Player'] == player]
    if game_name:
        player_data = player_data[player_data['Game Name'] == game_name]
        
    if player_data.empty:
        logger.warning(f"No data found for player {player}")
        return []
        
    figures = []
    
    # Performance over time
    for metric in ['KD_Ratio', 'SPM', 'Skill', 'Accuracy']:
        if metric in player_data.columns:
            fig = visualizer.plot_performance_over_time(
                player_data, metric, game_name
            )
            figures.append(fig)
            
    return figures
