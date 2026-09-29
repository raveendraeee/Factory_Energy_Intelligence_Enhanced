import pandas as pd

from src.feature_engineering import extract_features


def test_extract_features():
    df = pd.DataFrame([{
        "voltage": 230, "current": 8, "power_kw": 1.7,
        "power_factor": 0.92, "temperature": 34
    }])
    out = extract_features(df)
    assert list(out.columns) == [
        "voltage", "current", "power_kw", "power_factor", "temperature"
    ]
