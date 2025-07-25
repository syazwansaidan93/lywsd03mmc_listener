
# Bleak Direct LYWSD03MMC Poller

This document provides a comprehensive overview of the Python script designed to connect to Xiaomi LYWSD03MMC (and potentially LYWSD02MMC) Bluetooth Low Energy (BLE) temperature and humidity sensors, poll their data, and output it in a JSON-like format. The script is designed for resource-constrained embedded devices, focusing on compactness and efficiency.

## Table of Contents
- Overview
- Features
- Prerequisites
- Configuration (config.json)
- How it Works
- Constants
- Notification Handler (n_h)
- Connect and Listen (c_a_l)
- Main Function (main)
- Output Format
- Usage
- Limitations

---

## 1. Overview

This Python script utilizes the bleak library to establish and maintain direct BLE connections with specified Xiaomi LYWSD03MMC/LYWSD02MMC temperature and humidity sensors. It reads environmental data (temperature and humidity) via notifications and attempts to read battery percentage from the standard GATT Battery Level characteristic. The polling interval and target MAC addresses are configurable via an external config.json file.

The script is optimized for minimal resource usage, making it suitable for embedded systems. Debugging messages and extensive comments are intentionally removed to keep the code compact.

---

## 2. Features

- **Direct BLE Connection**: Establishes a direct connection to the sensor, allowing for active data retrieval.
- **Configurable Polling Interval**: Data retrieval frequency can be set in minutes via config.json.
- **Temperature & Humidity Reading**: Continuously receives temperature and humidity updates via BLE notifications.
- **Battery Percentage Reading**: Reads the battery percentage from the standard GATT Battery Level characteristic upon connection.
- **JSON Output**: Prints sensor data to standard output in a compact JSON-like string format.
- **Error Handling**: Includes basic exception handling for BLE operations and file I/O.
- **Cross-Platform Compatibility**: Designed to run on various operating systems supported by bleak.

---

## 3. Prerequisites

- Python 3.7+
- bleak library:
  ```bash
  pip install bleak
  ```
- Bluetooth Adapter (BLE capable)
- Xiaomi LYWSD03MMC/LYWSD02MMC Sensors

---

## 4. Configuration (config.json)

Place a `config.json` file in the same directory as the script.

### Example:
```json
{
    "mac_addresses": [
        "A4:C1:38:E6:AD:AD",
        "XX:XX:XX:XX:XX:XX"
    ],
    "poll_interval_minutes": 30
}
```

### Error Handling:
The script exits with an error if `config.json` is missing, malformed, or the MAC list is empty.

---

## 5. How it Works

### Constants
Defines key UUIDs, file paths, poll intervals, etc.

### Notification Handler (n_h)
- Parses BLE notification bytes (temperature, humidity)
- Reads cached battery percent
- Prints output JSON

### Connect and Listen (c_a_l)
- Connects to device
- Reads battery
- Enables notifications
- Reconnects on failure

### Main Function (main)
- Loads config
- Starts asyncio BLE tasks

---

## 6. Output Format

Example:
```json
{"mac":"A4:C1:38:E6:AD:AD","temperature":25.34,"humidity":60,"battery_percentage":99}
```

---

## 7. Usage

1. Save script as `poller.py`
2. Place `config.json` in same directory
3. Run:
   ```bash
   python poller.py
   ```
4. Stop with `Ctrl+C`

---

## 8. Limitations

- Coarse battery readings (firmware limitation)
- Minimal logs
- No persistent storage
- Only one client per sensor

---
