# Factory Energy Intelligence v1.6

Runnable IoT + AI anomaly-detection reference implementation.

## Stack

- Python 3.14
- MQTT / HiveMQ Cloud
- SQLite for local/demo mode
- PostgreSQL for Docker/industrial mode
- Isolation Forest
- Streamlit
- Grafana
- FastAPI
- Docker Compose
- GitHub Actions

## Quick local demo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/prepare_cloud_demo.py
streamlit run dashboard/app.py
```

The Streamlit application automatically uses `data/cloud_demo/*.csv` when available, so the dashboard can run without MQTT credentials.

## Docker stack

```powershell
docker compose up --build
```

Services:

- Streamlit: http://localhost:8501
- FastAPI: http://localhost:8000/docs
- Grafana: http://localhost:3000
- PostgreSQL: localhost:5432

Default Grafana login for the local stack:
`admin` / `admin`

## Live MQTT mode

Copy `.env.example` to `.env` and add HiveMQ credentials. Never commit `.env`.

```powershell
python scripts/generate_data.py
python -m src.mqtt_publisher
```

In another terminal:

```powershell
python -m src.mqtt_subscriber
```

## Streamlit Cloud

Deploy `dashboard/app.py` from GitHub.

The repository includes cloud-demo CSV data, so the application is usable without private MQTT credentials. For live MQTT, add the required secrets in Streamlit Cloud settings.

## Versioning

This package is the implementation baseline for v1.6.0. Use Git tags:

```text
v1.0.0
v1.1.0
...
v1.6.0
```

The v1.1-v1.6 roadmap is represented in `docs/VERSION_ROADMAP.md`; features should only be tagged as implemented after their code is actually enabled and tested.
