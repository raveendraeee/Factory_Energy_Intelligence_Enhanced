import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("database/energy.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            voltage REAL,
            current REAL,
            power_kw REAL,
            power_factor REAL,
            temperature REAL
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS anomaly_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telemetry_id INTEGER,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            prediction TEXT NOT NULL,
            anomaly_score REAL
        )
        """)
        conn.commit()

def insert_telemetry(record):
    initialize_database()
    with get_connection() as conn:
        cur = conn.execute("""
        INSERT INTO telemetry
        (device_id,timestamp,voltage,current,power_kw,power_factor,temperature)
        VALUES (?,?,?,?,?,?,?)
        """, (
            record["device_id"], record["timestamp"], record["voltage"],
            record["current"], record["power_kw"],
            record["power_factor"], record["temperature"]
        ))
        conn.commit()
        return cur.lastrowid

def insert_anomaly_event(telemetry_id, record, prediction, score=None):
    initialize_database()
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO anomaly_events
        (telemetry_id,device_id,timestamp,prediction,anomaly_score)
        VALUES (?,?,?,?,?)
        """, (
            telemetry_id, record["device_id"], record["timestamp"],
            prediction, score
        ))
        conn.commit()

def read_telemetry():
    initialize_database()
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM telemetry ORDER BY timestamp", conn)

def read_anomalies():
    initialize_database()
    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT * FROM anomaly_events ORDER BY timestamp", conn
        )
