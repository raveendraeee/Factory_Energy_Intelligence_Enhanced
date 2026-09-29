from pathlib import Path
from datetime import datetime, timedelta, timezone
import random
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "cloud_demo"
MODEL = ROOT / "models" / "isolation_forest.joblib"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    random.seed(42)
    rows = []
    start = datetime(2026, 9, 25, 8, 0, tzinfo=timezone.utc)
    for i in range(240):
        anomaly = i in {25, 61, 97, 133, 171, 210}
        voltage = random.gauss(230, 2)
        current = random.gauss(8, 0.7)
        temp = random.gauss(34, 1.8)
        pf = random.gauss(0.94, 0.02)
        if anomaly:
            kind = i % 3
            if kind == 0:
                current += 8
            elif kind == 1:
                temp += 18
            else:
                voltage += 35
        power = voltage * current * pf / 1000
        rows.append({
            "id": i + 1,
            "device_id": "DEMO-FACTORY-001",
            "timestamp": (start + timedelta(minutes=5*i)).isoformat(),
            "voltage": round(voltage, 2),
            "current": round(current, 2),
            "power_kw": round(power, 3),
            "power_factor": round(pf, 3),
            "temperature": round(temp, 2),
            "injected_anomaly": int(anomaly),
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "telemetry.csv", index=False)

    features = df[["voltage","current","power_kw","power_factor","temperature"]]
    normal = features[df["injected_anomaly"] == 0]
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(normal)
    pred = model.predict(features)
    score = model.decision_function(features)
    anomalies = df.loc[pred == -1, ["id","device_id","timestamp"]].copy()
    anomalies["telemetry_id"] = anomalies["id"]
    anomalies["prediction"] = "ANOMALY"
    anomalies["anomaly_score"] = score[pred == -1]
    anomalies.to_csv(OUT / "anomalies.csv", index=False)
    MODEL.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL)
    print(f"Generated {len(df)} telemetry records and {len(anomalies)} anomaly events.")

if __name__ == "__main__":
    main()
