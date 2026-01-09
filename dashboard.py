import streamlit as st
import requests
import json
import pandas as pd

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# Securely load the API URL from Streamlit Secrets
# This prevents your API link from being exposed in public GitHub repos.
if "API_URL" in st.secrets:
    API_URL = st.secrets["API_URL"]
else:
    st.error("🚨 API URL not found. Please configure secrets on Streamlit Cloud.")
    st.stop()

# ---------------------------------------------------------
# UI LAYOUT
# ---------------------------------------------------------
st.set_page_config(page_title="GE Aerospace: Engine Health Monitor", layout="wide")

st.title("✈️ Turbofan RUL Predictor")
st.markdown("### Cloud-Native Inference Dashboard")

# Create Tabs for different input methods
tab1, tab2 = st.tabs(["🎛️ Interactive Control", "📋 Raw JSON Input"])

# ---------------------------------------------------------
# TAB 1: INTERACTIVE SLIDERS (For Visual Demo)
# ---------------------------------------------------------
with tab1:
    st.info("Adjust key sensor parameters to simulate engine conditions.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚙️ Operational Settings")
        os_1 = st.slider("Operational Setting 1", -0.0050, 0.0050, -0.0007, step=0.0001, format="%.4f")
        os_2 = st.slider("Operational Setting 2", -0.0006, 0.0006, -0.0004, step=0.0001, format="%.4f")
        
        st.subheader("🌡️ Temperature Sensors")
        sensor_2 = st.number_input("Total Temperature (Fan Inlet) [R]", value=641.82)
        sensor_3 = st.number_input("Total Temperature (LPC Outlet) [R]", value=1589.70)
        sensor_4 = st.number_input("Total Temperature (HPC Outlet) [R]", value=1400.60)

    with col2:
        st.subheader("💨 Pressure & Speed Sensors")
        sensor_7 = st.number_input("Total Pressure (HPC Outlet) [psia]", value=554.36)
        sensor_8 = st.number_input("Fan Speed [rpm]", value=2388.06)
        sensor_9 = st.number_input("Core Speed [rpm]", value=9046.19)
        sensor_11 = st.number_input("Static Pressure (HPC Outlet) [psia]", value=47.47)
        sensor_12 = st.number_input("Ratio of Fuel Flow [pps/psi]", value=521.66)

    # Payload construction for Manual Mode
    manual_payload = {
        "os_1": os_1, "os_2": os_2, 
        "sensor_2": sensor_2, "sensor_3": sensor_3, "sensor_4": sensor_4,
        "sensor_7": sensor_7, "sensor_8": sensor_8, "sensor_9": sensor_9,
        "sensor_11": sensor_11, "sensor_12": sensor_12,
        # Default values for hidden sensors
        "sensor_13": 2388.02, "sensor_14": 8138.62, "sensor_15": 8.4195,
        "sensor_17": 392, "sensor_20": 39.06, "sensor_21": 23.4190
    }
    
    if st.button("Analyze Slider Data", type="primary"):
        payload = manual_payload
        trigger_api = True
    else:
        trigger_api = False

# ---------------------------------------------------------
# TAB 2: RAW JSON INPUT (For Copy-Paste Testing)
# ---------------------------------------------------------
with tab2:
    st.info("Paste full sensor telemetry JSON here (e.g., from a log file or test case).")
    
    # Default sample data to make it easy to test
    default_json = """{
    "os_1": -0.0007, "os_2": -0.0004, 
    "sensor_2": 641.82, "sensor_3": 1589.70, "sensor_4": 1400.60, 
    "sensor_7": 554.36, "sensor_8": 2388.06, "sensor_9": 9046.19, 
    "sensor_11": 47.47, "sensor_12": 521.66, "sensor_13": 2388.02, 
    "sensor_14": 8138.62, "sensor_15": 8.4195, "sensor_17": 392, 
    "sensor_20": 39.06, "sensor_21": 23.4190
}"""
    
    json_input = st.text_area("Input Payload", value=default_json, height=300)
    
    if st.button("Analyze JSON Payload", type="primary"):
        try:
            payload = json.loads(json_input)
            trigger_api = True
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON format. Please check your syntax.")
            trigger_api = False

# ---------------------------------------------------------
# API LOGIC (Shared)
# ---------------------------------------------------------
if trigger_api:
    st.divider()
    st.write("📡 Connecting to AWS Lambda...")
    
    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            rul = result['predicted_RUL']
            status = result['status']
            
            # Layout the results nicely
            r1, r2, r3 = st.columns([1, 1, 2])
            
            with r1:
                st.metric(label="RUL (Cycles Remaining)", value=f"{rul:.1f}")
            
            with r2:
                if status == "Healthy":
                    st.success(f"✅ System Status: {status}")
                else:
                    st.error(f"⚠️ System Status: {status}")
            
            with r3:
                st.write("**Inference Latency:** Serverless (AWS Lambda)")
                with st.expander("View Raw API Response"):
                    st.json(result)
                    
        else:
            st.error(f"API Error {response.status_code}")
            st.write(response.text)
            
    except Exception as e:
        st.error(f"Connection Failed: {e}")
