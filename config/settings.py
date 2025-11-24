import streamlit as st
from datetime import datetime, timedelta

# page configuration
PAGE_CONFIG = {
    "page_title": "📦 Supply Chain Monitoring Dashboard",
    "layout": "wide"
}

# file paths
DATA_FILES = {
    "inventory": "inventory.csv",
    "orders": "orders.csv", 
    "shipments": "shipments.csv",
    "costs": "costs.csv",
    "suppliers": "suppliers.csv"
}

# Cache settings
CACHE_TTL = 300  # 5 minutes