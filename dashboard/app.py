from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "data" / "cloud_demo"

st.set_page_config(page_title="Factory Energy Intelligence", page_icon="⚡", layout="wide")

@st.cache_data(ttl=10)
def load_data():
    telemetry_path = DEMO / "telemetry.csv"
    anomalies_path = DEMO / "anomalies.csv"
    if telemetry_path.exists():
        telemetry = pd.read_csv(telemetry_path)
        telemetry["timestamp"] = pd.to_datetime(
            telemetry["timestamp"], format="mixed", utc=True, errors="coerce"
        )
    else:
        telemetry = pd.DataFrame()
    if anomalies_path.exists():
        anomalies = pd.read_csv(anomalies_path)
        anomalies["timestamp"] = pd.to_datetime(
            anomalies["timestamp"], format="mixed", utc=True, errors="coerce"
        )
    else:
        anomalies = pd.DataFrame()
    return telemetry, anomalies

telemetry, anomalies = load_data()

st.title("⚡ Factory Energy Intelligence")
st.caption("IoT + AI anomaly detection | Streamlit Cloud demo")

if telemetry.empty:
    st.error("No demo telemetry found.")
    st.stop()

total = len(telemetry)
peak = telemetry["power_kw"].max()
avg_power = telemetry["power_kw"].mean()
avg_temp = telemetry["temperature"].mean()
detected = len(anomalies)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Telemetry Records", f"{total:,}")
c2.metric("Detected Anomalies", f"{detected:,}")
c3.metric("Peak Power", f"{peak:.2f} kW")
c4.metric("Average Temperature", f"{avg_temp:.1f} °C")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Live Telemetry", "AI Anomalies", "Historical Analytics", "System Health"]
)

with tab1:
    st.subheader("Factory Energy Overview")
    fig = px.line(telemetry, x="timestamp", y="power_kw", title="Power Consumption")
    st.plotly_chart(fig, use_container_width=True)
    fig2 = px.line(
        telemetry, x="timestamp",
        y=["voltage", "current", "temperature"],
        title="Electrical and Thermal Parameters"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Telemetry")
    st.dataframe(
        telemetry.sort_values("timestamp", ascending=False).head(50),
        use_container_width=True,
        hide_index=True,
    )

with tab3:
    st.subheader("AI Anomaly Detection")
    if anomalies.empty:
        st.info("No anomaly events detected.")
    else:
        st.dataframe(
            anomalies.sort_values("timestamp", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        fig = px.scatter(
            telemetry, x="timestamp", y="power_kw",
            color="injected_anomaly",
            title="Injected Scenario vs Power"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Historical Analytics")
    a, b, c = st.columns(3)
    a.metric("Average Power", f"{avg_power:.2f} kW")
    b.metric("Peak Power", f"{peak:.2f} kW")
    c.metric("Average Temperature", f"{avg_temp:.1f} °C")
    fig = px.histogram(telemetry, x="power_kw", nbins=30, title="Power Distribution")
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("System Health")
    st.success("Streamlit application is running")
    st.success("Cloud demo dataset loaded")
    st.success("AI model generated for demo dataset")
    st.info("Live MQTT mode is optional and requires private secrets.")
