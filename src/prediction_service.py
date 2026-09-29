from .anomaly_detector import anomaly_score, load_model, predict_anomalies
from .feature_engineering import extract_features, telemetry_to_dataframe


def predict_telemetry(telemetry):
    dataframe = telemetry_to_dataframe([telemetry])
    features = extract_features(dataframe)
    model = load_model()
    raw = predict_anomalies(model, features)[0]
    score = float(anomaly_score(model, features)[0])
    is_anomaly = int(raw == -1)
    return {
        "device_id": telemetry["device_id"],
        "timestamp": telemetry["timestamp"],
        "is_anomaly": is_anomaly,
        "prediction": "ANOMALY" if is_anomaly else "NORMAL",
        "anomaly_score": score,
    }
