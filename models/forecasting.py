import pandas as pd
import numpy as np
import os

# ML Component for Demand Forecasting


def forecast_demand():

    # Simple time series forecasting for inventory demand
    if "orders.csv" not in os.listdir():
        return None
    
    orders = pd.read_csv("orders.csv")
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    
    # Group by date and count orders
    daily_orders = orders.groupby(orders["order_date"].dt.date).size().reset_index()
    daily_orders.columns = ["date", "order_count"]
    daily_orders["date"] = pd.to_datetime(daily_orders["date"])
    
    
    # Simple moving average forecast
    if len(daily_orders) >= 7:
        # Create features (last 7 days)
        daily_orders["forecast"] = daily_orders["order_count"].rolling(window=7).mean().shift(1)
        daily_orders = daily_orders.dropna()
        
        # Forecast next 7 days
        last_date = daily_orders["date"].max()
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
        last_avg = daily_orders["order_count"].tail(7).mean()
        
        forecast_df = pd.DataFrame({
            "date": forecast_dates,
            "forecast": [last_avg] * 7
        })
        
        return daily_orders, forecast_df
    
    return None