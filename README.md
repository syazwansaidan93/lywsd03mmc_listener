# Bleak Direct LYWSD03MMC Poller

This document provides a comprehensive overview of the Python script designed to connect to Xiaomi LYWSD03MMC (and potentially LYWSD02MMC) Bluetooth Low Energy (BLE) temperature and humidity sensors, poll their data, and output it in a JSON-like format. The script is designed for resource-constrained embedded devices, focusing on compactness and efficiency.

## Table of Contents

- [Overview](#1-overview)
- [Features](#2-features)
- [Prerequisites](#3-prerequisites)
- [Configuration (config.json)](#4-configuration-configjson)
- [How it Works](#5-how-it-works)
  - [Constants](#constants)
  - [Notification Handler (n_h)](#notification-handler-n_h)
  - [Connect and Listen (c_a_l)](#connect-and-listen-c_a_l)
  - [Main Function (main)](#main-function-main)
- [Output Format](#6-output-format)
- [Usage](#7-usage)
- [Limitations](#8-limitations)

## 1. Overview

This Python script utilizes the bleak library to establish and maintain direct BLE connections with specified Xiaomi LYWSD03MMC/LYWSD02MMC temperature and humidity sensors. It reads environmental data (temperature and humidity) via notifications and attempts to read battery percentage from the standard GATT Battery Level characteristic. The polling interval and target MAC addresses are configurable via an external config.json file.

The script is optimized for minimal resource usage, making it suitable for embedded systems. Debugging messages and extensive comments are intentionally removed to keep the code compact.

## 2. Features

- **Direct BLE Connection**: Establishes a direct connection to the sensor, allowing for active data retrieval.
- **Configurable Polling Interval**: Data retrieval frequency can be set in minutes via config.json.
- **Temperature & Humidity Reading**: Continuously receives temperature and humidity updates via BLE notifications.
- **Battery Percentage Reading**: Reads the battery percentage from the standard GATT Battery Level characteristic upon connection.
- **JSON Output**: Prints sensor data to standard output in a compact JSON-like string format.
- **Error Handling**: Includes basic exception handling for BLE operations and file I/O.
- **Cross-Platform Compatibility**: Designed to run on various operating systems supported by bleak.

## 3. Prerequisites

- **Python 3.7+**: The script requires a modern Python version.
- **bleak library**: This asynchronous BLE client library is essential.

```bash
pip install bleak
```

- **Bluetooth Adapter**: A functional Bluetooth Low Energy (BLE) adapter on the host device.
- **Xiaomi LYWSD03MMC/LYWSD02MMC Sensor(s)**: The physical sensor devices.

## 4. Configuration (config.json)

The script reads its configuration from a file named `config.json` located in the same directory as the script.

### Example config.json:

```json
{
    "mac_addresses": [
        "A4:C1:38:E6:AD:AD",
        "XX:XX:XX:XX:XX:XX"
    ],
    "poll_interval_minutes": 30
}
```

- **mac_addresses** (list of strings, required): A list of MAC addresses for the LYWSD03MMC/LYWSD02MMC sensors you want to monitor. Replace the example MAC addresses with your actual device MAC addresses.
- **poll_interval_minutes** (integer, optional): The interval in minutes at which the script will attempt to poll the sensors. If not specified, it defaults to 1 minute.

### Error Handling for Configuration:

The script will exit with an error message if:

- `config.json` is not found.
- `config.json` contains invalid JSON.
- `mac_addresses` list is empty.

## 5. How it Works

The script is structured using Python's asyncio for concurrent handling of multiple BLE devices.

### Constants

- **CF**: Path to the configuration file (config.json).
- **MACS**: List of MAC addresses loaded from config.json.
- **PI**: Poll Interval in seconds, derived from poll_interval_minutes in config.json.
- **RT**: Request Timeout in seconds for BLE operations.
- **MDR**: Maximum Discovery Retries for finding a device.
- **DRD**: Delay between Discovery Retries.
- **D_C_U**: Data Characteristic UUID (`ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6`) for temperature and humidity notifications.
- **B_C_U**: Battery Characteristic UUID (`00002a19-0000-1000-8000-00805f9b34fb`) for standard battery level.
- **l_s_d**: Dictionary to store the latest sensor data for each MAC address.
- **a_c**: Dictionary to store active BleakClient instances.

### Notification Handler (n_h)

This function is a callback that gets triggered whenever the sensor sends new data via the `D_C_U` characteristic.

It parses the incoming byte data:

- Bytes 0-1 (little-endian, signed) are converted to temperature (divided by 100.0).
- Byte 2 is the humidity.

It updates the `l_s_d` dictionary with the latest temperature and humidity.

It retrieves the last known battery percentage (which is read once upon connection from `B_C_U`).

It prints the mac, temperature, humidity, and battery_percentage in a compact JSON-like string to standard output.

### Connect and Listen (c_a_l)

This asynchronous function is responsible for connecting to a single BLE device and maintaining its connection.

- Continuously attempts to find and connect to the specified MAC address.
- Upon connection, reads the initial battery percentage from the `B_C_U` characteristic.
- Enables notifications for the `D_C_U` characteristic.
- Enters a loop to keep the connection alive, sleeping for PI seconds.

Includes try-except blocks to handle reconnection on BLE errors.

### Main Function (main)

This is the entry point of the asynchronous application.

- Creates a separate `c_a_l` task for each MAC address in `MACS`.
- Uses `asyncio.gather` to run all tasks concurrently.

## 6. Output Format

The script prints sensor data to standard output in a compact JSON-like string format. Each line represents a new data point.

### Example Output:

```json
{"mac":"A4:C1:38:E6:AD:AD","temperature":25.34,"humidity":60,"battery_percentage":99}
```

- `mac`: The MAC address of the sensor.
- `temperature`: Measured temperature in Celsius.
- `humidity`: Measured humidity.
- `battery_percentage`: Battery percentage reported by the GATT characteristic.

## 7. Usage

1. **Save the script**: Save the Python code as `your_script_name.py` (e.g., `poller.py`).
2. **Create config.json** in the same directory.
3. **Run the script**:

```bash
python your_script_name.py
```

Press `Ctrl+C` to stop.

## 8. Limitations

- **Battery Percentage Granularity**: GATT battery readings are often coarse.
- **Error Messages**: Minimal output for compactness.
- **No Data Storage**: Output is not stored persistently.
- **Single Connection per Device**: Only one client should connect to each sensor.
- **Dependencies**: Requires `bleak` and system BLE stack.
