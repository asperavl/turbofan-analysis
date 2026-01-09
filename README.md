# ✈️ Turbofan Engine RUL Predictor

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://[YOUR-APP-LINK].streamlit.app/)

A cloud-native predictive maintenance system that estimates the **Remaining Useful Life (RUL)** of turbofan jet engines based on sensor telemetry.

This repository contains the **Frontend Dashboard** built with Streamlit. It communicates with a backend inference engine hosted on **AWS Lambda** (containerized with Docker).

## 🏗️ Architecture

The system follows a serverless microservices architecture:

1.  **Frontend:** Streamlit Dashboard (this repo) for interactive testing and visualization.
2.  **API Layer:** Amazon API Gateway handles secure REST requests.
3.  **Inference Engine:** AWS Lambda runs a custom Docker container.
4.  **Model:** XGBoost Regressor trained on the NASA CMAPSS Turbofan degradation dataset.

## 🚀 Features

* **Interactive Simulation:** Adjust 21 different engine sensor parameters (Fan Speed, Core Speed, Temperatures) via sliders to see real-time RUL impact.
* **Production-Ready Input:** Accepts raw JSON telemetry arrays (simulating IoT device payloads) for bulk testing.
* **Smart Filtering:** Backend automatically validates and filters noisy sensor data before inference.
* **Serverless Scalability:** Zero-idle cost infrastructure using AWS Lambda.

## 🛠️ Tech Stack

* **Frontend:** Python, Streamlit, Pandas
* **Backend:** AWS Lambda, Amazon API Gateway
* **Containerization:** Docker, Amazon ECR
* **Machine Learning:** XGBoost, Scikit-Learn

## 💻 Local Installation

To run this dashboard locally:

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/asperavl/turbofan-analysis.git
    cd turbofan-analysis
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Secrets:**
    Create a `.streamlit/secrets.toml` file and add your API Endpoint:
    ```toml
    API_URL = "https://your-api-gateway-url.amazonaws.com/"
    ```

4.  **Run the app:**
    ```bash
    streamlit run dashboard.py
    ```
