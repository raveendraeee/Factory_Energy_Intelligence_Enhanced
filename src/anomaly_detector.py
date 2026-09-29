from pathlib import Path
import joblib
from sklearn.ensemble import IsolationForest

MODEL_PATH = Path("models/isolation_forest.joblib")

def train_model(features, contamination=0.05, random_state=42):
    model = IsolationForest(
        contamination=contamination,
        random_state=random_state,
    )
    model.fit(features)
    return model

def save_model(model, path=MODEL_PATH):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)

def load_model(path=MODEL_PATH):
    return joblib.load(path)

def predict_anomalies(model, features):
    return model.predict(features)

def anomaly_score(model, features):
    return model.decision_function(features)
