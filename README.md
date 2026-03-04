# 🚆 Smart Railway Resource Planning System

> **Tekworks Hackathon Submission**  
> *Optimizing Railway Resources with AI-Powered Demand Prediction*

---

## 📋 Project Overview

The **Smart Railway Resource Planning System** is a data-driven web application designed to help railway planners make smarter decisions about resource allocation. By leveraging historical and operational data, the system predicts passenger demand, identifies overcrowding risks, and recommends optimal train and coach allocations.

### 🎯 Problem Statement
Railway planners often rely on intuition rather than data, leading to:
- ❌ Overcrowding during peak periods
- ❌ Inefficient coach and train allocation
- ❌ Poor platform utilization
- ❌ Reactive rather than proactive planning

### 💡 Our Solution
A Streamlit-based dashboard that:
- ✅ Visualizes historical passenger demand
- ✅ Predicts future demand using Machine Learning
- ✅ Recommends resource adjustments (coaches/trains)
- ✅ Alerts on overcrowding risks

---

## 🚀 Features
Feature

Description

📊 **Demand Analytics

Interactive charts showing passenger trends by route and date

🤖 **AI Forecasting

Random Forest model to predict future passenger demand

📋 **Resource Recommendations

Actionable alerts for coach/train allocation

⚠️ **Overcrowding Alerts

Real-time detection of high-utilization periods

📈 **Platform Heatmap

Visual representation of platform usage intensity

**Frontend**
Streamlit (Python)

**Data Processing**
Pandas, NumPy

**Machine Learning**
Scikit-Learn (Random Forest)

**Visualization**
Plotly, Matplotlib

**Data Storage**: CSV (Synthetic Dataset)

**Project Structure**
tekworks hackathon/
│
├── data_generator.py       # Script to generate synthetic railway data
├── app.py                  # Main Streamlit dashboard application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── railway_data.csv        # Generated dataset (created after running generator)

