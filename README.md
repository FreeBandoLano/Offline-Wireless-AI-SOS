# Offline Wireless AI SOS Project

> Encrypted ESP-NOW mesh with AI-assisted routing.

## Quick start
```bash
python -m venv .venv
. .venv/Scripts/Activate   # or source .venv/bin/activate
pip install -r requirements.txt
```

## 🎉 Phase 2 Complete - Python Data Collector

**ESP-NOW data collection infrastructure is now ready!**

### ✅ What's New
- **`python/collect.py`** - Serial data collector with JSON parsing
- **`python/analyze.py`** - Data analysis and visualization tools  
- **`python/demo.py`** - Demo/test framework with synthetic data
- **`requirements.txt`** - Complete Python dependencies
- **`HARDWARE_SETUP.md`** - Hardware testing guide
- **`quick_test.py`** - Simple ESP8266 connectivity tester

### 🚀 Try It Now
```bash
# Test with synthetic data (no hardware needed)
python python/demo.py --synthetic --samples 100

# Test with real ESP8266 hardware
python python/collect.py --port COM3 --duration 60

# Analyze collected data
python python/analyze.py
```

### 📊 Phase 2 Deliverables Met
✅ JSON metrics streamed every packet  
✅ `python/collect.py` → Pandas DataFrame  
✅ Real-time data collection via serial  
✅ CSV export with timestamps  
✅ Statistical analysis and visualization  
✅ Synthetic data generation for testing
## 🚦 Project Roadmap

| Phase&nbsp;≫&nbsp;Milestone | Target&nbsp;Date | Exit&nbsp;Criteria / Key Deliverables | Owner | Core Tasks (Σ = est. time) |
|---|---|---|---|---|
| **0. Kick-off & Env** | T₀ + 2 d | • GitHub repo scaffold (✅) <br>• VS Code + PlatformIO & Python venv ready <br>• Issue board seeded | Both | ▫ Lock scope (2 h) <br>▫ Flash “blink” sanity sketch (1 h) |
| **1. Single-Hop Proof** | T₀ + 1 w | • ESP-NOW ping-pong RTT < 10 ms <br>• UART logs `{seq,RSSI,μs}` | ✅ **COMPLETE** | ▫ Write minimal sketch (3 h) <br>▫ Serial sniff via PowerShell (1 h) |
| **2. Metric Logger** | T₀ + 10 d | • JSON metrics streamed every pkt <br>• `python/collect.py` → Pandas DF | ✅ **COMPLETE** | ▫ Enhance sketch (2 h) <br>▫ `pyserial` listener (2 h) |
| **3. Mesh Sandbox** | T₀ + 3 w | • 4 nodes flooding seq 0→3 <br>• Live topology graph on laptop | Tai | ▫ Duplicate sketches (1 h) <br>▫ Basic flood logic (2 h) |
| **4. Data Harvest v1** | T₀ + 4 w | • ≥ 1 k rows CSV `{src,dst,rssi,latency,hop}` | Both | ▫ Field walk-test (4 h) <br>▫ Clean & label (2 h) |
| **5. Baseline Model** | T₀ + 5 w | • `train.py` → RF model ≥ 70 % acc <br>• `model.pkl` saved | Arg | ▫ Feature eng. (3 h) <br>▫ Train / CM (3 h) |
| **6. Laptop-in-loop Routing** | T₀ + 6 w | • Serial proto round-trip < 100 ms <br>• Demo adaptive routing | Both | ▫ Define frame + CRC Σ (1 h) <br>▫ Python daemon (2 h) |
| **7. Security Layer** | T₀ + 7 w | • AES-128 + HMAC, throughput ▲ < 15 % | Tai | ▫ Integrate CryptoAES (2 h) |
| **8. Field Trial v2** | T₀ + 8 w | • Latency heat-map, post-mortem report | Arg | ▫ Collect 5 k pts (3 h) <br>▫ Visualise w/ `folium` (2 h) |
| **9. Stretch Goals** | — | RPi port, LoRa fallback, Flask dashboard | — | — |

> **Symbols:** Σ = sum/total effort; μs = microseconds; RTT = round-trip time.

