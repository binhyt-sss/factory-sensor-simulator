import json
import logging
import time
import os
from datetime import datetime
import requests
import paho.mqtt.client as mqtt
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MultiDeviceConnector:
    """
    Class to handle connections to ThingsBoard for multiple devices with different tokens.
    """
    
    def __init__(self, host, port=1883, tokens_file=None, https_mode=False):
        """
        Initialize ThingsBoard multi-device connector.
        
        Args:
            host (str): ThingsBoard host address
            port (int): MQTT port (default 1883)
            tokens_file (str): Path to JSON file containing device_id to token mappings
            https_mode (bool): If True, use HTTPS instead of MQTT
        """
        self.host = host
        self.port = port
        self.https_mode = https_mode
        self.device_tokens = {}
        self.mqtt_clients = {}
        
        # Load device tokens from file if provided
        if tokens_file and os.path.exists(tokens_file):
            self._load_tokens(tokens_file)
    
    def _load_tokens(self, tokens_file):
        """Load device tokens from JSON file."""
        try:
            with open(tokens_file, 'r') as f:
                self.device_tokens = json.load(f)
            logger.info(f"Loaded {len(self.device_tokens)} device tokens from {tokens_file}")
        except Exception as e:
            logger.error(f"Failed to load tokens from {tokens_file}: {e}")
    
    def add_device_token(self, device_id, token):
        """Add or update a device token."""
        self.device_tokens[device_id] = token
        # Initialize MQTT client for this device if not in HTTPS mode
        if not self.https_mode:
            self._init_mqtt_client(device_id)
    
    def _init_mqtt_client(self, device_id):
        """Initialize MQTT client for a specific device."""
        if device_id not in self.device_tokens:
            logger.error(f"No token found for device {device_id}")
            return
        
        token = self.device_tokens[device_id]
        client = mqtt.Client()
        client.username_pw_set(token)
        self.mqtt_clients[device_id] = client
    
    def connect_mqtt(self):
        """Connect all devices to ThingsBoard via MQTT."""
        if self.https_mode:
            logger.info("HTTPS mode enabled, skipping MQTT connections")
            return True
        
        success = True
        for device_id, token in self.device_tokens.items():
            if device_id not in self.mqtt_clients:
                self._init_mqtt_client(device_id)
            
            client = self.mqtt_clients.get(device_id)
            if not client:
                continue
                
            try:
                client.connect(self.host, self.port, 60)
                client.loop_start()
                logger.info(f"Connected device {device_id} to ThingsBoard at {self.host}:{self.port}")
            except Exception as e:
                logger.error(f"Failed to connect device {device_id} to ThingsBoard: {e}")
                success = False
        
        return success
    
    def disconnect_mqtt(self):
        """Disconnect all devices from ThingsBoard MQTT."""
        for device_id, client in self.mqtt_clients.items():
            try:
                client.loop_stop()
                client.disconnect()
            except Exception as e:
                logger.error(f"Error disconnecting device {device_id}: {e}")
        
        logger.info("Disconnected all devices from ThingsBoard MQTT")
    
    def send_telemetry(self, device_id, telemetry_data, timestamp=None):
        """
        Send telemetry data to ThingsBoard for a specific device.
        
        Args:
            device_id (str): Device identifier
            telemetry_data (dict): Telemetry data to send
            timestamp (int, optional): Timestamp in milliseconds
        
        Returns:
            bool: True if successful, False otherwise
        """
        if device_id not in self.device_tokens:
            logger.warning(f"No token found for device {device_id}, skipping telemetry")
            return False
            
        if timestamp is None:
            timestamp = int(time.time() * 1000)  # Convert to milliseconds
            
        # Add timestamp to telemetry data
        payload = {
            "ts": timestamp,
            "values": telemetry_data
        }
        
        if self.https_mode:
            return self._send_via_https(device_id, payload)
        else:
            return self._send_via_mqtt(device_id, payload)
    
    def _send_via_mqtt(self, device_id, payload):
        """Send data via MQTT protocol for a specific device."""
        client = self.mqtt_clients.get(device_id)
        if not client:
            logger.error(f"MQTT client not initialized for device {device_id}")
            return False
        try:
            # Convert payload to JSON string
            payload_json = json.dumps(payload)
            # Send to ThingsBoard
            result = client.publish('v1/devices/me/telemetry', payload_json, 1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Data sent successfully for device {device_id} via MQTT")
                return True
            else:
                logger.error(f"Failed to send data for device {device_id} via MQTT. Result code: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Error sending data for device {device_id} via MQTT: {e}")
            return False
    
    def _send_via_https(self, device_id, payload):
        """Send data via HTTPS protocol for a specific device."""
        token = self.device_tokens.get(device_id)
        if not token:
            logger.error(f"No token found for device {device_id}")
            return False
        
        try:
            # ThingsBoard REST API endpoint
            url = f"http://{self.host}:{self.port}/api/v1/{token}/telemetry"
            
            # Send request
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                logger.debug(f"Data sent successfully for device {device_id} via HTTPS")
                return True
            else:
                logger.error(f"Failed to send data for device {device_id} via HTTPS. Status code: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error sending data for device {device_id} via HTTPS: {e}")
            return False
