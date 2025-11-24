import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def render_inventory_management(data):
    inventory = data["inventory"]
    
    st.title("📦 Inventory Management")
    
    # Search Bar
    st.subheader("🔍 Search Inventory")
    search_item = st.text_input("Search by item name:")

    if search_item:
        filtered_inventory = inventory[inventory["item_name"].str.contains(search_item, case=False)]
        st.dataframe(filtered_inventory)

        csv = filtered_inventory.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Filtered Inventory", data=csv, file_name="filtered_inventory.csv")

    
    # Inventory Overview
    with st.expander("📦 Inventory Overview", expanded=True):
        st.subheader("Current Inventory")
        st.dataframe(inventory)

        if not inventory.empty:
            fig_inventory = px.bar(inventory, x="item_name", y="stock_level", color="stock_level",
                                title="Stock Levels", labels={"stock_level": "Stock Level"})
            st.plotly_chart(fig_inventory)

            low_stock = inventory[inventory["stock_level"] < inventory["reorder_threshold"]]
            if not low_stock.empty:
                st.warning("⚠️ Low stock items detected:")
                st.dataframe(low_stock)

    
    # Manual Inventory Update
    with st.expander("✍️ Update Inventory"):
        with st.form(key="manual_inventory_update"):
            item_name = st.text_input("Item Name").strip().lower()
            stock_level = st.number_input("Stock Level", min_value=0)
            reorder_threshold = st.number_input("Reorder Threshold", min_value=0)
            submitted = st.form_submit_button("Update Inventory")

            if submitted:
                existing = inventory[inventory["item_name"].str.lower() == item_name].index
                if not existing.empty:
                    inventory.loc[existing, "stock_level"] = stock_level
                    inventory.loc[existing, "reorder_threshold"] = reorder_threshold
                    st.success(f"✅ '{item_name}' updated!")
                else:
                    new_row = pd.DataFrame([{
                        "item_name": item_name,
                        "stock_level": stock_level,
                        "reorder_threshold": reorder_threshold,
                        "supplier": "New Supplier",
                        "lead_time_days": 7,
                        "last_updated": datetime.now()
                    }])
                    inventory = pd.concat([inventory, new_row], ignore_index=True)
                    st.success(f"✅ '{item_name}' added!")

                inventory.to_csv("inventory.csv", index=False)
                st.rerun()

    
    # Reduce Stock Level
    with st.expander("➖ Reduce Inventory Stock"):
        if not inventory.empty:
            with st.form("reduce_stock_form"):
                item_to_reduce = st.selectbox("Select Item", options=inventory["item_name"].unique())
                max_qty = int(inventory[inventory["item_name"] == item_to_reduce]["stock_level"].values[0])
                reduce_qty = st.number_input("Quantity to reduce", min_value=1, max_value=max_qty if max_qty > 0 else 1, step=1)
                reduce_submitted = st.form_submit_button("Reduce")

                if reduce_submitted:
                    inventory.loc[inventory["item_name"] == item_to_reduce, "stock_level"] -= reduce_qty
                    inventory["stock_level"] = inventory["stock_level"].clip(lower=0)
                    inventory.to_csv("inventory.csv", index=False)
                    st.success(f"✅ Reduced {reduce_qty} units from '{item_to_reduce}'")
                    st.rerun()
        else:
            st.info("Inventory is empty.")

            
    
    # Inventory Metrics
    st.subheader("Inventory Metrics")
    
    if not inventory.empty:
        total_inventory = inventory["stock_level"].sum()
        avg_lead_time = inventory["lead_time_days"].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Items in Stock", total_inventory)
        col2.metric("Average Lead Time", f"{avg_lead_time:.1f} days")
        col3.metric("Stock Health", f"{len(inventory[inventory['stock_level'] > inventory['reorder_threshold']]) / len(inventory) * 100:.1f}%")
        
        # Inventory by Supplier
        st.subheader("Inventory by Supplier")
        supplier_inventory = inventory.groupby("supplier")["stock_level"].sum().reset_index()
        fig = px.pie(supplier_inventory, values="stock_level", names="supplier", 
                   title="Stock Distribution by Supplier")
        st.plotly_chart(fig)
        
        # Inventory Value Estimation
        st.subheader("Estimated Inventory Value")
        # Add dummy unit costs for demonstration
        inventory_value = inventory.copy()
        inventory_value["unit_cost"] = np.random.uniform(10, 100, len(inventory)).round(2)
        inventory_value["total_value"] = inventory_value["stock_level"] * inventory_value["unit_cost"]
        
        fig = px.bar(inventory_value.sort_values("total_value", ascending=False), 
                   x="item_name", y="total_value", 
                   color="supplier",
                   title="Estimated Value by Item")
        st.plotly_chart(fig)
        
        total_value = inventory_value["total_value"].sum()
        st.info(f"Total estimated inventory value: ${total_value:,.2f}")