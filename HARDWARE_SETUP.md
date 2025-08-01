# ESP8266 Hardware Setup Guide

## 🔧 **Phase 2 Testing Requirements**

### **Hardware Needed**
- **2x ESP8266 boards** (ESP-01S or similar)
- **2x USB-to-Serial adapters** (FTDI or CP2102)
- **Breadboards/jumper wires** for connections
- **Computer with 2 available USB ports**

### **Current Firmware Status**
Your project has ping-pong firmware ready at:
```
firmware/ping_pong_esp01s/src/main.cpp
```

## 🚀 **Step-by-Step Setup**

### **Step 1: Flash the Firmware**

#### **Board 1 (Pinger)**
```cpp
#define ROLE_PINGER  1      // Keep as 1
uint8_t PEER_MAC[] = {0xAA,0xBB,0xCC,0xDD,0xEE,0xFF};   // Will update this
```

#### **Board 2 (Ponger)** 
```cpp
#define ROLE_PINGER  0      // Change to 0
uint8_t PEER_MAC[] = {0x11,0x22,0x33,0x44,0x55,0x66};   // Update with Board 1's MAC
```

### **Step 2: Get MAC Addresses**

1. **Flash basic firmware to both boards**
2. **Connect via serial** (115200 baud)
3. **Add this code** to `setup()` to print MAC:
   ```cpp
   Serial.print("MAC Address: ");
   Serial.println(WiFi.macAddress());
   ```

### **Step 3: Update MAC Configuration**

Once you have both MAC addresses:
- **Board 1**: Set `PEER_MAC[]` to Board 2's MAC
- **Board 2**: Set `PEER_MAC[]` to Board 1's MAC  
- **Re-flash both boards**

### **Step 4: Test ESP-NOW Communication**

#### **Expected Serial Output (Board 1 - Pinger):**
```json
{"seq":0,"rssi":-45,"lat_us":8500}
{"seq":1,"rssi":-46,"lat_us":8200}
{"seq":2,"rssi":-44,"lat_us":8750}
```

#### **Expected Serial Output (Board 2 - Ponger):**
```
(No output - just echoes packets back)
```

## 🔍 **Testing Process**

### **Phase A: Verify Communication**
```bash
# Connect to pinger board
python python/demo.py --real-port COM3 --duration 30

# Should see JSON output like:
# {"seq":123,"rssi":-45,"lat_us":8500}
```

### **Phase B: Collect Real Data**
```bash
# Full data collection session
python python/collect.py --port COM3 --duration 300 --output data/raw/proximity_test_001.csv

# Analyze results
python python/analyze.py data/raw/proximity_test_001.csv
```

### **Phase C: Distance Testing**
1. **Start close** (1 meter apart)
2. **Gradually increase distance**
3. **Note when packets start failing**
4. **Document RSSI vs distance relationship**

## 🚨 **Troubleshooting**

### **No Serial Output**
- Check baud rate (115200)
- Verify USB drivers
- Test with Arduino Serial Monitor first

### **JSON Parse Errors**
- Board may be outputting debug info
- Check firmware compilation
- Verify ESP-NOW initialization

### **No ESP-NOW Communication**
- Check MAC addresses are correct
- Boards must be on same WiFi channel
- Distance < 50m for initial testing

### **Timeouts/Packet Loss**
- Normal for some packet loss (2-5%)
- High loss may indicate range/interference issues
- Try different locations

## 📊 **Expected Results**

### **Good Performance Indicators:**
- **RSSI**: -30 to -70 dBm range
- **Latency**: 5-15 ms typical  
- **Packet Loss**: < 5%
- **Consistent sequence numbers**

### **Phase 2 Success Criteria:**
- ✅ ESP-NOW ping-pong RTT < 10 ms
- ✅ UART logs `{seq,RSSI,μs}` 
- ✅ Python collector captures data to CSV
- ✅ Analysis shows meaningful performance metrics

## 🎯 **Next Phase Preparation**

Once proximity testing works:
- **Phase 3**: Add 2 more nodes (4 total)
- **Phase 4**: Field testing with distance measurements
- **Phase 5**: ML model training on collected data

---

**Ready to flash your ESP8266 boards and start testing!** 🚀