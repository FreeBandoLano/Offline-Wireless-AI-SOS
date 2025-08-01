#!/usr/bin/env python3
"""
ESP-NOW Data Collector for Web of Grace Project

Collects JSON metrics from ESP8266 ESP-NOW ping-pong nodes via serial.
Parses data into pandas DataFrame and exports to CSV.

Usage:
    python collect.py --port COM3 --output data/raw/session_001.csv
    python collect.py --port /dev/ttyUSB0 --duration 300  # 5 minutes
"""

import argparse
import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

import serial
import pandas as pd


class ESP8266DataCollector:
    """Collects and processes ESP-NOW metrics from serial port."""
    
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 1.0):
        """Initialize collector with serial port configuration."""
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn: Optional[serial.Serial] = None
        self.data_buffer: List[Dict] = []
        
    def connect(self) -> bool:
        """Establish serial connection to ESP8266."""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(f"✅ Connected to {self.port} at {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            print(f"❌ Failed to connect to {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Close serial connection."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("🔌 Serial connection closed")
    
    def parse_json_line(self, line: str) -> Optional[Dict]:
        """Parse JSON line from ESP8266 output."""
        line = line.strip()
        if not line:
            return None
            
        try:
            data = json.loads(line)
            # Add timestamp
            data['timestamp'] = datetime.now().isoformat()
            return data
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parse error: {e} | Line: {line}")
            return None
    
    def collect_data(self, duration: Optional[float] = None, max_samples: Optional[int] = None) -> List[Dict]:
        """
        Collect data from serial port.
        
        Args:
            duration: Collection time in seconds (None for indefinite)
            max_samples: Maximum number of samples to collect
            
        Returns:
            List of parsed JSON records
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise RuntimeError("Serial connection not established")
        
        start_time = time.time()
        sample_count = 0
        
        print(f"📡 Starting data collection...")
        if duration:
            print(f"   Duration: {duration:.1f} seconds")
        if max_samples:
            print(f"   Max samples: {max_samples}")
        
        try:
            while True:
                # Check termination conditions
                if duration and (time.time() - start_time) >= duration:
                    print(f"⏰ Duration limit reached ({duration}s)")
                    break
                if max_samples and sample_count >= max_samples:
                    print(f"📊 Sample limit reached ({max_samples})")
                    break
                
                # Read line from serial
                try:
                    line = self.serial_conn.readline().decode('utf-8', errors='ignore')
                    if line:
                        parsed = self.parse_json_line(line)
                        if parsed:
                            self.data_buffer.append(parsed)
                            sample_count += 1
                            
                            # Print progress every 10 samples
                            if sample_count % 10 == 0:
                                elapsed = time.time() - start_time
                                print(f"📈 Samples: {sample_count}, Elapsed: {elapsed:.1f}s")
                                
                except UnicodeDecodeError:
                    continue  # Skip malformed data
                    
        except KeyboardInterrupt:
            print(f"\n⏹️  Collection stopped by user")
        
        elapsed = time.time() - start_time
        print(f"✅ Collection complete: {len(self.data_buffer)} samples in {elapsed:.1f}s")
        
        return self.data_buffer.copy()
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert collected data to pandas DataFrame."""
        if not self.data_buffer:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.data_buffer)
        
        # Ensure timestamp is datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def save_to_csv(self, filepath: str) -> bool:
        """Save collected data to CSV file."""
        try:
            df = self.to_dataframe()
            if df.empty:
                print("⚠️  No data to save")
                return False
            
            # Ensure output directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            df.to_csv(filepath, index=False)
            print(f"💾 Data saved to {filepath} ({len(df)} rows)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save CSV: {e}")
            return False


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="ESP-NOW Data Collector")
    
    parser.add_argument('--port', '-p', required=True,
                       help='Serial port (e.g., COM3, /dev/ttyUSB0)')
    parser.add_argument('--baudrate', '-b', type=int, default=115200,
                       help='Serial baudrate (default: 115200)')
    parser.add_argument('--duration', '-d', type=float,
                       help='Collection duration in seconds')
    parser.add_argument('--samples', '-s', type=int,
                       help='Maximum number of samples to collect')
    parser.add_argument('--output', '-o',
                       help='Output CSV file path')
    
    args = parser.parse_args()
    
    # Generate default output filename if not provided
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"data/raw/esp_now_data_{timestamp}.csv"
    
    # Initialize collector
    collector = ESP8266DataCollector(args.port, args.baudrate)
    
    try:
        # Connect and collect data
        if not collector.connect():
            sys.exit(1)
        
        data = collector.collect_data(duration=args.duration, max_samples=args.samples)
        
        if data:
            collector.save_to_csv(args.output)
            
            # Print summary statistics
            df = collector.to_dataframe()
            print(f"\n📊 Data Summary:")
            print(f"   Total samples: {len(df)}")
            if 'rssi' in df.columns:
                print(f"   RSSI range: {df['rssi'].min()} to {df['rssi'].max()} dBm")
            if 'lat_us' in df.columns:
                print(f"   Latency range: {df['lat_us'].min()} to {df['lat_us'].max()} μs")
        else:
            print("⚠️  No valid data collected")
            
    except Exception as e:
        print(f"❌ Collection failed: {e}")
        sys.exit(1)
    finally:
        collector.disconnect()


if __name__ == "__main__":
    main()