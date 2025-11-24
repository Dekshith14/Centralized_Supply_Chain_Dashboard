import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np



def render_order_shipment_tracking(data):
    orders = data["orders"]
    shipments = data["shipments"]
    
    st.title("🚚 Order & Shipment Tracking")
    
    tab1, tab2 = st.tabs(["📝 Orders", "🚚 Shipments"])
    
    with tab1:
        st.subheader("Order Management")
        
        # Order filters
        st.write("Filter Orders")
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect("Order Status", 
                                         options=orders["status"].unique() if not orders.empty else [],
                                         default=orders["status"].unique() if not orders.empty else [])
        with col2:
            date_range = st.date_input(
                "Order Date Range",
                value=(
                    orders["order_date"].min().date() if not orders.empty and "order_date" in orders.columns else datetime.now() - timedelta(days=30),
                    orders["order_date"].max().date() if not orders.empty and "order_date" in orders.columns else datetime.now()
                )
            )
        
        # Filter orders
        filtered_orders = orders
        if not orders.empty:
            if status_filter:
                filtered_orders = filtered_orders[filtered_orders["status"].isin(status_filter)]
                
            filtered_orders = filtered_orders[
                (filtered_orders["order_date"].dt.date >= date_range[0]) & 
                (filtered_orders["order_date"].dt.date <= date_range[1])
            ]
        
        # Display orders
        st.dataframe(filtered_orders)
        
        # Order analytics
        if not orders.empty:
            st.subheader("Order Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Orders by status
                status_counts = orders["status"].value_counts().reset_index()
                status_counts.columns = ["Status", "Count"]
                fig = px.pie(status_counts, values="Count", names="Status", 
                           title="Orders by Status")
                st.plotly_chart(fig)
            
            with col2:
                # Order timeline
                orders_by_date = orders.groupby(orders["order_date"].dt.date).size().reset_index()
                orders_by_date.columns = ["Date", "Count"]
                fig = px.line(orders_by_date, x="Date", y="Count", 
                            title="Orders over Time",
                            labels={"Count": "# of Orders", "Date": "Date"})
                st.plotly_chart(fig)
            
            # Top customers
            st.subheader("Top Customers")
            customer_orders = orders.groupby("customer").agg(
                order_count=("order_id", "count"),
                total_value=("total_value", "sum")
            ).reset_index().sort_values("total_value", ascending=False).head(5)
            
            fig = px.bar(customer_orders, x="customer", y="total_value", 
                       text_auto='.2s',
                       color="order_count",
                       labels={"total_value": "Total Value ($)", "customer": "Customer", "order_count": "# Orders"},
                       title="Top 5 Customers by Order Value")
            st.plotly_chart(fig)
    
    with tab2:
        st.subheader("Shipment Tracking")
        
        # Shipment filters
        st.write("Filter Shipments")
        col1, col2 = st.columns(2)
        with col1:
            shipment_status = st.multiselect("Shipment Status", 
                                         options=shipments["status"].unique() if not shipments.empty else [],
                                         default=shipments["status"].unique() if not shipments.empty else [])
        with col2:
            carrier_filter = st.multiselect("Carrier", 
                                         options=shipments["carrier"].unique() if not shipments.empty else [],
                                         default=shipments["carrier"].unique() if not shipments.empty else [])
        
        # Filter shipments
        filtered_shipments = shipments
        if not shipments.empty:
            if shipment_status:
                filtered_shipments = filtered_shipments[filtered_shipments["status"].isin(shipment_status)]
            if carrier_filter:
                filtered_shipments = filtered_shipments[filtered_shipments["carrier"].isin(carrier_filter)]
        
        # Display shipments
        st.dataframe(filtered_shipments)
        
        # Shipment analytics
        if not shipments.empty:
            st.subheader("Shipment Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Shipments by status
                status_counts = shipments["status"].value_counts().reset_index()
                status_counts.columns = ["Status", "Count"]
                fig = px.pie(status_counts, values="Count", names="Status", 
                           title="Shipments by Status")
                st.plotly_chart(fig)
            
            with col2:
                # Carrier performance
                carrier_perf = shipments.groupby("carrier").agg(
                    total_shipments=("shipment_id", "count"),
                    delayed=("status", lambda x: sum(x == "Delayed")),
                ).reset_index()
                
                carrier_perf["on_time_pct"] = (1 - carrier_perf["delayed"] / carrier_perf["total_shipments"]) * 100
                
                fig = px.bar(carrier_perf, x="carrier", y="on_time_pct",
                           labels={"carrier": "Carrier", "on_time_pct": "On-Time %"},
                           color="on_time_pct",
                           color_continuous_scale=px.colors.sequential.Viridis,
                           title="Carrier On-Time Performance")
                fig.update_layout(yaxis_range=[0, 100])
                st.plotly_chart(fig)
            
            # Delivery timeline
            st.subheader("Estimated Delivery Timeline")
            
            # Create dummy timeline data for visualization
            timeline_data = []
            for _, shipment in filtered_shipments.iterrows():
                if pd.notna(shipment["ship_date"]) and pd.notna(shipment["estimated_arrival"]):
                    timeline_data.append({
                        "Task": f"SHP-{shipment['shipment_id'][-4:]}",
                        "Start": shipment["ship_date"],
                        "Finish": shipment["estimated_arrival"],
                        "Status": shipment["status"]
                    })
            
            if timeline_data:
                timeline_df = pd.DataFrame(timeline_data)
                fig = px.timeline(timeline_df, x_start="Start", x_end="Finish", y="Task", color="Status")
                fig.update_layout(title="Shipment Timeline")
                st.plotly_chart(fig)