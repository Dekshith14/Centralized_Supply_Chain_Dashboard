import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np



def render_cost_analysis(data):
    costs = data["costs"]
    
    st.title("💰 Supply Chain Cost Analysis")
    
    if not costs.empty:
        # Main cost metrics
        total_cost = costs["amount"].sum()
        total_budget = costs["budget"].sum()
        variance = total_budget - total_cost
        variance_pct = (variance / total_budget) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cost", f"${total_cost:,.2f}")
        col2.metric("Total Budget", f"${total_budget:,.2f}")
        col3.metric("Variance", f"${variance:,.2f}", delta=f"{variance_pct:.1f}%")
        
        # Cost breakdown
        st.subheader("Cost Breakdown")
        
        fig = px.bar(costs, x="category", y=["amount", "budget"],
                   barmode="group",
                   labels={"value": "Amount ($)", "variable": "Type"},
                   title="Cost vs Budget by Category")
        st.plotly_chart(fig)
        
        # Add variance calculation
        costs_analysis = costs.copy()
        costs_analysis["variance"] = costs_analysis["budget"] - costs_analysis["amount"]
        costs_analysis["variance_pct"] = (costs_analysis["variance"] / costs_analysis["budget"]) * 100
        
        # Variance analysis
        st.subheader("Variance Analysis")
        
        fig = px.bar(costs_analysis.sort_values("variance"), x="category", y="variance",
                   labels={"variance": "Budget Variance ($)", "category": "Category"},
                   color="variance",
                   color_continuous_scale=px.colors.diverging.RdYlGn,
                   title="Budget Variance by Category")
        st.plotly_chart(fig)
        
        # Cost table with variance
        st.subheader("Detailed Cost Analysis")
        display_cols = ["category", "amount", "budget", "variance", "variance_pct"]
        st.dataframe(costs_analysis[display_cols].style.format({
            "amount": "${:,.2f}",
            "budget": "${:,.2f}",
            "variance": "${:,.2f}",
            "variance_pct": "{:.1f}%"
        }))
        
        # Cost optimization opportunities
        st.subheader("Cost Optimization Opportunities")
        
        # Identify categories with significant overspending
        overspend = costs_analysis[costs_analysis["variance"] < 0].sort_values("variance")
        
        if not overspend.empty:
            st.warning("Categories exceeding budget:")
            for _, row in overspend.iterrows():
                st.write(f"⚠️ **{row['category']}**: ${-row['variance']:,.2f} over budget ({-row['variance_pct']:.1f}% variance)")
        else:
            st.success("All categories are within budget!")
        
        # Cost-saving recommendations
        st.subheader("Cost Optimization Recommendations")
        
        # Sample recommendations (in real application, these would be ML-driven)
        recommendations = [
            "Consider consolidating shipments to reduce transportation costs",
            "Evaluate supplier contracts for raw materials to identify potential savings",
            "Optimize inventory levels to reduce holding costs",
            "Review administrative expenses for potential streamlining",
            "Analyze manufacturing processes for efficiency improvements"
        ]
        
        for rec in recommendations:
            st.write(f"💡 {rec}")
    else:
        st.info("No cost data available. Please upload or generate sample cost data.")