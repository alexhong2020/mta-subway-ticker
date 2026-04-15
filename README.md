# 🚇 NYC Subway Arrival Ticker (Roosevelt Island F-Train)

A real-time transit arrival board built with a **Raspberry Pi 3**, an **Adafruit RGB Matrix Bonnet**, and a **P3 64x32 LED Matrix**. This project fetches live MTA data via the GTFS-realtime feed and displays the next three arrivals for the Roosevelt Island station.



## 🛠 Hardware Components
* **Controller:** Raspberry Pi 3 Model B+
* **Display:** P3 64x32 RGB LED Matrix (1/16 Scan)
* **Interface:** Adafruit RGB Matrix Bonnet for Raspberry Pi
* **Power:** 5V 4A DC Power Supply (Dedicated to the Matrix)

## 🚀 Key Features
* **Real-Time Data:** Hooks into the MTA’s official GTFS-realtime API.
* **Custom Multiplexing:** Configured specifically for 1/16 scan rate panels to avoid "zooming" issues.
* **Optimized Layout:** Custom vertical spacing to fit the Roosevelt Island station name and three upcoming train times on a single 32-row screen.

## ⚙️ The "Secret Sauce" Configuration
The biggest challenge of this build was the hardware-software gap. Standard P3 panels often require specific timing and multiplexing flags to display correctly on a Raspberry Pi 3.

To run the ticker without flickering or scaling issues, the following command is used:
```bash
sudo python3 display.py --led-rows=32 --led-cols=64 --led-row-addr-type=2 --led-multiplexing=0 --led-slowdown-gpio=2
```

### Critical Flags Explained:
* `--led-row-addr-type=2`: Fixed the "Zoomed In" issue by remapping row addressing for the 1/16 scan panel.
* `--led-slowdown-gpio=2`: Necessary for Pi 3 to prevent "ghosting" or "red snow" caused by the high-speed GPIO pins.
* `--led-multiplexing=0`: Standard multiplexing for this specific Amazon-sourced panel.

## 📂 Project Structure
* `display.py`: The main entry point. Handles the LED canvas, font rendering, and the refresh loop.
* `mta.py`: The data engine. Authenticates with the MTA API and parses the GTFS protobuf feed into a readable list of minutes.
* `.gitignore`: Configured to keep API keys and Python caches out of the public repo.

## 🏗 Setup & Installation
1. **Clone the repo:**
   ```bash
   git clone git@github.com:alexhong2020/mta-subway-ticker.git
   cd mta-subway-ticker
   ```
2. **Install Dependencies:**
   Requires the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library by Henner Zeller.
3. **Add your MTA API Key:**
   Replace the placeholder in `mta.py` with your key from the [MTA Developer Portal](https://api.mta.info/).

## 📝 Substack Build Log
This project was documented in detail on my Substack. TBD.

