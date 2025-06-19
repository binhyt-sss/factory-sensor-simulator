from src.thingsboard.sensor_type import SensorType

class MachineType:
    
    MIXER = "MIXER"
    CNC_MACHINE = "CNC_MACHINE"
    HYDRAULIC_PRESS = "HYDRAULIC_PRESS"
    CONVEYOR_SYSTEM = "CONVEYOR_SYSTEM"
    PUMP_SYSTEM = "PUMP_SYSTEM"

    MACHINE_SENSORS = {
        MIXER: [
            # Temperature sensors
            SensorType.RTD_PT100,
            SensorType.THERMOCOUPLE_K_TYPE,
            SensorType.INFRARED_TEMP,
            # Vibration/Motion sensors
            SensorType.PIEZOELECTRIC_ACCELEROMETER,
            SensorType.ROTARY_ENCODER,
            SensorType.GYROSCOPE,
            # Audio sensor
            SensorType.INDUSTRIAL_MICROPHONE,
            # Level sensors
            SensorType.CAPACITIVE_LEVEL,
            SensorType.ULTRASONIC_LEVEL,
            # Power monitoring
            SensorType.CURRENT_TRANSFORMER,
            SensorType.POWER_METER
        ],
        CNC_MACHINE: [
            # Temperature sensors
            SensorType.RTD_PT100,
            SensorType.THERMOCOUPLE_J_TYPE,
            SensorType.THERMAL_IMAGING,
            # Vibration sensors
            SensorType.MEMS_ACCELEROMETER,
            SensorType.PROXIMITY_PROBE,
            SensorType.STRAIN_GAUGE,
            # Position sensors
            SensorType.LINEAR_ENCODER,
            SensorType.ABSOLUTE_ENCODER,
            SensorType.LVDT,
            # Pressure/Flow sensors
            SensorType.PRESSURE_TRANSDUCER,
            SensorType.ELECTROMAGNETIC_FLOW,
            SensorType.DIFFERENTIAL_PRESSURE,
            # Level sensors
            SensorType.FLOAT_LEVEL_SWITCH,
            SensorType.CAPACITIVE_LEVEL,
            # Optical sensors
            SensorType.LASER_DISTANCE,
            SensorType.PHOTOELECTRIC,
            # Audio sensor
            SensorType.ACOUSTIC_EMISSION
        ],
        HYDRAULIC_PRESS: [
            # Pressure sensors
            SensorType.STRAIN_GAUGE_PRESSURE,
            SensorType.PIEZOELECTRIC_PRESSURE,
            SensorType.BOURDON_TUBE_GAUGE,
            # Temperature sensors
            SensorType.RTD_PT100,
            SensorType.THERMISTOR,
            SensorType.BIMETALLIC_TEMP_SWITCH,
            # Position sensors
            SensorType.LVDT,
            SensorType.MAGNETOSTRICTIVE_POSITION,
            SensorType.LIMIT_SWITCH,
            # Force/Load sensors
            SensorType.LOAD_CELL,
            SensorType.STRAIN_GAUGE,
            SensorType.PIEZOELECTRIC_FORCE,
            # Vibration sensors
            SensorType.INDUSTRIAL_ACCELEROMETER,
            SensorType.VELOCITY_SENSOR
        ],
        CONVEYOR_SYSTEM: [
            # Speed/Motion sensors
            SensorType.TACHOMETER,
            SensorType.HALL_EFFECT,
            SensorType.INCREMENTAL_ENCODER,
            # Detection sensors
            SensorType.PHOTOELECTRIC,
            SensorType.INDUCTIVE_PROXIMITY,
            SensorType.LASER_SCANNER,
            SensorType.ULTRASONIC_SENSOR,
            # Load/Weight sensors
            SensorType.BELT_SCALE_LOAD_CELL,
            SensorType.STRAIN_GAUGE,
            # Safety sensors
            SensorType.EMERGENCY_STOP,
            SensorType.LIGHT_CURTAIN,
            SensorType.SAFETY_MAT
        ],
        PUMP_SYSTEM: [
            # Flow sensors
            SensorType.ELECTROMAGNETIC_FLOW,
            SensorType.TURBINE_FLOW,
            SensorType.ULTRASONIC_FLOW,
            # Pressure sensors
            SensorType.BOURDON_PRESSURE_GAUGE,
            SensorType.DIAPHRAGM_PRESSURE,
            SensorType.DIFFERENTIAL_PRESSURE,
            # Level sensors
            SensorType.RADAR_LEVEL,
            SensorType.HYDROSTATIC_LEVEL,
            SensorType.FLOAT_LEVEL_SWITCH,
            # Temperature sensors
            SensorType.RTD_PT100,
            # Vibration sensors
            SensorType.MEMS_ACCELEROMETER,
            SensorType.PROXIMITY_PROBE
        ]
    } 