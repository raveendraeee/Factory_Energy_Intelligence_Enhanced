from pathlib import Path
import pandas as pd
from src.anomaly_detector import train_model, save_model

path = Path("data/cloud_demo/telemetry.csv")
df = pd.read_csv(path)
features = df.loc[df["injected_anomaly"] == 0,
                  ["voltage","current","power_kw","power_factor","temperature"]]
model = train_model(features)
save_model(model)
print("Model saved.")
