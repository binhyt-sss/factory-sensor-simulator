# Factory Sensor Simulator

This project simulates various industrial sensors for different machine types in a factory environment. It generates realistic sensor data that can be used for testing, development, and demonstration purposes. The simulator includes data for temperature, vibration, pressure, and other sensor types with realistic patterns and anomalies.

## Features

- Simulates 5 different types of industrial machines with their specific sensors
- Generates realistic sensor data with configurable noise, trends, and anomalies
- Integrates with ThingsBoard IoT platform for data visualization
- Supports containerized deployment with Docker
- Includes data export functionality to JSON format
- Provides statistical analysis and visualization tools

## Supported Machine Types and Sensors
The simulator includes the following machine types and their associated sensors:
### 1. MIXER (Máy trộn)
- **Temperature Sensors**: RTD PT100, Thermocouple K-Type, Infrared Temperature Sensor
- **Vibration/Motion Sensors**: Piezoelectric Accelerometer, Rotary Encoder, Gyroscope
- **Audio Sensor**: Industrial Microphone
- **Level Sensors**: Capacitive Level Sensor, Ultrasonic Level Sensor
- **Power Monitoring**: Current Transformer (CT), Power Meter
### 2. CNC MACHINE
- **Temperature Sensors**: RTD PT100, Thermocouple J-Type, Thermal Imaging Sensor
- **Vibration Sensors**: MEMS Accelerometer, Proximity Probe, Strain Gauge
- **Position Sensors**: Linear Encoder, Absolute Encoder, LVDT
- **Pressure/Flow Sensors**: Pressure Transducer, Electromagnetic Flow Meter, Differential Pressure Sensor
- **Level Sensors**: Float Level Switch, Capacitive Level Sensor
- **Optical Sensors**: Laser Distance Sensor, Photoelectric Sensor
- **Audio Sensor**: Acoustic Emission Sensor

### 3. HYDRAULIC PRESS
- **Pressure Sensors**: Strain Gauge Pressure Transducer, Piezoelectric Pressure Sensor, Bourdon Tube Gauge
- **Temperature Sensors**: RTD PT100, Thermistor, Bimetallic Temperature Switch
- **Position Sensors**: LVDT, Magnetostrictive Position Sensor, Limit Switch
- **Force/Load Sensors**: Load Cell, Strain Gauge, Piezoelectric Force Sensor
- **Vibration Sensors**: Industrial Accelerometer, Velocity Sensor

### 4. CONVEYOR SYSTEM
- **Speed/Motion Sensors**: Tachometer Generator, Hall Effect Sensor, Incremental Encoder
- **Detection Sensors**: Photoelectric Sensor, Inductive Proximity Sensor, Laser Scanner, Ultrasonic Sensor
- **Load/Weight Sensors**: Belt Scale Load Cell, Strain Gauge
- **Safety Sensors**: Emergency Stop Switch, Light Curtain, Safety Mat

### 5. PUMP SYSTEM
- **Flow Sensors**: Electromagnetic Flow Meter, Turbine Flow Meter, Ultrasonic Flow Meter
- **Pressure Sensors**: Bourdon Pressure Gauge, Diaphragm Pressure Sensor, Differential Pressure Transmitter
- **Level Sensors**: Radar Level Sensor, Hydrostatic Level Sensor, Float Level Switch
- **Temperature Sensors**: RTD PT100, Thermowell
- **Vibration Sensors**: Accelerometer, Proximity Probe

## Setup and Installation

### Prerequisites
- Python 3.10 or higher
- Docker (optional, for containerized deployment)
- ThingsBoard account (for data visualization)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/binhyt-sss/factory-sensor-simulator.git
   cd factory-sensor-simulator
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
Configure the simulator by editing the `tokens.json` file with your ThingsBoard credentials:

```json
{
  "url": "https://your-thingsboard-instance.com",
  "username": "your-username",
  "password": "your-password"
}
```

## Usage

### Running the Simulator
To start the simulator with default settings:
```bash
python src/thingsboard/main.py
```

For specific machine types:
```bash
python src/thingsboard/main.py --machine-type MIXER
```

### Adjusting Simulation Parameters
You can adjust simulation parameters like data generation frequency, noise levels, and anomaly probability in the configuration files.

### Docker Deployment
You can also run the simulator in a Docker container:
```bash
docker-compose up -d
```

### Analyzing Generated Data
The simulator includes tools for analyzing the generated data:

```bash
python src/analysis/visualize_data.py
```

## Project Structure
- `src/sensor/`: Contains the sensor simulation models
- `src/thingsboard/`: Contains ThingsBoard integration code
- `simulation_data/`: Generated sensor data files
- `analysis_results/`: Data analysis visualizations
- `docker-compose.yml`: Docker Compose configuration for containerized deployment
- `Dockerfile`: Docker configuration for building the container image
- `requirements.txt`: Python dependencies

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[MIT License](LICENSE)

## Acknowledgements
- This project was developed to simulate industrial IoT sensor data for training and testing purposes.
- Special thanks to the ThingsBoard community for their excellent IoT platform.