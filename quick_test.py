#!/usr/bin/env python3
"""
Quick ESP8266 Test Script

Simple test to verify your ESP8266 is outputting data correctly
before running the full data collector.
"""

import serial
import time
import sys

def test_esp8266_output(port, duration=30):
    """Quick test of ESP8266 serial output"""
    
    print(f"🔌 Testing ESP8266 on port {port}")
    print(f"⏱️  Will monitor for {duration} seconds...")
    print("=" * 50)
    
    try:
        # Open serial connection
        ser = serial.Serial(port, 115200, timeout=1)
        time.sleep(2)  # Let connection stabilize
        
        start_time = time.time()
        line_count = 0
        json_count = 0
        
        while (time.time() - start_time) < duration:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    line_count += 1
                    print(f"[{time.time() - start_time:.1f}s] {line}")
                    
                    # Check if it looks like JSON
                    if line.startswith('{') and line.endswith('}'):
                        json_count += 1
                        
            except KeyboardInterrupt:
                break
                
        ser.close()
        
        print("=" * 50)
        print(f"📊 Test Results:")
        print(f"   Total lines received: {line_count}")
        print(f"   JSON-like lines: {json_count}")
        
        if json_count > 0:
            print(f"✅ ESP8266 appears to be working!")
            print(f"💡 Try: python python/collect.py --port {port}")
        else:
            print(f"⚠️  No JSON output detected")
            print(f"🔧 Check: Firmware flashed? Correct baud rate? ESP-NOW working?")
            
    except serial.SerialException as e:
        print(f"❌ Serial connection failed: {e}")
        print(f"💡 Available ports on Windows: COM1, COM3, COM4, etc.")
        print(f"💡 Available ports on Linux: /dev/ttyUSB0, /dev/ttyACM0, etc.")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
        
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python quick_test.py COM3")
        print("       python quick_test.py /dev/ttyUSB0")
        sys.exit(1)
    
    port = sys.argv[1]
    test_esp8266_output(port)

if __name__ == "__main__":
    main()