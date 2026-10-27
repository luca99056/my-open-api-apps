"""Service 2: Interactive weather dashboard using Open-Meteo."""
import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

st.set_page_config(page_title="Interactive Weather Dashboard", page_icon="🌤️", layout="wide")
st.title("🌤️ Interactive Weather Dashboard")
st.caption("Arts and Advanced Big Data | Open API — Service 2")
st.write("Click a location on the map to explore its hourly temperature forecast.")

@st.cache_data(ttl=600, show_spinner=False)
def get_hourly_temperature(lat: float, lon: float) -> pd.DataFrame:
    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m",
            "forecast_days": 2,
            "timezone": "auto",
        },
        timeout=15,
    )
    response.raise_for_status()
    hourly = response.json()["hourly"]
    df = pd.DataFrame({
        "time": pd.to_datetime(hourly["time"]),
        "Temperature (°C)": hourly["temperature_2m"],
    })
    return df.set_index("time")

st.subheader("1. Pick a place on the map")
fmap = folium.Map(location=[36.5, 127.5], zoom_start=6)
result = st_folium(fmap, height=400, use_container_width=True, key="weather_map")
clicked = (result or {}).get("last_clicked")

if not clicked:
    st.info("Click anywhere on the map (Seoul, Busan, or even the sea) to load the forecast.")
    st.stop()

lat, lon = round(clicked["lat"], 3), round(clicked["lng"], 3)
st.subheader(f"2. Hourly temperature at {lat}, {lon}")

try:
    with st.spinner("Loading the weather forecast..."):
        df = get_hourly_temperature(lat, lon)
    if df.empty:
        st.info("No temperature data is available for this location.")
        st.stop()
except (requests.RequestException, KeyError, ValueError):
    st.error("The weather service is temporarily unavailable. Please try again later.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("First forecast hour", f"{df.iloc[0, 0]:.1f} °C")
col2.metric("Highest", f"{df.iloc[:, 0].max():.1f} °C")
col3.metric("Lowest", f"{df.iloc[:, 0].min():.1f} °C")
st.line_chart(df)
with st.expander("View hourly temperature data"):
    st.dataframe(df, use_container_width=True)
st.caption("Data: Open-Meteo.com (free for non-commercial use).")
