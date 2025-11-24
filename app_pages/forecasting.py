import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from models.forecasting import forecast_demand  # importing the model function



def render_demand_forecasting():

    st.title("📈 Demand Forecasting")
    
    # Get forecast data
    forecast_result = forecast_demand()
    
    if forecast_result:
        historical_data, forecast_df = forecast_result
        
        st.subheader("Order Volume Forecast")
        
        # Combine historical and forecast data for visualization
        historical_data["type"] = "Historical"
        forecast_df["type"] = "Forecast"
        forecast_df["order_count"] = forecast_df["forecast"]
        
        combined_data = pd.concat([historical_data, forecast_df])
        
        fig = px.line(combined_data, x="date", y="order_count", color="type",
                    title="Order Volume - Historical & Forecast",
                    labels={"order_count": "Number of Orders", "date": "Date"})
        st.plotly_chart(fig)
        
        # Forecast details
        st.subheader("Forecast Details")
        st.dataframe(forecast_df[["date", "forecast"]].rename(columns={"forecast": "Forecasted Orders"}))
        
        # Forecast accuracy (dummy metrics for now)
        st.subheader("Forecast Accuracy Metrics")
        col1, col2, col3 = st.columns(3)
        # col1.metric("MAPE", "15.3%")
        # col2.metric("MAE", "2.4 orders")
        # col3.metric("Forecast Bias", "+0.8")

        from sklearn.metrics import mean_absolute_error
        mae = mean_absolute_error(historical_data["order_count"], historical_data["forecast"])
        mape = (np.abs((historical_data["order_count"] - historical_data["forecast"]) / historical_data["order_count"])).mean() * 100
        bias = (historical_data["forecast"] - historical_data["order_count"]).mean()

        col1.metric("MAPE", mape)
        col2.metric("MAE", mae)
        col3.metric("Forecast Bias", bias)

        # Inventory recommendations based on forecast
        st.subheader("Inventory Recommendations")
        
        st.info("Based on the forecast, consider the following actions:")
        recommendations = [
            "Increase stock levels for Raw Material A by 20% to meet projected demand",
            "Expedite orders for Component B to avoid stockout in the next 7 days",
            "Consider reducing order frequency and increasing order quantity for Part C to optimize costs",
            "Schedule production increase for Finished Product J starting next week"
        ]
        
        for i, rec in enumerate(recommendations):
            st.write(f"{i+1}. {rec}")
    else:
        st.info("Insufficient order data for forecasting. Please add more order data.")
        
        # Show sample forecast chart anyway
        st.subheader("Sample Forecast Visualization")
        dates = pd.date_range(start=datetime.now() - pd.Timedelta(days=30), periods=45)
        sample_data = pd.DataFrame({
            "date": dates,
            "order_count": np.random.normal(loc=10, scale=2, size=45).round()
        })
        sample_data["type"] = "Historical"
        sample_data.loc[sample_data["date"] > datetime.now(), "type"] = "Forecast"
        
        fig = px.line(sample_data, x="date", y="order_count", color="type",
                    title="Sample Order Forecast",
                    labels={"order_count": "Number of Orders", "date": "Date"})
        fig.add_vline(x=datetime.now(), line_dash="dash", line_color="gray")
        st.plotly_chart(fig)
        
        st.write("Upload order data to generate actual forecasts.")