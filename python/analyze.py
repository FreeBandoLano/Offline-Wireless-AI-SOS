#!/usr/bin/env python3
"""
ESP-NOW Data Analysis for Web of Grace Project

Analyzes collected ESP-NOW metrics and generates visualizations.

Usage:
    python analyze.py data/raw/esp_now_data_20231215_143022.csv
    python analyze.py --input data/processed/ --output reports/
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class ESP8266DataAnalyzer:
    """Analyzes ESP-NOW performance metrics."""
    
    def __init__(self, data_file: str):
        """Initialize analyzer with data file."""
        self.data_file = data_file
        self.df: Optional[pd.DataFrame] = None
        
    def load_data(self) -> bool:
        """Load data from CSV file."""
        try:
            self.df = pd.read_csv(self.data_file)
            
            # Convert timestamp if present
            if 'timestamp' in self.df.columns:
                self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            
            print(f"✅ Loaded {len(self.df)} records from {self.data_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load data: {e}")
            return False
    
    def basic_stats(self) -> dict:
        """Generate basic statistics summary."""
        if self.df is None:
            return {}
        
        stats = {
            'total_samples': len(self.df),
            'time_span': None,
            'rssi_stats': {},
            'latency_stats': {},
            'packet_loss': 0
        }
        
        # Time analysis
        if 'timestamp' in self.df.columns:
            duration = (self.df['timestamp'].max() - self.df['timestamp'].min()).total_seconds()
            stats['time_span'] = f"{duration:.1f} seconds"
        
        # RSSI analysis
        if 'rssi' in self.df.columns:
            rssi_data = self.df['rssi'].dropna()
            stats['rssi_stats'] = {
                'mean': rssi_data.mean(),
                'std': rssi_data.std(),
                'min': rssi_data.min(),
                'max': rssi_data.max(),
                'median': rssi_data.median()
            }
        
        # Latency analysis
        if 'lat_us' in self.df.columns:
            lat_data = self.df['lat_us'].dropna()
            stats['latency_stats'] = {
                'mean_us': lat_data.mean(),
                'std_us': lat_data.std(),
                'min_us': lat_data.min(),
                'max_us': lat_data.max(),
                'median_us': lat_data.median(),
                'p95_us': lat_data.quantile(0.95),
                'p99_us': lat_data.quantile(0.99)
            }
        
        # Packet loss (estimate from sequence gaps)
        if 'seq' in self.df.columns:
            seq_data = self.df['seq'].dropna().sort_values()
            expected_packets = seq_data.max() - seq_data.min() + 1 if len(seq_data) > 0 else 0
            actual_packets = len(seq_data)
            stats['packet_loss'] = max(0, (expected_packets - actual_packets) / expected_packets * 100) if expected_packets > 0 else 0
        
        return stats
    
    def print_summary(self):
        """Print analysis summary to console."""
        stats = self.basic_stats()
        
        print("\n📊 ESP-NOW Performance Analysis")
        print("=" * 50)
        
        print(f"📈 Dataset: {stats['total_samples']} samples")
        if stats['time_span']:
            print(f"⏱️  Duration: {stats['time_span']}")
        
        if stats['rssi_stats']:
            rssi = stats['rssi_stats']
            print(f"\n📡 RSSI Analysis:")
            print(f"   Mean: {rssi['mean']:.1f} dBm (±{rssi['std']:.1f})")
            print(f"   Range: {rssi['min']:.0f} to {rssi['max']:.0f} dBm")
            print(f"   Median: {rssi['median']:.1f} dBm")
        
        if stats['latency_stats']:
            lat = stats['latency_stats']
            print(f"\n⚡ Latency Analysis:")
            print(f"   Mean: {lat['mean_us']:.0f} μs (±{lat['std_us']:.0f})")
            print(f"   Range: {lat['min_us']:.0f} to {lat['max_us']:.0f} μs")
            print(f"   Median: {lat['median_us']:.0f} μs")
            print(f"   95th percentile: {lat['p95_us']:.0f} μs")
            print(f"   99th percentile: {lat['p99_us']:.0f} μs")
        
        print(f"\n📦 Packet Loss: {stats['packet_loss']:.2f}%")
    
    def create_visualizations(self, output_dir: str = "reports/"):
        """Generate analysis plots."""
        if self.df is None:
            print("❌ No data loaded for visualization")
            return
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
        
        # 1. RSSI Distribution
        if 'rssi' in self.df.columns:
            plt.figure(figsize=(10, 6))
            plt.subplot(2, 2, 1)
            self.df['rssi'].hist(bins=30, alpha=0.7, color='blue')
            plt.xlabel('RSSI (dBm)')
            plt.ylabel('Frequency')
            plt.title('RSSI Distribution')
            plt.grid(True, alpha=0.3)
        
        # 2. Latency Distribution
        if 'lat_us' in self.df.columns:
            plt.subplot(2, 2, 2)
            self.df['lat_us'].hist(bins=30, alpha=0.7, color='green')
            plt.xlabel('Latency (μs)')
            plt.ylabel('Frequency')
            plt.title('Latency Distribution')
            plt.grid(True, alpha=0.3)
        
        # 3. Time series (if timestamp available)
        if 'timestamp' in self.df.columns and 'rssi' in self.df.columns:
            plt.subplot(2, 2, 3)
            plt.plot(self.df['timestamp'], self.df['rssi'], alpha=0.6, linewidth=0.8)
            plt.xlabel('Time')
            plt.ylabel('RSSI (dBm)')
            plt.title('RSSI vs Time')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
        
        # 4. RSSI vs Latency correlation
        if 'rssi' in self.df.columns and 'lat_us' in self.df.columns:
            plt.subplot(2, 2, 4)
            plt.scatter(self.df['rssi'], self.df['lat_us'], alpha=0.6, s=10)
            plt.xlabel('RSSI (dBm)')
            plt.ylabel('Latency (μs)')
            plt.title('RSSI vs Latency')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        output_file = Path(output_dir) / "esp_now_analysis.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"📊 Visualizations saved to {output_file}")
        
        plt.show()


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="ESP-NOW Data Analyzer")
    
    parser.add_argument('input_file', nargs='?',
                       help='Input CSV file path')
    parser.add_argument('--output', '-o', default="reports/",
                       help='Output directory for reports (default: reports/)')
    parser.add_argument('--no-plots', action='store_true',
                       help='Skip generating plots')
    
    args = parser.parse_args()
    
    if not args.input_file:
        # Look for latest file in data/raw/
        data_dir = Path("data/raw")
        if data_dir.exists():
            csv_files = list(data_dir.glob("*.csv"))
            if csv_files:
                args.input_file = str(sorted(csv_files)[-1])  # Most recent
                print(f"🔍 Using latest data file: {args.input_file}")
            else:
                print("❌ No CSV files found in data/raw/")
                sys.exit(1)
        else:
            print("❌ No input file specified and data/raw/ not found")
            parser.print_help()
            sys.exit(1)
    
    # Initialize analyzer
    analyzer = ESP8266DataAnalyzer(args.input_file)
    
    try:
        if not analyzer.load_data():
            sys.exit(1)
        
        # Print summary
        analyzer.print_summary()
        
        # Generate visualizations
        if not args.no_plots:
            analyzer.create_visualizations(args.output)
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()