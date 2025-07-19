import streamlit as st
import json
import time
from pathlib import Path

st.set_page_config(page_title="AIM – Asset Intelligence Module", layout="centered")
st.title("🤖 AIM – Real-Time Smart Maintenance Co-Pilot")

data_file = Path("data/live_feed.json")

if not data_file.exists():
    st.error("Live data not yet generated. Please run simulator.py.")
    st.stop()

with open(data_file) as f:
    data = json.load(f)

st.metric(label="🌀 Fan 1 Speed (RPM)", value=data["fan_1_speed"])
st.metric(label="🌀 Fan 2 Speed (RPM)", value=data["fan_2_speed"])
st.metric(label="🌡️ Temperature (°C)", value=round(data["temperature"], 2))
st.caption(f"Last updated: {data['timestamp']}")

st.divider()
st.subheader("🧠 AI Co-Pilot Insight")

# Insight logic
if data["fan_2_speed"] == 0 and data["temperature"] > 27:
    st.warning("⚠️ Fan 2 is inactive while temperature is rising — check for failure.")
    if st.button("Generate Work Order for Fan 2"):
        st.success("✅ Work order generated and logged.")
elif data["temperature"] > 30:
    st.error("🔥 High temperature detected! Suggest urgent inspection.")
    if st.button("Alert Technician"):
        st.success("🚨 Alert sent!")
else:
    st.success("✅ System running smoothly.")

st.divider()
if st.button("🔄 Refresh Now"):
    st.rerun()
