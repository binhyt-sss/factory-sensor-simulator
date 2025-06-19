import json
import logging
import random
import time
from datetime import datetime
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class VirtualSensor:
    """Base class for virtual sensors."""
    
    def __init__(self, sensor_id: str, sensor_type: str, min_value: float, max_value: float, unit: str):
        """
        Initialize a virtual sensor.
        
        Args:
            sensor_id: Unique identifier for the sensor
            sensor_type: Type of sensor
            min_value: Minimum value for the sensor
            max_value: Maximum value for the sensor
            unit: Unit of measurement
        """
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.current_value = self._generate_initial_value()
    
    def _generate_initial_value(self) -> float:
        """Generate an initial value for the sensor."""
        return random.uniform(self.min_value, self.max_value)
    
    def get_reading(self) -> Dict:
        """Get a sensor reading."""
        # Update current value with some randomness
        drift = random.uniform(-0.05, 0.05)  # 5% drift
        self.current_value = self.current_value * (1 + drift)
        
        # Ensure value stays within bounds
        self.current_value = max(min(self.current_value, self.max_value), self.min_value)
        
        return {
            "sensor_id": self.sensor_id,
            "type": self.sensor_type,
            "value": round(self.current_value, 2),
            "unit": self.unit,
            "timestamp": int(time.time() * 1000)
        }

class MachineSimulator:
    """Base class for machine simulators."""
    
    def __init__(self, machine_id: str, machine_type: str):
        """
        Initialize a machine simulator.
        
        Args:
            machine_id: Unique identifier for the machine
            machine_type: Type of machine
        """
        self.machine_id = machine_id
        self.machine_type = machine_type
        self.sensors: List[VirtualSensor] = []
        self.operational_status = True
        self.maintenance_mode = False
        self.operational_hours = random.uniform(1000, 50000)
        self.installation_date = datetime(
            random.randint(2018, 2025), 
            random.randint(1, 12), 
            random.randint(1, 28)
        )
    
    def add_sensor(self, sensor: VirtualSensor) -> None:
        """Add a sensor to the machine."""
        self.sensors.append(sensor)
    
    def get_telemetry(self) -> Dict:
        """Get telemetry data from all sensors."""
        telemetry = {
            "machine_id": self.machine_id,
            "machine_type": self.machine_type,
            "operational_status": self.operational_status,
            "maintenance_mode": self.maintenance_mode,
            "operational_hours": round(self.operational_hours, 2),
            "installation_date": self.installation_date.strftime("%Y-%m-%d"),
            "sensors": {}
        }
        
        # Add sensor readings
        for sensor in self.sensors:
            reading = sensor.get_reading()
            telemetry["sensors"][sensor.sensor_id] = {
                "value": reading["value"],
                "unit": reading["unit"]
            }
        
        return telemetry

class MixerMachine(MachineSimulator):
    """Simulator for a mixer machine."""
    
    def __init__(self, machine_id: str):
        """Initialize a mixer machine simulator."""
        super().__init__(machine_id, "MIXER")
        
        # Add temperature sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_rtd", "RTD_PT100", 20, 100, "°C"))
        self.add_sensor(VirtualSensor(f"{machine_id}_thermocouple", "Thermocouple_K_Type", 20, 100, "°C"))
        self.add_sensor(VirtualSensor(f"{machine_id}_infrared", "Infrared_Temperature", 25, 95, "°C"))
        
        # Add vibration/motion sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_piezo", "Piezoelectric_Accelerometer", 0, 25, "mm/s"))
        self.add_sensor(VirtualSensor(f"{machine_id}_encoder", "Rotary_Encoder", 0, 1000, "RPM"))
        self.add_sensor(VirtualSensor(f"{machine_id}_gyro", "Gyroscope", -10, 10, "deg/s"))
        
        # Add audio sensor
        self.add_sensor(VirtualSensor(f"{machine_id}_mic", "Industrial_Microphone", 60, 95, "dB"))
        
        # Add level sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_cap_level", "Capacitive_Level", 0, 100, "%"))
        self.add_sensor(VirtualSensor(f"{machine_id}_ultra_level", "Ultrasonic_Level", 0, 100, "%"))
        
        # Add power monitoring
        self.add_sensor(VirtualSensor(f"{machine_id}_current", "Current_Transformer", 0, 100, "A"))
        self.add_sensor(VirtualSensor(f"{machine_id}_power", "Power_Meter", 0, 200, "kW"))

class CncMachine(MachineSimulator):
    """Simulator for a CNC machine."""
    
    def __init__(self, machine_id: str):
        """Initialize a CNC machine simulator."""
        super().__init__(machine_id, "CNC_MACHINE")
        
        # Add temperature sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_rtd", "RTD_PT100", 20, 90, "°C"))
        self.add_sensor(VirtualSensor(f"{machine_id}_thermocouple", "Thermocouple_J_Type", 20, 90, "°C"))
        self.add_sensor(VirtualSensor(f"{machine_id}_thermal", "Thermal_Imaging", 25, 85, "°C"))
        
        # Add vibration sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_mems", "MEMS_Accelerometer", 0, 20, "mm/s"))
        self.add_sensor(VirtualSensor(f"{machine_id}_proximity", "Proximity_Probe", 0, 10, "mm"))
        self.add_sensor(VirtualSensor(f"{machine_id}_strain", "Strain_Gauge", 0, 1000, "μm/m"))
        
        # Add position sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_linear", "Linear_Encoder", 0, 1000, "mm"))
        self.add_sensor(VirtualSensor(f"{machine_id}_absolute", "Absolute_Encoder", 0, 360, "deg"))
        self.add_sensor(VirtualSensor(f"{machine_id}_lvdt", "LVDT", -10, 10, "mm"))
        
        # Add pressure/flow sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_pressure", "Pressure_Transducer", 0, 100, "bar"))
        self.add_sensor(VirtualSensor(f"{machine_id}_flow", "Electromagnetic_Flow", 0, 50, "L/min"))
        self.add_sensor(VirtualSensor(f"{machine_id}_diff_pressure", "Differential_Pressure", -10, 10, "bar"))
        
        # Add level sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_float", "Float_Level_Switch", 0, 100, "%"))
        self.add_sensor(VirtualSensor(f"{machine_id}_cap_level", "Capacitive_Level", 0, 100, "%"))
        
        # Add optical sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_laser", "Laser_Distance", 0, 1000, "mm"))
        self.add_sensor(VirtualSensor(f"{machine_id}_photoelectric", "Photoelectric", 0, 1, "binary"))
        
        # Add audio sensor
        self.add_sensor(VirtualSensor(f"{machine_id}_acoustic", "Acoustic_Emission", 70, 95, "dB"))

class HydraulicPress(MachineSimulator):
    """Simulator for a hydraulic press."""
    
    def __init__(self, machine_id: str):
        """Initialize a hydraulic press simulator."""
        super().__init__(machine_id, "HYDRAULIC_PRESS")
        
        # Add pressure sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_strain_pressure", "Strain_Gauge_Pressure", 0, 300, "bar"))
        self.add_sensor(VirtualSensor(f"{machine_id}_piezo_pressure", "Piezoelectric_Pressure", 0, 300, "bar"))
        self.add_sensor(VirtualSensor(f"{machine_id}_bourdon", "Bourdon_Tube_Gauge", 0, 300, "bar"))
        
        # Add temperature sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_rtd", "RTD_PT100", 20, 80, "°C"))
        self.add_sensor(VirtualSensor(f"{machine_id}_thermistor", "Thermistor", 20, 80, "°C"))
        self.add_sensor(VirtualSensor(f"{machine_id}_bimetallic", "Bimetallic_Temperature", 20, 80, "°C"))
        
        # Add position sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_lvdt", "LVDT", 0, 500, "mm"))
        self.add_sensor(VirtualSensor(f"{machine_id}_magnetostrictive", "Magnetostrictive_Position", 0, 500, "mm"))
        self.add_sensor(VirtualSensor(f"{machine_id}_limit", "Limit_Switch", 0, 1, "binary"))
        
        # Add force/load sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_load_cell", "Load_Cell", 0, 50000, "kg"))
        self.add_sensor(VirtualSensor(f"{machine_id}_strain", "Strain_Gauge", 0, 1000, "μm/m"))
        self.add_sensor(VirtualSensor(f"{machine_id}_piezo_force", "Piezoelectric_Force", 0, 50000, "N"))
        
        # Add vibration sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_accelerometer", "Industrial_Accelerometer", 0, 30, "mm/s"))
        self.add_sensor(VirtualSensor(f"{machine_id}_velocity", "Velocity_Sensor", 0, 100, "mm/s"))

class ConveyorSystem(MachineSimulator):
    """Simulator for a conveyor system."""
    
    def __init__(self, machine_id: str):
        """Initialize a conveyor system simulator."""
        super().__init__(machine_id, "CONVEYOR_SYSTEM")
        
        # Add speed/motion sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_tacho", "Tachometer_Generator", 0, 300, "RPM"))
        self.add_sensor(VirtualSensor(f"{machine_id}_hall", "Hall_Effect", 0, 300, "RPM"))
        self.add_sensor(VirtualSensor(f"{machine_id}_encoder", "Incremental_Encoder", 0, 300, "RPM"))
        
        # Add detection sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_photoelectric", "Photoelectric", 0, 1, "binary"))
        self.add_sensor(VirtualSensor(f"{machine_id}_inductive", "Inductive_Proximity", 0, 1, "binary"))
        self.add_sensor(VirtualSensor(f"{machine_id}_laser", "Laser_Scanner", 0, 1000, "mm"))
        self.add_sensor(VirtualSensor(f"{machine_id}_ultrasonic", "Ultrasonic", 0, 1000, "mm"))
        
        # Add load/weight sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_belt_scale", "Belt_Scale_Load_Cell", 0, 5000, "kg"))
        self.add_sensor(VirtualSensor(f"{machine_id}_strain", "Strain_Gauge", 0, 1000, "μm/m"))
        
        # Add safety sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_emergency", "Emergency_Stop", 0, 1, "binary"))
        self.add_sensor(VirtualSensor(f"{machine_id}_light_curtain", "Light_Curtain", 0, 1, "binary"))
        self.add_sensor(VirtualSensor(f"{machine_id}_safety_mat", "Safety_Mat", 0, 1, "binary"))

class PumpSystem(MachineSimulator):
    """Simulator for a pump system."""
    
    def __init__(self, machine_id: str):
        """Initialize a pump system simulator."""
        super().__init__(machine_id, "PUMP_SYSTEM")
        
        # Add flow sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_electromagnetic", "Electromagnetic_Flow", 0, 100, "L/min"))
        self.add_sensor(VirtualSensor(f"{machine_id}_turbine", "Turbine_Flow", 0, 100, "L/min"))
        self.add_sensor(VirtualSensor(f"{machine_id}_ultrasonic", "Ultrasonic_Flow", 0, 100, "L/min"))
        
        # Add pressure sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_bourdon", "Bourdon_Pressure", 0, 10, "bar"))
        self.add_sensor(VirtualSensor(f"{machine_id}_diaphragm", "Diaphragm_Pressure", 0, 10, "bar"))
        self.add_sensor(VirtualSensor(f"{machine_id}_differential", "Differential_Pressure", -1, 1, "bar"))
        
        # Add level sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_radar", "Radar_Level", 0, 100, "%"))
        self.add_sensor(VirtualSensor(f"{machine_id}_hydrostatic", "Hydrostatic_Level", 0, 100, "%"))
        self.add_sensor(VirtualSensor(f"{machine_id}_float", "Float_Level_Switch", 0, 1, "binary"))
        
        # Add temperature sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_rtd", "RTD_PT100", 20, 60, "°C"))
        self.add_sensor(VirtualSensor(f"{machine_id}_thermowell", "Thermowell", 20, 60, "°C"))
        
        # Add vibration sensors
        self.add_sensor(VirtualSensor(f"{machine_id}_accelerometer", "Accelerometer", 0, 20, "mm/s"))
        self.add_sensor(VirtualSensor(f"{machine_id}_proximity", "Proximity_Probe", 0, 10, "mm"))

class MachineSimulationFactory:
    """Factory class to create machine simulators."""
    
    @staticmethod
    def create_machine(machine_type: str, machine_id: str) -> Optional[MachineSimulator]:
        """
        Create a machine simulator of the specified type.
        
        Args:
            machine_type: Type of machine to create
            machine_id: Unique identifier for the machine
            
        Returns:
            MachineSimulator: Machine simulator instance
        """
        machine_map = {
            "MIXER": MixerMachine,
            "CNC_MACHINE": CncMachine,
            "HYDRAULIC_PRESS": HydraulicPress,
            "CONVEYOR_SYSTEM": ConveyorSystem,
            "PUMP_SYSTEM": PumpSystem
        }
        
        if machine_type in machine_map:
            return machine_map[machine_type](machine_id)
        else:
            logger.error(f"Unknown machine type: {machine_type}")
            return None

class VirtualSensorSimulator:
    """
    Class to simulate multiple machines with sensors and send data to ThingsBoard.
    """
    
    def __init__(self, thingsboard_connector=None):
        """
        Initialize the virtual sensor simulator.
        
        Args:
            thingsboard_connector: ThingsBoardConnector instance
        """
        self.machines: List[MachineSimulator] = []
        self.thingsboard_connector = thingsboard_connector
    
    def add_machine(self, machine: MachineSimulator) -> None:
        """Add a machine to the simulator."""
        self.machines.append(machine)
    
    def generate_machine_id(self, prefix: str, index: int) -> str:
        """Generate a unique machine ID."""
        return f"{prefix}_{index:06d}"
    
    def create_machines(self, counts: Dict[str, int]) -> None:
        """
        Create machines of various types.
        
        Args:
            counts: Dictionary mapping machine types to counts
        """
        for machine_type, count in counts.items():
            for i in range(count):
                machine_id = self.generate_machine_id(machine_type, i)
                machine = MachineSimulationFactory.create_machine(machine_type, machine_id)
                if machine:
                    self.add_machine(machine)
        
        logger.info(f"Created {len(self.machines)} virtual machines")
    
    def simulate_cycle(self) -> List[Dict]:
        """
        Simulate one cycle of all machines.
        
        Returns:
            List of telemetry data from all machines
        """
        telemetry_data = []
        
        for machine in self.machines:
            # Get telemetry data from the machine
            telemetry = machine.get_telemetry()
            telemetry_data.append(telemetry)
            
            # Send to ThingsBoard if connector is available
            if self.thingsboard_connector:
                self.thingsboard_connector.send_telemetry(
                    machine.machine_id, 
                    {"sensors": telemetry["sensors"]}
                )
        
        return telemetry_data
    
    def simulate_continuous(self, interval_seconds: float, duration_seconds: Optional[float] = None) -> None:
        """
        Continuously simulate machines and send data.
        
        Args:
            interval_seconds: Interval between simulation cycles in seconds
            duration_seconds: Total duration of simulation in seconds, or None for infinite
        """
        start_time = time.time()
        cycle_count = 0
        
        try:
            logger.info("Starting continuous simulation...")
            
            while True:
                cycle_start = time.time()
                
                # Simulate one cycle
                self.simulate_cycle()
                cycle_count += 1
                
                # Check if duration is reached
                elapsed = time.time() - start_time
                if duration_seconds and elapsed >= duration_seconds:
                    logger.info(f"Simulation completed after {elapsed:.2f} seconds ({cycle_count} cycles)")
                    break
                
                # Sleep for remaining time in the interval
                cycle_time = time.time() - cycle_start
                sleep_time = max(0, interval_seconds - cycle_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
                if cycle_count % 10 == 0:
                    logger.info(f"Completed {cycle_count} simulation cycles")
        
        except KeyboardInterrupt:
            logger.info(f"Simulation stopped after {cycle_count} cycles")
        
        finally:
            if self.thingsboard_connector:
                # Disconnect from ThingsBoard
                if hasattr(self.thingsboard_connector, 'disconnect_mqtt'):
                    self.thingsboard_connector.disconnect_mqtt()
    
    def save_simulation_data(self, data: List[Dict], filename: Optional[str] = None) -> None:
        """
        Save simulation data to a file.
        
        Args:
            data: List of telemetry data from machines
            filename: Filename to save to, or None for timestamp-based name
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulation_data/virtual_sensor_data_{timestamp}.json"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save data to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved simulation data to {filename}")
