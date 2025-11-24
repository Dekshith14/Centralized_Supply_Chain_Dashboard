import streamlit as st
import time
from config.settings import PAGE_CONFIG
from data.data_generator import create_sample_data_if_not_exists
from data.data_loader import load_data
from app_pages import dashboard, inventory, orders, costs, suppliers, forecasting, alerts


def main():

    create_sample_data_if_not_exists()

    st.set_page_config(**PAGE_CONFIG)

    # Sidebar
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

    # LOAD DATA
    data = load_data()

    # -------------------------
    # ROUTING
    # -------------------------
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
        alerts.render_alerts_notifications()          # ✅ FIXED — pass data + correct function name


    # -------------------------
    # SIDEBAR FOOTER
    # -------------------------
    st.sidebar.markdown("---")

    with st.sidebar:
        if st.button("Refresh Data"):
            with st.spinner("Refreshing data..."):
                time.sleep(1)
                st.success("✅ Data refreshed!")
                st.rerun()


if __name__ == "__main__":
    main()
