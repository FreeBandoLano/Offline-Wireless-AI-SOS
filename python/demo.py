#!/usr/bin/env python3
"""
ESP-NOW Demo/Test Script for Web of Grace Project

Simulates ESP-NOW data collection for testing purposes when hardware is not available.

Usage:
    python demo.py                              # Generate synthetic data
    python demo.py --real-port COM3             # Test with real hardware
    python demo.py --synthetic --samples 100    # Generate 100 synthetic samples
"""

import argparse
import json
import time
import random
from datetime import datetime
from pathlib import Path

from collect import ESP8266DataCollector


class SyntheticESP8266:
    """Generates synthetic ESP-NOW data for testing."""
    
    def __init__(self, base_rssi: int = -50, base_latency: int = 8000):
        """Initialize synthetic data generator."""
        self.base_rssi = base_rssi
        self.base_latency = base_latency
        self.seq = 0
    
    def generate_sample(self) -> dict:
        """Generate one synthetic ESP-NOW sample."""
        # Simulate RSSI variation (-30 to -80 dBm typical range)
        rssi_noise = random.gauss(0, 5)  # 5 dBm standard deviation
        rssi = max(-80, min(-30, self.base_rssi + rssi_noise))
        
        # Simulate latency variation (base ± 30%)
        lat_noise = random.gauss(0, self.base_latency * 0.1)
        latency = max(1000, int(self.base_latency + lat_noise))  # Min 1ms
        
        # Occasional packet loss/timeout simulation
        if random.random() < 0.02:  # 2% error rate
            return {"error": "pong_timeout"}
        
        sample = {
            "seq": self.seq,
            "rssi": int(rssi),
            "lat_us": latency
        }
        
        self.seq += 1
        return sample
    
    def simulate_collection(self, samples: int = 50, delay: float = 0.5) -> list:
        """Simulate data collection session."""
        print(f"🔄 Generating {samples} synthetic ESP-NOW samples...")
        
        data = []
        for i in range(samples):
            sample = self.generate_sample()
            sample['timestamp'] = datetime.now().isoformat()
            data.append(sample)
            
            # Print progress
            if (i + 1) % 10 == 0:
                print(f"   Generated {i + 1}/{samples} samples")
            
            time.sleep(delay)
        
        print(f"✅ Generated {len(data)} synthetic samples")
        return data


def test_real_hardware(port: str, duration: float = 30):
    """Test data collection with real ESP8266 hardware."""
    print(f"🔌 Testing real hardware on {port}")
    
    collector = ESP8266DataCollector(port)
    
    try:
        if not collector.connect():
            return False
        
        print("📡 Collecting data from ESP8266...")
        data = collector.collect_data(duration=duration)
        
        if data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"data/raw/hardware_test_{timestamp}.csv"
            collector.save_to_csv(output_file)
            print(f"✅ Hardware test complete: {len(data)} samples saved")
            return True
        else:
            print("⚠️  No data received from hardware")
            return False
            
    except Exception as e:
        print(f"❌ Hardware test failed: {e}")
        return False
    finally:
        collector.disconnect()


def test_synthetic_data(samples: int = 50):
    """Test with synthetic data generation."""
    print("🎲 Testing with synthetic data")
    
    # Generate synthetic data
    generator = SyntheticESP8266()
    data = generator.simulate_collection(samples=samples, delay=0.1)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"data/raw/synthetic_test_{timestamp}.csv"
    
    # Convert to DataFrame and save
    import pandas as pd
    df = pd.DataFrame(data)
    
    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    
    print(f"✅ Synthetic test complete: {len(data)} samples saved to {output_file}")
    
    # Quick analysis
    valid_data = [d for d in data if 'error' not in d]
    if valid_data:
        rssi_values = [d['rssi'] for d in valid_data]
        lat_values = [d['lat_us'] for d in valid_data]
        
        print(f"📊 Quick Stats:")
        print(f"   Valid samples: {len(valid_data)}/{len(data)}")
        print(f"   RSSI range: {min(rssi_values)} to {max(rssi_values)} dBm")
        print(f"   Latency range: {min(lat_values)} to {max(lat_values)} μs")
    
    return output_file


def main():
    """Main demo interface."""
    parser = argparse.ArgumentParser(description="ESP-NOW Demo/Test")
    
    parser.add_argument('--real-port', '-p',
                       help='Test with real hardware on specified port')
    parser.add_argument('--synthetic', '-s', action='store_true',
                       help='Generate synthetic test data')
    parser.add_argument('--samples', '-n', type=int, default=50,
                       help='Number of synthetic samples (default: 50)')
    parser.add_argument('--duration', '-d', type=float, default=30,
                       help='Hardware test duration in seconds (default: 30)')
    
    args = parser.parse_args()
    
    print("🚀 ESP-NOW Data Collection Demo")
    print("=" * 40)
    
    success = False
    
    if args.real_port:
        # Test with real hardware
        success = test_real_hardware(args.real_port, args.duration)
    elif args.synthetic:
        # Generate synthetic data
        output_file = test_synthetic_data(args.samples)
        success = True
        
        # Optionally run analysis
        try:
            from analyze import ESP8266DataAnalyzer
            print(f"\n🔍 Running analysis on synthetic data...")
            analyzer = ESP8266DataAnalyzer(output_file)
            if analyzer.load_data():
                analyzer.print_summary()
        except ImportError:
            print("⚠️  Analysis module not available")
    else:
        # Default: show available options
        print("Choose a demo mode:")
        print("  --synthetic          Generate synthetic test data")
        print("  --real-port COM3     Test with real ESP8266 hardware")
        print("")
        print("Examples:")
        print("  python demo.py --synthetic --samples 100")
        print("  python demo.py --real-port COM3 --duration 60")
        return
    
    if success:
        print(f"\n🎉 Demo completed successfully!")
        print(f"💡 Next steps:")
        print(f"   1. Try: python analyze.py  (to analyze collected data)")
        print(f"   2. Check: data/raw/  (for CSV files)")
        print(f"   3. Run: python collect.py --port [YOUR_PORT]  (for real collection)")
    else:
        print(f"\n❌ Demo failed - check hardware connection or try synthetic mode")


if __name__ == "__main__":
    main()