# 🌍 AI-DRIVEN-ENVIRONMENTAL-MONITORING-AND-FORECASTING-SYSTEM

AI-Driven Environmental Monitoring and Forecasting System uses spatiotemporal models like CNN+LSTM and ConvLSTM to predict air quality and classify satellite images. It integrates sensor and satellite data to support urban planning, pollution control, and environmental risk management.


A deep learning-powered system that monitors and forecasts environmental conditions using spatiotemporal models. This project integrates air quality forecasting and satellite image classification to support urban planning, public health, and sustainability goals.



## 🚀 Overview

Environmental changes are dynamic and complex. This project applies **AI and deep learning models** (CNN+LSTM, ConvLSTM, MobileNet) to:
- 📈 Forecast **Air Quality Index (AQI)** using real-time sensor data (PM2.5, PM10, NO₂, SO₂, CO, etc.)
- 🛰️ Classify **satellite images** into environmental categories (e.g., roads, water bodies, vegetation, buildings)
  
This unified system offers actionable insights for authorities, planners, and citizens to better understand and react to environmental changes.

---

## 🧠 Core Technologies

| Task                        | Models Used               | Data Sources                          |
|----------------------------|---------------------------|----------------------------------------|
| AQI Forecasting            | Linear Regression, ARIMA, CNN+LSTM, ConvLSTM | IoT sensor data, AQI datasets |
| Satellite Image Classification | MobileNet, CNN+LSTM         | MODIS, Sentinel, custom labeled datasets |

---

## 📂 Project Structure

📁 ai-environment-monitoring/
├── models/              # Trained deep learning models
├── data/                # Raw & processed sensor + satellite data
├── src/                 # Model training, preprocessing, utilities
├── notebooks/           # Jupyter notebooks for EDA & experiments
├── results/             # Prediction outputs, metrics, visualizations
├── flask_app/           # (Optional) Web app interface
├── README.md
├── requirements.txt
└── LICENSE
