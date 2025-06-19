import json
import logging
import time
from datetime import datetime
import requests
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class ThingsBoardConnector:
    
    def __init__(self, host, port=1883, access_token=None, https_mode=False):
        self.host = host
        self.port = port
        self.access_token = access_token
        self.https_mode = https_mode
        self.mqtt_client = None
        
        if not https_mode and access_token:
            # Initialize MQTT client
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.username_pw_set(access_token)
    
    def connect_mqtt(self):
        if not self.mqtt_client:
            logger.error("MQTT client not initialized. Check if access token is provided.")
            return False
        
        try:
            self.mqtt_client.connect(self.host, self.port, 60)
            self.mqtt_client.loop_start()
            logger.info(f"Connected to ThingsBoard at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to ThingsBoard: {e}")
            return False
    
    def disconnect_mqtt(self):
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            logger.info("Disconnected from ThingsBoard MQTT")
    
    def send_telemetry(self, device_id, telemetry_data, timestamp=None):

        if timestamp is None:
            timestamp = int(time.time() * 1000)  # Convert to milliseconds
            
        # Add timestamp to telemetry data
        payload = {
            "ts": timestamp,
            "values": telemetry_data
        }
        
        # Save data locally for debugging/backup
        self._save_data_locally(device_id, payload)
        
        if self.https_mode:
            return self._send_via_https(device_id, payload)
        else:
            return self._send_via_mqtt(payload)
    
    def _send_via_mqtt(self, payload):
        if not self.mqtt_client:
            logger.error("MQTT client not initialized.")
            return False
        
        try:
            # Convert payload to JSON string
            payload_json = json.dumps(payload)
            # Send to ThingsBoard
            result = self.mqtt_client.publish('v1/devices/me/telemetry', payload_json, 1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug("Data sent successfully via MQTT")
                return True
            else:
                logger.error(f"Failed to send data via MQTT. Result code: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Error sending data via MQTT: {e}")
            return False
    
    def _send_via_https(self, device_id, payload):
        if not self.access_token:
            logger.error("Access token not provided for HTTPS connection.")
            return False
        
        try:            # ThingsBoard REST API endpoint
            url = f"http://{self.host}:{self.port}/api/v1/{self.access_token}/telemetry"
            
            # Send request
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                logger.debug("Data sent successfully via HTTPS")
                return True
            else:
                logger.error(f"Failed to send data via HTTPS. Status code: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error sending data via HTTPS: {e}")
            return False
    
    def _save_data_locally(self, device_id, payload):
        try:
            # Create a timestamp-based filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulation_data/sensor_data_{timestamp}.json"
            
            # Append device_id to the payload
            payload_with_device = payload.copy()
            payload_with_device["device_id"] = device_id
            
            # Save as JSON file
            with open(filename, 'w') as f:
                json.dump(payload_with_device, f, indent=2)
                
            logger.debug(f"Data saved locally to {filename}")
        except Exception as e:
            logger.error(f"Error saving data locally: {e}")
