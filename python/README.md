# ESP-NOW Data Collection & Analysis

Python tools for collecting and analyzing ESP-NOW mesh network performance data from ESP8266 nodes.

## 📁 Files

- **`collect.py`** - Main data collector, reads JSON from serial port
- **`analyze.py`** - Data analysis and visualization tool  
- **`demo.py`** - Demo/test script with synthetic data generation

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate     # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Test with Synthetic Data
```bash
python demo.py --synthetic --samples 100
python analyze.py  # Analyzes the latest generated data
```

### 3. Collect Real Data
```bash
# Find your ESP8266 serial port (e.g., COM3, /dev/ttyUSB0)
python collect.py --port COM3 --duration 60 --output data/raw/field_test_001.csv

# Analyze collected data
python analyze.py data/raw/field_test_001.csv
```

## 📊 Data Format

The ESP8266 firmware outputs JSON lines like:
```json
{"seq":123,"rssi":-45,"lat_us":8500}
{"error":"pong_timeout"}
```

**Fields:**
- `seq` - Packet sequence number
- `rssi` - Received Signal Strength Indicator (dBm)  
- `lat_us` - Round-trip latency in microseconds
- `timestamp` - Added by collector (ISO format)
- `error` - Error message for failed packets

## 🔧 Usage Examples

### Data Collection
```bash
# Basic collection
python collect.py --port COM3

# Timed collection (5 minutes)
python collect.py --port COM3 --duration 300

# Limited samples
python collect.py --port COM3 --samples 1000

# Custom output location
python collect.py --port COM3 --output experiments/outdoor_test.csv
```

### Data Analysis
```bash
# Analyze specific file
python analyze.py data/raw/esp_now_data_20231215_143022.csv

# Auto-find latest file
python analyze.py

# Generate plots only
python analyze.py --output reports/
```

### Demo/Testing
```bash
# Generate synthetic test data
python demo.py --synthetic --samples 200

# Test hardware connection
python demo.py --real-port COM3 --duration 30
```

## 📈 Analysis Output

The analyzer provides:

**Console Summary:**
- Dataset size and duration
- RSSI statistics (mean, range, distribution)
- Latency statistics (percentiles, variance)
- Packet loss estimation

**Visualizations:**
- RSSI distribution histogram
- Latency distribution histogram  
- Time series plots (RSSI vs time)
- Correlation plots (RSSI vs latency)

## 🛠️ Integration with Phase 3+

This collector is designed for **Phase 2** but will extend to later phases:

- **Phase 3 (Mesh):** Multi-node data collection via multiple serial ports
- **Phase 5 (ML):** Feature engineering for routing model training
- **Phase 6 (Laptop-in-loop):** Real-time decision integration
- **Phase 8 (Field trials):** Large-scale data collection campaigns

## 🚨 Troubleshooting

**Serial Connection Issues:**
```bash
# Windows: Check Device Manager for COM port
# Linux: ls /dev/ttyUSB* or ls /dev/ttyACM*

# Test connection
python demo.py --real-port COM3
```

**JSON Parse Errors:**
- Check ESP8266 firmware output format
- Verify baud rate (default: 115200)
- Serial cable quality

**No Data Collected:**
- Verify ESP8266 is running ping-pong firmware
- Check peer MAC addresses in firmware  
- Test with synthetic data first: `python demo.py --synthetic`