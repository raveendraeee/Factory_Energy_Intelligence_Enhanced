import json
from pathlib import Path

from src.mqtt_publisher import generate_telemetry

Path("data/sample").mkdir(parents=True, exist_ok=True)
with open("data/sample/telemetry.jsonl", "w", encoding="utf-8") as f:
    for _ in range(1000):
        f.write(json.dumps(generate_telemetry()) + "\n")
print("Generated data/sample/telemetry.jsonl")
