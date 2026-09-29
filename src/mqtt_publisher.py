import json
import os
import random
import ssl
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

def build_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if os.getenv("MQTT_USE_TLS", "true").lower() == "true":
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    return client

def generate_telemetry():
    voltage = round(random.normalvariate(230, 2), 2)
    current = round(random.normalvariate(8, 1), 2)
    power_factor = round(min(0.99, max(0.75, random.normalvariate(0.94, 0.025))), 3)
    power = round(voltage * current * power_factor / 1000, 3)
    return {
        "device_id": os.getenv("DEVICE_ID", "ESP32-ENERGY-001"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "voltage": voltage,
        "current": current,
        "power_kw": power,
        "power_factor": power_factor,
        "temperature": round(random.normalvariate(34, 2), 2),
    }

def main():
    host = os.environ["MQTT_BROKER_HOST"]
    port = int(os.getenv("MQTT_BROKER_PORT", "8883"))
    client = build_client()
    client.username_pw_set(os.environ["MQTT_USERNAME"], os.environ["MQTT_PASSWORD"])
    client.connect(host, port, keepalive=60)
    client.loop_start()
    topic = os.getenv("MQTT_TELEMETRY_TOPIC", "factory/energy/telemetry")
    try:
        while True:
            payload = json.dumps(generate_telemetry())
            client.publish(topic, payload, qos=1)
            print(payload)
            time.sleep(5)
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
