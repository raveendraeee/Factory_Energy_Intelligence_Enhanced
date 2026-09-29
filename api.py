from pathlib import Path

import pandas as pd
from fastapi import FastAPI

app = FastAPI(title="Factory Energy Intelligence API", version="1.6.0")
DATA = Path("data/cloud_demo")

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.6.0"}

@app.get("/telemetry/summary")
def telemetry_summary():
    df = pd.read_csv(DATA / "telemetry.csv")
    return {
        "records": int(len(df)),
        "avg_power_kw": float(df["power_kw"].mean()),
        "peak_power_kw": float(df["power_kw"].max()),
        "avg_temperature_c": float(df["temperature"].mean()),
    }

@app.get("/anomalies")
def anomalies():
    path = DATA / "anomalies.csv"
    if not path.exists():
        return []
    return pd.read_csv(path).to_dict(orient="records")
