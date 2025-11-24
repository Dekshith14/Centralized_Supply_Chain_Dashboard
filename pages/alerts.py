import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go



def render_alerts_notifications():
    st.title("🚨 Alerts & Notifications")
    
    # Generate sample alerts
    alerts = [
        {"severity": "Critical", "message": "Item 'Raw Material A' has reached critical stock level (5 units)", "time": "2 hours ago"},
        {"severity": "High", "message": "Shipment SHP-0015 is delayed by carrier", "time": "5 hours ago"},
        {"severity": "Medium", "message": "New order received from Customer B worth $8,500", "time": "Yesterday"},
        {"severity": "Low", "message": "Supplier D performance dropped below threshold", "time": "2 days ago"},
        {"severity": "Critical", "message": "Component G stock level is zero - production impact likely", "time": "2 days ago"}
    ]
    
    # Alert filters
    st.subheader("Alert Filters")
    col1, col2 = st.columns(2)
    with col1:
        severity_filter = st.multiselect("Severity", 
                                       options=["Critical", "High", "Medium", "Low"],
                                       default=["Critical", "High"])
    with col2:
        date_filter = st.selectbox("Time Range", 
                                 options=["All Time", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
                                 index=0)
    
    # Filter alerts (in a real app, this would filter from database)
    filtered_alerts = [alert for alert in alerts if alert["severity"] in severity_filter]
    
    # Display alerts
    st.subheader("Current Alerts")
    
    if not filtered_alerts:
        st.success("No alerts matching the selected criteria.")
    else:
        for alert in filtered_alerts:
            if alert["severity"] == "Critical":
                st.error(f"**{alert['severity']}**: {alert['message']} - {alert['time']}")
            elif alert["severity"] == "High":
                st.warning(f"**{alert['severity']}**: {alert['message']} - {alert['time']}")
            elif alert["severity"] == "Medium":
                st.info(f"**{alert['severity']}**: {alert['message']} - {alert['time']}")
            else:
                st.success(f"**{alert['severity']}**: {alert['message']} - {alert['time']}")
    
    # Alert settings
    with st.expander("Alert Settings"):
        st.subheader("Notification Preferences")
        
        st.checkbox("Email notifications", value=True)
        st.checkbox("SMS notifications", value=False)
        st.checkbox("In-app notifications", value=True)
        
        st.subheader("Alert Thresholds")
        st.slider("Low stock threshold (%)", 0, 100, 20, 
                help="Alert when stock falls below this percentage of reorder level")
        st.slider("Delivery delay threshold (days)", 0, 10, 1, 
                help="Alert when delivery is delayed by this many days")
        
        if st.button("Save Settings"):
            st.success("✅ Alert settings saved successfully!")
