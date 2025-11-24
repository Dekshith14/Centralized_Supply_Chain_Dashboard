import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

# Dashboard pages

def render_dashboard_overview(data):
    inventory = data["inventory"]
    orders = data["orders"]
    shipments = data["shipments"]
    costs = data["costs"]
    
    # KPI section
    st.title("📊 Centralized Supply Chain Monitoring Dashboard")
    
    # Date Filters
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From Date", datetime.now() - pd.Timedelta(days=30))
    with col2:
        end_date = st.date_input("To Date", datetime.now())
    
    # KPI Summary Cards with deltas (showing change from previous period)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    low_stock_count = len(inventory[inventory["stock_level"] < inventory["reorder_threshold"]])
    kpi1.metric("🔻 Low Stock Items", low_stock_count, delta="-2 from last week")
    
    if not orders.empty:
        total_orders = len(orders)
        new_orders = len(orders[orders["status"] == "New"])
        kpi2.metric("🛒 Total Orders", total_orders, delta=f"+{new_orders} new")
    
    if not shipments.empty:
        on_time = len(shipments[shipments["status"] != "Delayed"])
        on_time_pct = round((on_time / len(shipments)) * 100)
        kpi3.metric("📦 On-Time Delivery", f"{on_time_pct}%", delta=f"{on_time_pct - 95}% from target")
    
    if not costs.empty:
        total_cost = costs["amount"].sum()
        total_budget = costs["budget"].sum()
        cost_variance = round(((total_budget - total_cost) / total_budget) * 100, 1)
        kpi4.metric("💰 Budget Variance", f"${total_cost:,.2f}", delta=f"{cost_variance}% under budget")
    

    # Main overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Order Status Distribution")
        if not orders.empty:
            order_status = orders["status"].value_counts().reset_index()
            order_status.columns = ["Status", "Count"]
            fig = px.pie(order_status, values="Count", names="Status", hole=0.4,
                       color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Supply Chain Cost Breakdown")
        if not costs.empty:
            fig = px.bar(costs, x="category", y="amount", text_auto='.2s',
                       color="amount", labels={"amount": "Cost ($)"})
            fig.update_layout(xaxis_title="Category", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)
    

    # Inventory status
    st.subheader("Inventory Health")
    if not inventory.empty:
        # calculate health metrics
        inventory["status"] = pd.cut(
            inventory["stock_level"] / inventory["reorder_threshold"],
            bins=[0, 0.8, 1.5, float('inf')],
            labels=["Critical", "Warning", "Healthy"]
        )
        
        status_counts = inventory["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        fig = px.bar(status_counts, x="Status", y="Count", color="Status",
                   color_discrete_map={"Critical": "red", "Warning": "orange", "Healthy": "green"})
        st.plotly_chart(fig, use_container_width=True)
        
        # Show critical items
        critical_items = inventory[inventory["status"] == "Critical"]
        if not critical_items.empty:
            st.error("🚨 Critical Stock Levels - Immediate Action Required")
            st.dataframe(critical_items[["item_name", "stock_level", "reorder_threshold"]])