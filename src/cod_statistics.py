"""
Statistical analysis utilities for Call of Duty game data analysis.

This module provides functions for statistical testing, correlation analysis,
and performance comparison on Call of Duty game statistics data.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
import logging
from scipy import stats
from scipy.stats import ttest_ind, mannwhitneyu, kruskal, pearsonr, spearmanr
import warnings

logger = logging.getLogger(__name__)


class CODStatisticalAnalyzer:
    """Statistical analyzer for Call of Duty game data."""
    
    def __init__(self, confidence_level: float = 0.95):
        """
        Initialize the statistical analyzer.
        
        Args:
            confidence_level: Confidence level for statistical tests
        """
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level
        
    def compare_players_performance(self, df: pd.DataFrame, metric: str,
                                  players: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Compare performance metric between players using statistical tests.
        
        Args:
            df: Processed DataFrame
            metric: Metric to compare
            players: List of players to compare (if None, uses all)
            
        Returns:
            Dictionary with test results
        """
        if players is None:
            players = df['Player'].unique().tolist()
            
        if len(players) < 2:
            return {"error": "Need at least 2 players for comparison"}
            
        results = {
            "metric": metric,
            "players": players,
            "sample_sizes": {},
            "means": {},
            "stds": {},
            "tests": {}
        }
        
        # Calculate descriptive statistics
        for player in players:
            player_data = df[df['Player'] == player][metric].dropna()
            results["sample_sizes"][player] = len(player_data)
            results["means"][player] = player_data.mean()
            results["stds"][player] = player_data.std()
            
        # Perform pairwise t-tests
        for i, player1 in enumerate(players):
            for player2 in players[i+1:]:
                data1 = df[df['Player'] == player1][metric].dropna()
                data2 = df[df['Player'] == player2][metric].dropna()
                
                if len(data1) > 1 and len(data2) > 1:
                    # Check for normality (Shapiro-Wilk test)
                    try:
                        _, p1 = stats.shapiro(data1.sample(min(5000, len(data1))))
                        _, p2 = stats.shapiro(data2.sample(min(5000, len(data2))))
                        normal_dist = p1 > 0.05 and p2 > 0.05
                    except:
                        normal_dist = False
                        
                    # Choose appropriate test
                    if normal_dist:
                        stat, p_value = ttest_ind(data1, data2)
                        test_type = "t-test"
                    else:
                        stat, p_value = mannwhitneyu(data1, data2, alternative='two-sided')
                        test_type = "Mann-Whitney U"
                        
                    results["tests"][f"{player1}_vs_{player2}"] = {
                        "test_type": test_type,
                        "statistic": stat,
                        "p_value": p_value,
                        "significant": p_value < self.alpha,
                        "effect_size": self._calculate_effect_size(data1, data2)
                    }
                    
        return results
        
    def _calculate_effect_size(self, data1: pd.Series, data2: pd.Series) -> float:
        """Calculate Cohen's d effect size."""
        n1, n2 = len(data1), len(data2)
        pooled_std = np.sqrt(((n1 - 1) * data1.std()**2 + (n2 - 1) * data2.std()**2) / (n1 + n2 - 2))
        return (data1.mean() - data2.mean()) / pooled_std
        
    def analyze_game_impact(self, df: pd.DataFrame, metric: str) -> Dict[str, Any]:
        """
        Analyze if different games have significant impact on performance.
        
        Args:
            df: Processed DataFrame
            metric: Metric to analyze
            
        Returns:
            Dictionary with analysis results
        """
        games = df['Game Name'].unique()
        if len(games) < 2:
            return {"error": "Need at least 2 games for comparison"}
            
        # Prepare data for ANOVA
        groups = []
        for game in games:
            game_data = df[df['Game Name'] == game][metric].dropna()
            if len(game_data) > 0:
                groups.append(game_data)
                
        if len(groups) < 2:
            return {"error": "Not enough data for analysis"}
            
        # Perform Kruskal-Wallis test (non-parametric ANOVA)
        statistic, p_value = kruskal(*groups)
        
        results = {
            "metric": metric,
            "games": games.tolist(),
            "kruskal_wallis": {
                "statistic": statistic,
                "p_value": p_value,
                "significant": p_value < self.alpha
            },
            "game_stats": {}
        }
        
        # Calculate stats for each game
        for game in games:
            game_data = df[df['Game Name'] == game][metric].dropna()
            if len(game_data) > 0:
                results["game_stats"][game] = {
                    "mean": game_data.mean(),
                    "std": game_data.std(),
                    "count": len(game_data),
                    "median": game_data.median()
                }
                
        return results
        
    def calculate_correlation_analysis(self, df: pd.DataFrame, 
                                     metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Calculate correlations between performance metrics.
        
        Args:
            df: Processed DataFrame
            metrics: List of metrics to analyze
            
        Returns:
            Dictionary with correlation results
        """
        if metrics is None:
            # Select numeric performance columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            exclude_cols = ['Match ID', 'Win']
            metrics = [col for col in numeric_cols if col not in exclude_cols]
            
        correlation_data = df[metrics].dropna()
        
        if correlation_data.empty:
            return {"error": "No valid data for correlation analysis"}
            
        # Pearson correlation
        pearson_corr = correlation_data.corr(method='pearson')
        
        # Spearman correlation (rank-based, more robust)
        spearman_corr = correlation_data.corr(method='spearman')
        
        # Find strongest correlations
        strong_correlations = []
        for i, col1 in enumerate(metrics):
            for col2 in metrics[i+1:]:
                if col1 in pearson_corr.columns and col2 in pearson_corr.columns:
                    pearson_r = pearson_corr.loc[col1, col2]
                    spearman_r = spearman_corr.loc[col1, col2]
                    
                    if abs(pearson_r) > 0.5:  # Strong correlation threshold
                        strong_correlations.append({
                            "variables": f"{col1} - {col2}",
                            "pearson_r": pearson_r,
                            "spearman_r": spearman_r,
                            "strength": self._correlation_strength(abs(pearson_r))
                        })
                        
        return {
            "pearson_correlation_matrix": pearson_corr.to_dict(),
            "spearman_correlation_matrix": spearman_corr.to_dict(),
            "strong_correlations": strong_correlations,
            "metrics_analyzed": metrics
        }
        
    def _correlation_strength(self, r: float) -> str:
        """Classify correlation strength."""
        if r >= 0.8:
            return "Very Strong"
        elif r >= 0.6:
            return "Strong"
        elif r >= 0.4:
            return "Moderate"
        elif r >= 0.2:
            return "Weak"
        else:
            return "Very Weak"
            
    def analyze_performance_trends(self, df: pd.DataFrame, player: str, 
                                 metric: str, window: int = 10) -> Dict[str, Any]:
        """
        Analyze performance trends for a specific player.
        
        Args:
            df: Processed DataFrame
            player: Player name
            metric: Metric to analyze
            window: Window size for trend analysis
            
        Returns:
            Dictionary with trend analysis results
        """
        player_data = df[df['Player'] == player].sort_values('UTC Timestamp')
        
        if len(player_data) < window:
            return {"error": f"Need at least {window} data points for trend analysis"}
            
        metric_data = player_data[metric].dropna()
        if len(metric_data) < window:
            return {"error": f"Not enough valid {metric} data for trend analysis"}
            
        # Calculate rolling statistics
        rolling_mean = metric_data.rolling(window=window).mean()
        rolling_std = metric_data.rolling(window=window).std()
        
        # Linear trend analysis
        x = np.arange(len(metric_data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, metric_data)
        
        # Detect improvement/decline periods
        improvement_periods = []
        decline_periods = []
        
        for i in range(window, len(rolling_mean)):
            if i >= window * 2:  # Need enough data for comparison
                recent_mean = rolling_mean.iloc[i-window:i].mean()
                earlier_mean = rolling_mean.iloc[i-window*2:i-window].mean()
                
                if recent_mean > earlier_mean * 1.1:  # 10% improvement
                    improvement_periods.append(i)
                elif recent_mean < earlier_mean * 0.9:  # 10% decline
                    decline_periods.append(i)
                    
        return {
            "player": player,
            "metric": metric,
            "trend_analysis": {
                "slope": slope,
                "r_squared": r_value**2,
                "p_value": p_value,
                "trend_direction": "improving" if slope > 0 else "declining",
                "trend_strength": self._correlation_strength(abs(r_value))
            },
            "statistics": {
                "overall_mean": metric_data.mean(),
                "overall_std": metric_data.std(),
                "recent_mean": metric_data.tail(window).mean(),
                "recent_std": metric_data.tail(window).std(),
                "best_performance": metric_data.max(),
                "worst_performance": metric_data.min()
            },
            "periods": {
                "improvement_periods": len(improvement_periods),
                "decline_periods": len(decline_periods)
            }
        }
        
    def calculate_player_rankings(self, df: pd.DataFrame, 
                                metrics: List[str]) -> pd.DataFrame:
        """
        Calculate comprehensive player rankings across multiple metrics.
        
        Args:
            df: Processed DataFrame
            metrics: List of metrics to include in ranking
            
        Returns:
            DataFrame with player rankings
        """
        player_stats = df.groupby('Player')[metrics].agg(['mean', 'std', 'count'])
        
        rankings = pd.DataFrame(index=player_stats.index)
        
        for metric in metrics:
            if (metric, 'mean') in player_stats.columns:
                # Rank players by mean performance (higher is better for most metrics)
                metric_means = player_stats[(metric, 'mean')]
                rankings[f'{metric}_rank'] = metric_means.rank(ascending=False)
                rankings[f'{metric}_mean'] = metric_means
                rankings[f'{metric}_std'] = player_stats[(metric, 'std')]
                
        # Calculate overall ranking (average of individual ranks)
        rank_columns = [col for col in rankings.columns if col.endswith('_rank')]
        rankings['overall_rank'] = rankings[rank_columns].mean(axis=1)
        rankings['overall_rank_position'] = rankings['overall_rank'].rank()
        
        return rankings.sort_values('overall_rank')
        
    def detect_performance_anomalies(self, df: pd.DataFrame, player: str,
                                   metric: str, threshold: float = 2.0) -> Dict[str, Any]:
        """
        Detect anomalous performances using z-score analysis.
        
        Args:
            df: Processed DataFrame
            player: Player name
            metric: Metric to analyze
            threshold: Z-score threshold for anomaly detection
            
        Returns:
            Dictionary with anomaly analysis results
        """
        player_data = df[df['Player'] == player][metric].dropna()
        
        if len(player_data) < 10:
            return {"error": "Need at least 10 data points for anomaly detection"}
            
        mean_val = player_data.mean()
        std_val = player_data.std()
        z_scores = np.abs((player_data - mean_val) / std_val)
        
        anomalies = player_data[z_scores > threshold]
        
        return {
            "player": player,
            "metric": metric,
            "total_matches": len(player_data),
            "anomalies_found": len(anomalies),
            "anomaly_rate": len(anomalies) / len(player_data) * 100,
            "threshold": threshold,
            "statistics": {
                "mean": mean_val,
                "std": std_val,
                "min": player_data.min(),
                "max": player_data.max()
            },
            "anomalous_values": anomalies.tolist() if len(anomalies) > 0 else []
        }


def perform_comprehensive_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform comprehensive statistical analysis on the dataset.
    
    Args:
        df: Processed DataFrame
        
    Returns:
        Dictionary with comprehensive analysis results
    """
    analyzer = CODStatisticalAnalyzer()
    
    results = {
        "dataset_summary": {
            "total_matches": len(df),
            "players": df['Player'].unique().tolist(),
            "games": df['Game Name'].unique().tolist(),
            "date_range": {
                "start": df['UTC Timestamp'].min().isoformat() if 'UTC Timestamp' in df.columns else None,
                "end": df['UTC Timestamp'].max().isoformat() if 'UTC Timestamp' in df.columns else None
            }
        }
    }
    
    # Key metrics for analysis
    key_metrics = ['KD_Ratio', 'SPM', 'Skill', 'Accuracy', 'Score']
    available_metrics = [m for m in key_metrics if m in df.columns]
    
    if available_metrics:
        # Player comparisons
        results["player_comparisons"] = {}
        for metric in available_metrics[:3]:  # Limit to avoid too much data
            results["player_comparisons"][metric] = analyzer.compare_players_performance(df, metric)
            
        # Correlation analysis
        results["correlation_analysis"] = analyzer.calculate_correlation_analysis(df, available_metrics)
        
        # Player rankings
        results["player_rankings"] = analyzer.calculate_player_rankings(df, available_metrics).to_dict()
        
    return results
