# Centralized-Supply-Chain-Monitoring-System
A web application that provides real-time monitoring and analytics of key supply chain operations.


## In this repo
```
supply_chain_dashboard/
├── main.py                # Main streamlit app entry point
├── config/
│   └── settings.py        # Configuration settings
├── data/
│   ├── __init__.py
│   ├── data_generator.py  # Sample data creation generation
│   └── data_loader.py     # Data loading functions
├── models/
│   ├── __init__.py
│   └── forecasting.py     # ML models and forecasting
└── pages/
    ├── __init__.py
    ├── dashboard.py       # Dashboard overview
    ├── inventory.py       # Inventory management
    ├── orders.py          # Order & shipment tracking
    ├── costs.py           # Cost analysis
    ├── suppliers.py       # Supplier performance
    ├── forecasting.py     # Demand forecasting
    └── alerts.py          # Alerts & notifications

```


## Key supply chain operations -
1. Supply chain overview - Provides a summary of the most critical components of the supply chain between a period of time of our choosing
2. Inventory management -  Lists of current inventory items, search options, manual update options and visualizations for various inventory-related metrics
3. Order and shipment tracking - Tracking the movement of goods and supplies through the various phases of the supply chain
4. Cost analysis - Analysis of all cost and finance related data in the supply chain
5. Supplier performance tracking - Analysis of the best performing suppliers, ranking of suppliers etc.
6. Demand forecasting - Simple Moving Average (SMA) over the last 7 days to predict the demand for the next week
7. Alerts and notifications - Stockouts, shipment delays etc.


## Key features
1. Individual pages for the above-mentioned SCM operations.
2. Detailed visualizations -
   - Bar graphs
   - Pie charts
   - Line graphs
   - Web charts
3. Demand forecasting - Simple, straight-forward forecasting using Simple Moving Average (SMA)


## Screenshot of Overview Page
![Screenshot 2025-06-11 012439](https://github.com/user-attachments/assets/3d3e3b58-0bf1-4cbb-9911-800a72755905)
