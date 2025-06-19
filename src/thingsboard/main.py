import argparse
import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

from src.thingsboard.simulator import SensorSimulator, MachineType
from src.thingsboard.multi_device_connector import MultiDeviceConnector

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SensorSimulation")

def main():
    """Main function to run the sensor simulator."""
    # Load environment variables from .env file if present
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Virtual Sensor Simulator for ThingsBoard')
    
    parser.add_argument('--host', type=str, default=os.getenv('TB_HOST', 'localhost'),
                        help='ThingsBoard host address')
    parser.add_argument('--port', type=int, default=int(os.getenv('TB_PORT', '1883')),
                        help='ThingsBoard port (default: 1883 for MQTT, 8080 for HTTP)')
    parser.add_argument('--token', type=str, default=os.getenv('TB_ACCESS_TOKEN'),
                        help='Device access token for ThingsBoard (used as default if tokens-file not provided)')
    parser.add_argument('--tokens-file', type=str, default=os.getenv('TB_TOKENS_FILE'),
                        help='Path to JSON file containing device_id to token mappings')
    parser.add_argument('--https', action='store_true', default=os.getenv('TB_HTTPS', 'false').lower() == 'true',
                        help='Use HTTPS instead of MQTT protocol')
    parser.add_argument('--interval', type=int, default=int(os.getenv('SIMULATION_INTERVAL', '5')),
                        help='Interval between data generations in seconds')
    parser.add_argument('--duration', type=int, default=0,
                        help='Total duration of simulation in seconds (0 for infinite, Ctrl+C to stop)')
    parser.add_argument('--mixers', type=int, default=int(os.getenv('MIXER_COUNT', '5')),
                        help='Number of mixer machines to simulate')
    parser.add_argument('--cnc', type=int, default=int(os.getenv('CNC_COUNT', '10')),
                        help='Number of CNC machines to simulate')
    parser.add_argument('--hydraulic', type=int, default=int(os.getenv('HYDRAULIC_COUNT', '7')),
                        help='Number of hydraulic presses to simulate')
    parser.add_argument('--conveyor', type=int, default=int(os.getenv('CONVEYOR_COUNT', '8')),
                        help='Number of conveyor systems to simulate')
    parser.add_argument('--pump', type=int, default=int(os.getenv('PUMP_COUNT', '6')),
                        help='Number of pump systems to simulate')
    parser.add_argument('--local-only', action='store_true', 
                        help='Only save data locally, do not connect to ThingsBoard')
    parser.add_argument('--save-local', action='store_true',
                        help='Save generated data to local JSON files (default: do not save)')
    
    args = parser.parse_args()
    
    # Configure machine count
    machine_count = {
        MachineType.MIXER: args.mixers,
        MachineType.CNC_MACHINE: args.cnc,
        MachineType.HYDRAULIC_PRESS: args.hydraulic,
        MachineType.CONVEYOR_SYSTEM: args.conveyor,
        MachineType.PUMP_SYSTEM: args.pump
    }
    
    # Log configuration
    logger.info("Starting sensor simulation with the following configuration:")
    logger.info(f"ThingsBoard Host: {args.host}:{args.port}")
    logger.info(f"Protocol: {'HTTPS' if args.https else 'MQTT'}")
    if args.tokens_file:
        logger.info(f"Using device tokens from file: {args.tokens_file}")
    logger.info(f"Simulation Interval: {args.interval} seconds")
    logger.info(f"Simulation Duration: {'Infinite' if args.duration <= 0 else f'{args.duration} seconds'}")
    logger.info(f"Machine Count: {sum(machine_count.values())} machines")
    
    # Create sensor simulator
    simulator = SensorSimulator(machine_count)
    
    # Set up ThingsBoard configuration
    if args.local_only:
        logger.info("Running in local-only mode (no ThingsBoard connection)")
        tb_config = None
    elif args.tokens_file:
        logger.info(f"Using multi-device mode with tokens from: {args.tokens_file}")
        tb_config = {
            "host": args.host,
            "port": args.port,
            "tokens_file": args.tokens_file,
            "https_mode": args.https,
            "multi_device": True
        }
    elif args.token:
        logger.info("Using single-token mode")
        tb_config = {
            "host": args.host,
            "port": args.port,
            "access_token": args.token,
            "https_mode": args.https,
            "multi_device": False
        }
    else:
        logger.info("No token provided, running in local-only mode")
        tb_config = None
    
    # Run simulation
    simulator.simulate(interval=args.interval, duration=args.duration, thingsboard_config=tb_config)


if __name__ == "__main__":
    main()
