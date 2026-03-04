import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import os
import subprocess

# Page Config
st.set_page_config(page_title="RailPlan AI", layout="wide")

# --- Helper Functions ---
@st.cache_data
def load_data():
    if os.path.exists("railway_data.csv"):
        df = pd.read_csv("railway_data.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        
        # ✅ Create Route column from Source and Destination
        df['Route'] = df['Source'] + " - " + df['Destination']
        
        return df
    else:
        return None

def train_model(df):
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    
    # Encode Route for ML model
    df['Route_Encoded'] = df['Route'].astype('category').cat.codes
    
    features = ['Month', 'Day', 'Is_Weekend', 'Is_Holiday', 'Route_Encoded']
    target = 'Passenger_Count'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    
    return model, mae

def predict_demand(model, route_str, date_str):
    # Create temporary dataframe to get route code
    df_temp = pd.DataFrame({'Route': [route_str]})
    route_code = df_temp['Route'].astype('category').cat.codes.iloc[0]
    
    date = pd.to_datetime(date_str)
    features = {
        'Month': date.month,
        'Day': date.day,
        'Is_Weekend': 1 if date.dayofweek >= 5 else 0,
        'Is_Holiday': 0,
        'Route_Encoded': route_code
    }
    df_pred = pd.DataFrame([features])
    return model.predict(df_pred)[0]

# --- Main App ---
st.title("🚆 Smart Railway Resource Planning System")
st.markdown("Tekworks Hackathon | Optimizing Railway Resources with AI")

# Sidebar
st.sidebar.header("Configuration")
if st.sidebar.button("Generate Sample Data"):
    subprocess.run(["python", "data_generator.py"])
    st.success("Data generated! Refreshing...")
    st.rerun()

df = load_data()

if df is not None:
    # --- Tab 1: Dashboard Overview ---
    tab1, tab2, tab3 = st.tabs(["📊 Demand Analytics", "🤖 Prediction Engine", "📋 Resource Recommendations"])
    
    with tab1:
        st.subheader("Historical Passenger Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            # ✅ Added unique key='route_filter'
            route_filter = st.selectbox("Select Route", df['Route'].unique(), key='route_filter')
            filtered_df = df[df['Route'] == route_filter]
            
            fig = px.line(filtered_df, x='Date', y='Passenger_Count', title=f"Passenger Demand: {route_filter}", markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Platform Utilization Heatmap")
            platform_heat = df.pivot_table(index='Date', columns='Platform', values='Passenger_Count', aggfunc='sum')
            fig_heat = px.imshow(platform_heat, aspect="auto", color_continuous_scale="Blues", title="Platform Load Intensity")
            st.plotly_chart(fig_heat, use_container_width=True)

    with tab2:
        st.subheader("AI Demand Forecasting")
        st.info("Model: Random Forest Regressor | Metric: Mean Absolute Error")
        
        model, mae = train_model(df)
        st.metric("Model Accuracy (MAE)", f"{mae:.2f} passengers")
        
        st.markdown("### Predict Future Demand")
        col1, col2, col3 = st.columns(3)
        with col1:
            # ✅ Added unique key='route_select'
            selected_route = st.selectbox("Select Route", df['Route'].unique(), key='route_select')
        with col2:
            selected_date = st.date_input("Select Date", min_value=df['Date'].min(), max_value=df['Date'].max())
        with col3:
            if st.button("Predict", key='predict_btn'):
                pred = predict_demand(model, selected_route, str(selected_date))
                st.success(f"Predicted Passengers: **{int(pred)}**")
                
                fig_pred = go.Figure()
                fig_pred.add_trace(go.Scatter(x=[selected_date], y=[pred], mode='markers', name='Prediction', marker=dict(size=15, color='red')))
                fig_pred.update_layout(title=f"Forecast for {selected_date} on {selected_route}", xaxis_title="Date", yaxis_title="Passengers")
                st.plotly_chart(fig_pred, use_container_width=True)

    with tab3:
        st.subheader("Resource Allocation Recommendations")
        st.markdown("Based on predicted demand vs. current **Seat_Capacity**.")
        
        df['Utilization_Rate'] = (df['Passenger_Count'] / df['Seat_Capacity']) * 100
        df['Overcrowding'] = df['Utilization_Rate'] > 100
        
        high_demand = df[df['Utilization_Rate'] > 80].groupby(['Route', 'Date']).agg({
            'Passenger_Count': 'sum',
            'Seat_Capacity': 'sum',
            'Train_ID': 'count'
        }).reset_index()
        
        st.dataframe(high_demand, use_container_width=True)
        
        st.markdown("### Actionable Alerts")
        alerts = df[df['Overcrowding'] == True]
        if not alerts.empty:
            st.error(f"⚠️ **{len(alerts)}** instances of Overcrowding detected in historical data.")
            st.warning("Recommendation: Add coaches to these specific train runs.")
            
            st.markdown("#### Proactive Planning Suggestion")
            st.write("For the upcoming peak period (Next 7 Days):")
            future_dates = pd.date_range(start=df['Date'].max(), periods=7)
            recommendations = []
            
            for date in future_dates:
                for route in df['Route'].unique():
                    route_code = df[df['Route'] == route]['Route_Encoded'].iloc[0]
                    pred = predict_demand(model, route, str(date))
                    capacity = 600 
                    if pred > capacity:
                        recommendations.append({
                            "Date": date,
                            "Route": route,
                            "Predicted Demand": int(pred),
                            "Capacity": capacity,
                            "Action": "Add 1 Coach"
                        })
            
            if recommendations:
                rec_df = pd.DataFrame(recommendations)
                st.dataframe(rec_df, use_container_width=True)
            else:
                st.success("No immediate resource adjustments needed for the next week.")
else:
    st.warning("Please generate data first using the sidebar button.")