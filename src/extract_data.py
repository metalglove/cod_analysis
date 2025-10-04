#!/usr/bin/env python3
"""
Data Extraction Script for COD Analysis

This script helps extract data from your original analysis.ipynb notebook
and converts it to a format that can be used in the enhanced analysis.

Usage:
1. Run your original analysis.ipynb notebook up to the point where 'dfa' is created
2. In a new cell in that notebook, run: exec(open('extract_data.py').read())
3. This will create 'extracted_cod_data.csv' that can be used in enhanced_analysis.ipynb
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def extract_cod_data(dfa):
    """
    Extract and export the processed COD data from the original notebook.
    
    Args:
        dfa: The processed DataFrame from the original analysis
    """
    print("🔄 Extracting COD data from original notebook...")
    
    # Basic info
    print(f"📊 Total records: {len(dfa)}")
    print(f"👥 Players: {dfa['Player'].unique().tolist()}")
    print(f"📅 Date range: {dfa['UTC Timestamp'].min()} to {dfa['UTC Timestamp'].max()}")
    
    # Show column info
    print(f"\n📈 Available columns ({len(dfa.columns)}):")
    for i, col in enumerate(dfa.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Export to CSV
    output_file = 'extracted_cod_data.csv'
    dfa.to_csv(output_file, index=False)
    print(f"\n✅ Data exported to: {output_file}")
    
    # Create summary statistics
    summary_file = 'data_summary.txt'
    with open(summary_file, 'w') as f:
        f.write("COD Analysis Data Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total records: {len(dfa)}\n")
        f.write(f"Players: {', '.join(dfa['Player'].unique())}\n")
        f.write(f"Games: {', '.join(dfa['Game Name'].unique())}\n")
        f.write(f"Date range: {dfa['UTC Timestamp'].min()} to {dfa['UTC Timestamp'].max()}\n")
        f.write(f"Total days: {(dfa['UTC Timestamp'].max() - dfa['UTC Timestamp'].min()).days}\n\n")
        
        # Player statistics
        f.write("Player Statistics:\n")
        f.write("-" * 20 + "\n")
        player_stats = dfa.groupby('Player').agg({
            'Kills': ['count', 'mean', 'std'],
            'Deaths': 'mean',
            'Score': 'mean',
            'Skill': 'mean'
        }).round(2)
        f.write(str(player_stats))
        f.write("\n\n")
        
        # Game distribution
        f.write("Game Distribution:\n")
        f.write("-" * 18 + "\n")
        game_counts = dfa['Game Name'].value_counts()
        for game, count in game_counts.items():
            f.write(f"{game}: {count} matches\n")
    
    print(f"📋 Summary saved to: {summary_file}")
    
    return output_file

# If running directly (not imported)
if __name__ == "__main__":
    # Check if we're running in a notebook with 'dfa' variable
    try:
        # This will work if 'dfa' exists in the current namespace
        if 'dfa' in locals() or 'dfa' in globals():
            dfa_var = dfa if 'dfa' in locals() else globals()['dfa']
            extract_cod_data(dfa_var)
        else:
            print("❌ No 'dfa' variable found.")
            print("📝 To use this script:")
            print("1. Run your original analysis.ipynb notebook")
            print("2. After the data processing steps, add a new cell with:")
            print("   exec(open('extract_data.py').read())")
            print("3. This will create 'extracted_cod_data.csv'")
    except NameError:
        print("❌ This script should be run from within the original notebook")
        print("   where the 'dfa' DataFrame has been created.")
