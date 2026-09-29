import pandas as pd

FEATURE_COLUMNS = [
    "voltage",
    "current",
    "power_kw",
    "power_factor",
    "temperature",
]

def telemetry_to_dataframe(records):
    return pd.DataFrame(records)

def extract_features(dataframe):
    missing = [c for c in FEATURE_COLUMNS if c not in dataframe.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")
    return dataframe[FEATURE_COLUMNS].astype(float)
