import json
import os
import ssl

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from .database import insert_anomaly_event, insert_telemetry
from .prediction_service import predict_telemetry

load_dotenv()

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    client.username_pw_set(os.environ["MQTT_USERNAME"], os.environ["MQTT_PASSWORD"])

    def on_connect(client, userdata, flags, reason_code, properties):
        print("MQTT connected:", reason_code)
        client.subscribe(os.getenv(
            "MQTT_TELEMETRY_TOPIC", "factory/energy/telemetry"
        ), qos=1)

    def on_message(client, userdata, msg):
        try:
            record = json.loads(msg.payload.decode())
            telemetry_id = insert_telemetry(record)
            result = predict_telemetry(record)
            insert_anomaly_event(
                telemetry_id, record, result["prediction"], result["anomaly_score"]
            )
            print(result)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            print("Telemetry processing error:", error)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(
        os.environ["MQTT_BROKER_HOST"],
        int(os.getenv("MQTT_BROKER_PORT", "8883")),
        keepalive=60,
    )
    client.loop_forever()

if __name__ == "__main__":
    main()
