import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def render_supplier_performance(data):
    suppliers = data["suppliers"]
    inventory = data["inventory"]
    
    st.title("📊 Supplier Performance Analysis")
    
    if not suppliers.empty:
        # Supplier selection
        selected_supplier = st.selectbox("Select Supplier for Detailed Analysis", 
                                        options=["All Suppliers"] + suppliers["supplier_name"].tolist())
        
        if selected_supplier == "All Suppliers":
            # Radar chart for all suppliers
            st.subheader("Comparative Performance Analysis")
            
            fig = go.Figure()
            
            categories = ["Reliability", "Lead Time", "On-Time Delivery", "Quality", "Cost"]
            
            for _, supplier in suppliers.iterrows():
                # Normalize metrics for radar chart (higher is better)
                lead_time_score = 5 - (supplier["avg_lead_time"] / 20 * 5)  # Invert so lower is better
                
                fig.add_trace(go.Scatterpolar(
                    r=[supplier["reliability_score"], lead_time_score, 
                       supplier["on_time_delivery"] * 5, supplier["quality_score"], 4],
                    theta=categories,
                    fill='toself',
                    name=supplier["supplier_name"]
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )),
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show supplier table
            st.subheader("Supplier Performance Metrics")
            suppliers_display = suppliers.copy()
            suppliers_display["on_time_delivery"] = suppliers_display["on_time_delivery"].apply(lambda x: f"{x*100:.1f}%")
            st.dataframe(suppliers_display)
            
            # Supplier ranking
            st.subheader("Supplier Ranking")
            
            # Calculate overall score (weighted average)
            supplier_rank = suppliers.copy()
            supplier_rank["lead_time_score"] = 5 - (supplier_rank["avg_lead_time"] / 20 * 5)
            supplier_rank["overall_score"] = (
                supplier_rank["reliability_score"] * 0.25 +
                supplier_rank["lead_time_score"] * 0.25 +
                supplier_rank["on_time_delivery"] * 5 * 0.25 +
                supplier_rank["quality_score"] * 0.25
            )
            
            supplier_rank = supplier_rank.sort_values("overall_score", ascending=False)
            
            fig = px.bar(supplier_rank, x="supplier_name", y="overall_score",
                       labels={"supplier_name": "Supplier", "overall_score": "Overall Score"},
                       color="overall_score",
                       title="Supplier Performance Ranking")
            st.plotly_chart(fig)
            
        else:
            # Single supplier detailed analysis
            supplier_data = suppliers[suppliers["supplier_name"] == selected_supplier].iloc[0]
            
            st.subheader(f"Detailed Analysis: {selected_supplier}")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Reliability Score", f"{supplier_data['reliability_score']:.1f}/5")
            col2.metric("Lead Time", f"{supplier_data['avg_lead_time']} days")
            col3.metric("On-Time Delivery", f"{supplier_data['on_time_delivery']*100:.1f}%")
            col4.metric("Quality Score", f"{supplier_data['quality_score']:.1f}/5")
            
            # Get items supplied by this supplier
            if not inventory.empty:
                supplier_items = inventory[inventory["supplier"] == selected_supplier]
                
                if not supplier_items.empty:
                    st.subheader(f"Items Supplied by {selected_supplier}")
                    st.dataframe(supplier_items[["item_name", "stock_level", "lead_time_days"]])
                    
                    # Stock levels of items from this supplier
                    fig = px.bar(supplier_items, x="item_name", y="stock_level", 
                               color="stock_level",
                               labels={"item_name": "Item", "stock_level": "Stock Level"},
                               title=f"Current Stock Levels - {selected_supplier} Items")
                    st.plotly_chart(fig)
                    
                    # Risk assessment
                    critical_items = supplier_items[supplier_items["stock_level"] < supplier_items["reorder_threshold"]]
                    if not critical_items.empty:
                        st.warning(f"⚠️ Critical stock levels for {len(critical_items)} items supplied by {selected_supplier}")
                        st.dataframe(critical_items[["item_name", "stock_level", "reorder_threshold"]])
                else:
                    st.info(f"No items currently sourced from {selected_supplier}")
            
            # Performance history (simulated)
            st.subheader("Performance History")
            
            # Generate dummy historical data
            dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
            history = pd.DataFrame({
                "date": dates,
                "on_time_delivery": np.clip(
                    np.random.normal(supplier_data["on_time_delivery"], 0.05, size=12),
                    0, 1
                ),
                "quality_score": np.clip(
                    np.random.normal(supplier_data["quality_score"], 0.2, size=12),
                    1, 5
                ),
                "lead_time": np.clip(
                    np.random.normal(supplier_data["avg_lead_time"], 2, size=12),
                    1, 30
                ).astype(int)
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=history["date"], 
                y=history["on_time_delivery"],
                mode='lines+markers',
                name='On-Time Delivery %'
            ))
            fig.add_trace(go.Scatter(
                x=history["date"], 
                y=history["quality_score"] / 5,  # Normalize to 0-1 scale
                mode='lines+markers',
                name='Quality Score (normalized)'
            ))
            fig.update_layout(title="Historical Performance Metrics")
            st.plotly_chart(fig)
            
            # Notes and action items
            st.subheader("Notes & Action Items")
            
            notes = st.text_area("Supplier Notes", placeholder="Enter notes about this supplier...")
            
            col1, col2 = st.columns(2)
            with col1:
                action_required = st.selectbox("Action Required", 
                                             ["None", "Review Contract", "Request Quality Improvement", 
                                              "Negotiate Lead Times", "Find Alternative Supplier"])
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            
            if st.button("Save Notes & Actions"):
                st.success("✅ Supplier information updated successfully!")
    else:
        st.info("No supplier data available.")