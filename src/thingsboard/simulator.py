import random
import time
import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Import ThingsBoard connector
from src.thingsboard.connector import ThingsBoardConnector
from src.thingsboard.sensor_type import SensorType
from src.thingsboard.machine_type import MachineType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VirtualSensorSimulator")

class SensorSimulator:
    """Class to simulate sensor readings for various machine types."""
    
    # Define normal operating ranges for each sensor type
    SENSOR_RANGES = {
        # Temperature sensors (°C)
        SensorType.RTD_PT100: (20.0, 80.0),
        SensorType.THERMOCOUPLE_K_TYPE: (25.0, 90.0),
        SensorType.THERMOCOUPLE_J_TYPE: (20.0, 85.0),
        SensorType.INFRARED_TEMP: (22.0, 78.0),
        SensorType.THERMISTOR: (25.0, 75.0),
        SensorType.BIMETALLIC_TEMP_SWITCH: (30.0, 70.0),
        SensorType.THERMAL_IMAGING: (20.0, 95.0),
        
        # Vibration/motion sensors (mm/s or Hz)
        SensorType.PIEZOELECTRIC_ACCELEROMETER: (0.1, 15.0),
        SensorType.ROTARY_ENCODER: (50, 2000),
        SensorType.GYROSCOPE: (0.01, 5.0),
        SensorType.MEMS_ACCELEROMETER: (0.05, 10.0),
        SensorType.PROXIMITY_PROBE: (0.5, 5.0),
        SensorType.STRAIN_GAUGE: (10, 500),
        SensorType.INDUSTRIAL_ACCELEROMETER: (0.2, 20.0),
        SensorType.VELOCITY_SENSOR: (0.5, 25.0),
        
        # Audio sensors (dB)
        SensorType.INDUSTRIAL_MICROPHONE: (50, 95),
        SensorType.ACOUSTIC_EMISSION: (40, 90),
        
        # Level sensors (%)
        SensorType.CAPACITIVE_LEVEL: (10, 90),
        SensorType.ULTRASONIC_LEVEL: (5, 95),
        SensorType.FLOAT_LEVEL_SWITCH: (0, 100),
        SensorType.RADAR_LEVEL: (0, 100),
        SensorType.HYDROSTATIC_LEVEL: (5, 95),
        
        # Power/electrical sensors
        SensorType.CURRENT_TRANSFORMER: (5, 80),
        SensorType.POWER_METER: (50, 200),
        
        # Position/distance sensors (mm)
        SensorType.LINEAR_ENCODER: (0, 1000),
        SensorType.ABSOLUTE_ENCODER: (0, 360),
        SensorType.LVDT: (0, 100),
        SensorType.MAGNETOSTRICTIVE_POSITION: (0, 500),
        SensorType.LIMIT_SWITCH: (0, 1),
        SensorType.LASER_DISTANCE: (10, 5000),
        SensorType.PHOTOELECTRIC: (0, 1),
        
        # Pressure/flow sensors (bar or L/min)
        SensorType.PRESSURE_TRANSDUCER: (0, 100),
        SensorType.ELECTROMAGNETIC_FLOW: (5, 200),
        SensorType.DIFFERENTIAL_PRESSURE: (0, 25),
        SensorType.STRAIN_GAUGE_PRESSURE: (0, 150),
        SensorType.PIEZOELECTRIC_PRESSURE: (5, 120),
        SensorType.BOURDON_TUBE_GAUGE: (0, 100),
        SensorType.BOURDON_PRESSURE_GAUGE: (0, 100),
        SensorType.DIAPHRAGM_PRESSURE: (0, 50),
        SensorType.TURBINE_FLOW: (10, 300),
        SensorType.ULTRASONIC_FLOW: (5, 250),
        
        # Force/load sensors (kg or N)
        SensorType.LOAD_CELL: (0, 5000),
        SensorType.PIEZOELECTRIC_FORCE: (0, 10000),
        SensorType.BELT_SCALE_LOAD_CELL: (0, 2000),
        
        # Speed sensors (RPM or m/s)
        SensorType.TACHOMETER: (0, 3000),
        SensorType.HALL_EFFECT: (0, 1),
        SensorType.INCREMENTAL_ENCODER: (0, 5000),
        
        # Detection sensors (binary or mm)
        SensorType.INDUCTIVE_PROXIMITY: (0, 1),
        SensorType.LASER_SCANNER: (50, 10000),
        SensorType.ULTRASONIC_SENSOR: (100, 5000),
        
        # Safety sensors (binary)
        SensorType.EMERGENCY_STOP: (0, 1),
        SensorType.LIGHT_CURTAIN: (0, 1),
        SensorType.SAFETY_MAT: (0, 1)
    }
    
    # Define units for each sensor type
    SENSOR_UNITS = {
        # Temperature sensors
        SensorType.RTD_PT100: "°C",
        SensorType.THERMOCOUPLE_K_TYPE: "°C",
        SensorType.THERMOCOUPLE_J_TYPE: "°C",
        SensorType.INFRARED_TEMP: "°C",
        SensorType.THERMISTOR: "°C",
        SensorType.BIMETALLIC_TEMP_SWITCH: "°C",
        SensorType.THERMAL_IMAGING: "°C",
        
        # Vibration/motion sensors
        SensorType.PIEZOELECTRIC_ACCELEROMETER: "mm/s",
        SensorType.ROTARY_ENCODER: "RPM",
        SensorType.GYROSCOPE: "rad/s",
        SensorType.MEMS_ACCELEROMETER: "mm/s²",
        SensorType.PROXIMITY_PROBE: "mm",
        SensorType.STRAIN_GAUGE: "µε",
        SensorType.INDUSTRIAL_ACCELEROMETER: "mm/s²",
        SensorType.VELOCITY_SENSOR: "mm/s",
        
        # Audio sensors
        SensorType.INDUSTRIAL_MICROPHONE: "dB",
        SensorType.ACOUSTIC_EMISSION: "dB",
        
        # Level sensors
        SensorType.CAPACITIVE_LEVEL: "%",
        SensorType.ULTRASONIC_LEVEL: "%",
        SensorType.FLOAT_LEVEL_SWITCH: "binary",
        SensorType.RADAR_LEVEL: "%",
        SensorType.HYDROSTATIC_LEVEL: "%",
        
        # Power/electrical sensors
        SensorType.CURRENT_TRANSFORMER: "A",
        SensorType.POWER_METER: "kW",
        
        # Position/distance sensors
        SensorType.LINEAR_ENCODER: "mm",
        SensorType.ABSOLUTE_ENCODER: "degrees",
        SensorType.LVDT: "mm",
        SensorType.MAGNETOSTRICTIVE_POSITION: "mm",
        SensorType.LIMIT_SWITCH: "binary",
        SensorType.LASER_DISTANCE: "mm",
        SensorType.PHOTOELECTRIC: "binary",
        
        # Pressure/flow sensors
        SensorType.PRESSURE_TRANSDUCER: "bar",
        SensorType.ELECTROMAGNETIC_FLOW: "L/min",
        SensorType.DIFFERENTIAL_PRESSURE: "bar",
        SensorType.STRAIN_GAUGE_PRESSURE: "bar",
        SensorType.PIEZOELECTRIC_PRESSURE: "bar",
        SensorType.BOURDON_TUBE_GAUGE: "bar",
        SensorType.BOURDON_PRESSURE_GAUGE: "bar",
        SensorType.DIAPHRAGM_PRESSURE: "bar",
        SensorType.TURBINE_FLOW: "L/min",
        SensorType.ULTRASONIC_FLOW: "L/min",
        
        # Force/load sensors
        SensorType.LOAD_CELL: "kg",
        SensorType.PIEZOELECTRIC_FORCE: "N",
        SensorType.BELT_SCALE_LOAD_CELL: "kg",
        
        # Speed sensors
        SensorType.TACHOMETER: "RPM",
        SensorType.HALL_EFFECT: "binary",
        SensorType.INCREMENTAL_ENCODER: "pulses/rev",
        
        # Detection sensors
        SensorType.INDUCTIVE_PROXIMITY: "binary",
        SensorType.LASER_SCANNER: "mm",
        SensorType.ULTRASONIC_SENSOR: "mm",
        
        # Safety sensors
        SensorType.EMERGENCY_STOP: "binary",
        SensorType.LIGHT_CURTAIN: "binary",
        SensorType.SAFETY_MAT: "binary"
    }
    
    def __init__(self, machine_count: Dict[str, int] = None):
        """
        Initialize the sensor simulator.
        
        Args:
            machine_count: Dictionary with machine types as keys and count as values
        """
        self.machines = {}
        self.machine_sensors = {}
        self.sensor_values = {}
        
        # Default machine count if not provided
        if machine_count is None:
            machine_count = {
                MachineType.MIXER: 5,
                MachineType.CNC_MACHINE: 10,
                MachineType.HYDRAULIC_PRESS: 7,
                MachineType.CONVEYOR_SYSTEM: 8,
                MachineType.PUMP_SYSTEM: 6
            }
        
        # Initialize machines and their sensors
        self._initialize_machines(machine_count)
    
    def _initialize_machines(self, machine_count: Dict[str, int]):
        """Initialize machines and their sensors."""
        for machine_type, count in machine_count.items():
            for i in range(1, count + 1):
                machine_id = f"{machine_type}_{i:03d}"
                self.machines[machine_id] = machine_type
                
                # Initialize sensors for this machine
                self.machine_sensors[machine_id] = MachineType.MACHINE_SENSORS.get(machine_type, [])
                
                # Initialize sensor values with default values
                self.sensor_values[machine_id] = {}
                for sensor_type in self.machine_sensors[machine_id]:
                    # Get normal range for this sensor
                    min_val, max_val = self.SENSOR_RANGES.get(sensor_type, (0, 100))
                    
                    # For binary sensors, use 0 or 1
                    if self.SENSOR_UNITS.get(sensor_type) == "binary":
                        # Most safety sensors should be in "safe" state (1) by default
                        if sensor_type in [SensorType.EMERGENCY_STOP, SensorType.LIGHT_CURTAIN, 
                                         SensorType.SAFETY_MAT]:
                            self.sensor_values[machine_id][sensor_type] = 1
                        else:
                            self.sensor_values[machine_id][sensor_type] = random.choice([0, 1])
                    else:
                        # Generate a random value within normal range
                        initial_value = min_val + random.random() * (max_val - min_val)
                        self.sensor_values[machine_id][sensor_type] = round(initial_value, 2)
        
        logger.info(f"Initialized {len(self.machines)} machines with sensors")
    
    def generate_sensor_data(self, machine_id: str = None) -> Dict[str, Dict[str, float]]:
        """
        Generate simulated sensor data for all machines or a specific machine.
        
        Args:
            machine_id: Optional machine ID to generate data for
        
        Returns:
            Dictionary with machine IDs as keys and sensor data as values
        """
        result = {}
        
        # If machine_id is specified, only generate data for that machine
        if machine_id and machine_id in self.machines:
            result[machine_id] = self._generate_machine_data(machine_id)
        else:
            # Generate data for all machines
            for machine_id in self.machines:
                result[machine_id] = self._generate_machine_data(machine_id)
        
        return result
    
    def _generate_machine_data(self, machine_id: str) -> Dict[str, float]:
        """
        Generate simulated sensor data for a specific machine.
        
        Args:
            machine_id: Machine ID to generate data for
        
        Returns:
            Dictionary with sensor types as keys and values as values
        """
        result = {}
        
        # Get machine type
        machine_type = self.machines.get(machine_id)
        
        # Get sensors for this machine
        sensors = self.machine_sensors.get(machine_id, [])
        
        # Update sensor values with some random variation
        for sensor_type in sensors:
            current_value = self.sensor_values[machine_id].get(sensor_type, 0)
            
            # For binary sensors, occasionally change state
            if self.SENSOR_UNITS.get(sensor_type) == "binary":
                # Safety sensors should rarely change to unsafe state
                if sensor_type in [SensorType.EMERGENCY_STOP, SensorType.LIGHT_CURTAIN, 
                                  SensorType.SAFETY_MAT]:
                    if random.random() < 0.01:  # 1% chance of safety issue
                        new_value = 0  # Unsafe state
                    else:
                        new_value = 1  # Safe state
                else:
                    # For other binary sensors, 5% chance of changing state
                    if random.random() < 0.05:
                        new_value = 1 - current_value  # Toggle between 0 and 1
                    else:
                        new_value = current_value
            else:
                # Get normal range for this sensor
                min_val, max_val = self.SENSOR_RANGES.get(sensor_type, (0, 100))
                
                # Add some random variation (±5% of range)
                range_width = max_val - min_val
                variation = (random.random() - 0.5) * 0.05 * range_width
                
                # Calculate new value
                new_value = current_value + variation
                
                # Keep within sensor range
                new_value = max(min_val, min(max_val, new_value))
                
                # Round to 2 decimal places
                new_value = round(new_value, 2)
            
            # Update stored value
            self.sensor_values[machine_id][sensor_type] = new_value
            
            # Add to result with units
            sensor_key = f"{sensor_type}"
            result[sensor_key] = new_value
            
            # Add unit as separate key for ThingsBoard compatibility
            unit = self.SENSOR_UNITS.get(sensor_type, "")
            result[f"{sensor_type}_unit"] = unit
        
        # Add machine type and timestamp
        result["machine_type"] = machine_type
        result["timestamp"] = int(time.time() * 1000)  # milliseconds
        
        return result
    
    def simulate(self, interval: int = 5, duration: int = 60, 
                 thingsboard_config: Dict[str, Any] = None):
        """
        Run a continuous simulation, generating data at specified intervals.
        
        Args:
            interval: Interval between data generations in seconds
            duration: Total duration of simulation in seconds
            thingsboard_config: Configuration for ThingsBoard connection
        """
        tb_connector = None
        
        # Initialize ThingsBoard connector if configuration is provided
        if thingsboard_config:
            try:
                host = thingsboard_config.get("host", "localhost")
                port = thingsboard_config.get("port", 1883)
                https_mode = thingsboard_config.get("https_mode", False)
                multi_device = thingsboard_config.get("multi_device", False)
                
                if multi_device:
                    # Import and use MultiDeviceConnector
                    from src.thingsboard.multi_device_connector import MultiDeviceConnector
                    tokens_file = thingsboard_config.get("tokens_file")
                    
                    tb_connector = MultiDeviceConnector(
                        host=host, 
                        port=port, 
                        tokens_file=tokens_file,
                        https_mode=https_mode
                    )
                    
                    # Connect to MQTT if not in HTTPS mode
                    if not https_mode:
                        tb_connector.connect_mqtt()
                    
                    logger.info(f"Connected to ThingsBoard at {host}:{port} using multiple device tokens")
                else:
                    # Use standard ThingsBoardConnector
                    from src.thingsboard.connector import ThingsBoardConnector
                    access_token = thingsboard_config.get("access_token")
                    
                    tb_connector = ThingsBoardConnector(
                        host=host, 
                        port=port, 
                        access_token=access_token,
                        https_mode=https_mode
                    )
                    
                    # Connect to MQTT if not in HTTPS mode
                    if not https_mode:
                        tb_connector.connect_mqtt()
                    
                    logger.info(f"Connected to ThingsBoard at {host}:{port} using single token")
                
            except Exception as e:
                logger.error(f"Failed to initialize ThingsBoard connector: {e}")
                tb_connector = None
        
        # Calculate number of iterations
        iterations = duration // interval if duration > 0 else float('inf')
        
        abnormal_event_count = {machine_id: 0 for machine_id in self.machines}
        try:
            logger.info(f"Starting simulation with {len(self.machines)} machines...")
            logger.info(f"Sending data every {interval} seconds for {duration} seconds")
            
            iteration_count = 0
            while iteration_count < iterations or duration <= 0:
                start_time = time.time()
                
                # Generate data for all machines
                data = self.generate_sensor_data()

                # Tạo event bất thường: 1% xác suất mỗi vòng lặp
                if random.random() < 0.01:
                    # Tăng xác suất cho máy đã từng bị event
                    machine_ids = list(self.machines.keys())
                    weights = [3 if abnormal_event_count[mid] > 0 else 1 for mid in machine_ids]
                    abnormal_machine_id = random.choices(machine_ids, weights=weights, k=1)[0]
                    sensors = self.machine_sensors[abnormal_machine_id]
                    if sensors:
                        abnormal_sensor = random.choice(sensors)
                        min_val, max_val = self.SENSOR_RANGES.get(abnormal_sensor, (0, 100))
                        abnormal_value = round(max_val * 1.5, 2)  # tăng 50% so với max
                        data[abnormal_machine_id][abnormal_sensor] = abnormal_value
                        abnormal_event_count[abnormal_machine_id] += 1
                        logger.warning(f"[EVENT] Abnormal value injected: {abnormal_machine_id} - {abnormal_sensor} = {abnormal_value} (event #{abnormal_event_count[abnormal_machine_id]})")
                
                # Send data to ThingsBoard
                if tb_connector:
                    for machine_id, machine_data in data.items():
                        tb_connector.send_telemetry(machine_id, machine_data)
                
                # Log progress
                iteration_count += 1
                if iteration_count % 10 == 0:
                    logger.info(f"Completed {iteration_count} iterations")
                
                # Wait for next interval
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user")
        
        finally:
            # Disconnect from ThingsBoard
            if tb_connector and hasattr(tb_connector, 'disconnect_mqtt'):
                tb_connector.disconnect_mqtt()
                logger.info("Disconnected from ThingsBoard")


if __name__ == "__main__":
    # Example usage
    simulator = SensorSimulator()
    
    # ThingsBoard configuration
    tb_config = {
        "host": "localhost",
        "port": 1883,
        "access_token": "YOUR_ACCESS_TOKEN",
        "https_mode": False
    }
    
    # Run simulation for 60 seconds with 5-second intervals
    simulator.simulate(interval=5, duration=60, thingsboard_config=tb_config)
