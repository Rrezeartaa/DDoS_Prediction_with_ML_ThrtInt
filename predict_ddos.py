import time
import json
import numpy as np
import joblib
import logging
from collections import deque
from datetime import datetime
from xgboost import XGBClassifier

MODEL_PATH = "xg_boost_best_model.pkl"
LOG_PATH = "/var/log/pfsense.log" # the file in Wazuh for the active logs to be written from pfSense
SLIDING_WINDOW_SIZE = 60
CONFIDENCE_THRESHOLD = 0.9
REPLICA_COUNT = 5
QUORUM_THRESHOLD = 3  # simple 3-of-5 consensus

logging.basicConfig(
    filename="prediction_service.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

try:
    model: XGBClassifier = joblib.load(MODEL_PATH)
    logging.info(f"Loaded XGBoost model from {MODEL_PATH}")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise SystemExit(e)

def check_replicas_agree(confidence: float) -> bool:

    votes = [confidence > CONFIDENCE_THRESHOLD for _ in range(REPLICA_COUNT)]
    return sum(votes) >= QUORUM_THRESHOLD


def write_alert(alert_data: dict):

    try:
        with open(LOG_PATH, "a") as log_file:
            log_file.write(json.dumps(alert_data) + "\n")
        logging.info(f"Alert written to Wazuh: {alert_data}")
    except Exception as e:
        logging.error(f"Failed to write alert: {e}")

window = deque(maxlen=SLIDING_WINDOW_SIZE)

def predict_realtime(flow_features: np.ndarray):

    window.append(flow_features)

    if len(window) < SLIDING_WINDOW_SIZE:
        return

    X = np.mean(window, axis=0).reshape(1, -1)
    proba = float(model.predict_proba(X)[0, 1])

    if proba > CONFIDENCE_THRESHOLD and check_replicas_agree(proba):
        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": round(proba, 4),
            "features": X.tolist(),
        }
        write_alert(alert)
        print(f"[ALERT] DDoS detected | Confidence: {proba:.4f}")
    else:
        print(f"[INFO] No attack detected | Confidence: {proba:.4f}")


if __name__ == "__main__":
    print("Starting real-time DDoS detection service...")
    logging.info("Service started")

    try:
        while True:
            mock_flow = np.random.rand(15)  # 15 features, as per dataset (inside the AWS config actual flow ingestion from pfSense logs are made in real-time)
            predict_realtime(mock_flow)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping service.")
        logging.info("Service stopped by user")
