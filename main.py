import streamlit as st
import time
from config.settings import PAGE_CONFIG
from data.data_generator import create_sample_data_if_not_exists
from data.data_loader import load_data
from pages import dashboard, inventory, orders, costs, suppliers, forecasting, alerts


# Main application function
def main():
    # Create sample data if not exists
    create_sample_data_if_not_exists()
    
    # Sidebar navigation
    st.sidebar.title("📦 Supply Chain Dashboard")
    
    navigation = st.sidebar.radio("Navigation", [
        "Dashboard Overview", 
        "Inventory Management", 
        "Order & Shipment Tracking",
        "Cost Analysis",
        "Supplier Performance",
        "Demand Forecasting",
        "Alerts & Notifications",
    ])
    
    # Load data
    data = load_data()
    
    # Render selected page
    if navigation == "Dashboard Overview":
        dashboard.render_dashboard_overview(data)
    elif navigation == "Inventory Management":
        inventory.render_inventory_management(data)
    elif navigation == "Order & Shipment Tracking":
        orders.render_order_shipment_tracking(data)
    elif navigation == "Cost Analysis":
        costs.render_cost_analysis(data)
    elif navigation == "Supplier Performance":
        suppliers.render_supplier_performance(data)
    elif navigation == "Demand Forecasting":
        forecasting.render_demand_forecasting()
    elif navigation == "Alerts & Notifications":
        alerts.render_alerts_notifications()
    
    # Footer
    st.sidebar.markdown("---")
    # st.sidebar.info("Supply Chain Dashboard v1.0.0")
    
    # Show loading state for data refresh
    with st.sidebar:
        if st.button("Refresh Data"):
            with st.spinner("Refreshing data..."):
                time.sleep(1)  # Simulate loading
                st.success("✅ Data refreshed!")
                st.rerun()


#########################################################################################################################################

if __name__ == "__main__":
    main()