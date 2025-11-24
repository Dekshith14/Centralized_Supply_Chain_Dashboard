import pandas as pd
import numpy as np
from datetime import datetime
import os


# sample data generation
def create_sample_data_if_not_exists():
    
    # Inventory data
    if not os.path.exists("inventory.csv"):
        inventory_data = {
            "item_id": range(1, 11),
            "item_name": ["Aluminum Sheets", "Circuit Boards", "Steel Bolts", "Hydraulic Pumps", 
              "Corrugated Boxes", "Industrial Lubricant", "Resistors - 10kΩ", "Plastic Casings", 
              "Gear Assemblies", "Smartphone Model X"],
            "stock_level": [120, 85, 50, 30, 200, 15, 65, 25, 40, 75],
            "reorder_threshold": [50, 40, 30, 20, 100, 30, 30, 20, 25, 40],
            "supplier": ["TMT Pvt Ltd", "Techtronix Components", "Bharat Fasteners Co.", "TMT Pvt Ltd",
                "HydroMech Systems", "Techtronix Components", "Bharat Fasteners Co.", "Ace Packaging India", 
                "Techtronix Components", "In-House Production"],
            "lead_time_days": [14, 7, 10, 14, 5, 7, 10, 21, 14, 3],
            "last_updated": [datetime.now() - pd.Timedelta(days=x) for x in range(10)]
        }
        pd.DataFrame(inventory_data).to_csv("inventory.csv", index=False)
    
    
    # Orders data
    if not os.path.exists("orders.csv"):
        orders_data = {
            "order_id": [f"ORD-{i:04d}" for i in range(1, 31)],
            "customer": [f"Customer {chr(65 + i % 8)}" for i in range(30)],
            "order_date": [(datetime.now() - pd.Timedelta(days=i)) for i in range(30)],
            "requested_delivery": [(datetime.now() + pd.Timedelta(days=i % 10 + 5)) for i in range(30)],
            "status": np.random.choice(["New", "Processing", "Shipped", "Delivered", "Cancelled"], 30, 
                                     p=[0.1, 0.3, 0.3, 0.2, 0.1]),
            "total_value": np.random.uniform(500, 10000, 30).round(2)
        }
        pd.DataFrame(orders_data).to_csv("orders.csv", index=False)
    
    
    # Shipments data
    if not os.path.exists("shipments.csv"):
        shipments_data = {
            "shipment_id": [f"SHP-{i:04d}" for i in range(1, 26)],
            "order_id": [f"ORD-{i:04d}" for i in range(1, 26)],
            "ship_date": [(datetime.now() - pd.Timedelta(days=i % 15)) for i in range(1, 26)],
            "carrier": np.random.choice(["FedEx", "UPS", "DHL", "USPS"], 25),
            "status": np.random.choice(["In Transit", "Delivered", "Delayed", "Scheduled"], 25, 
                                     p=[0.4, 0.3, 0.2, 0.1]),
            "tracking_number": [f"TRK{i:06d}" for i in range(100000, 100025)],
            "estimated_arrival": [(datetime.now() + pd.Timedelta(days=i % 7)) for i in range(1, 26)]
        }
        pd.DataFrame(shipments_data).to_csv("shipments.csv", index=False)
    
    
    # Costs data
    if not os.path.exists("costs.csv"):
        categories = ["Raw Materials", "Manufacturing", "Warehousing", "Transportation", 
                    "Inventory Holding", "Order Processing", "Returns", "Administrative"]
        costs_data = {
            "category": categories,
            "amount": [125000, 87500, 45000, 67500, 32000, 18500, 12000, 36000],
            "budget": [130000, 90000, 50000, 70000, 35000, 20000, 15000, 40000],
            "period": ["Q1 2025"] * 8
        }
        pd.DataFrame(costs_data).to_csv("costs.csv", index=False)
    
    
    # Supplier data - new dataset
    if not os.path.exists("suppliers.csv"):
        supplier_data = {
            "supplier_name": ["TMT Pvt Ltd", "Techtronix Components", "Bharat Fasteners Co.", "HydroMech Systems", "Ace Packaging India"],
            "reliability_score": [4.2, 3.8, 4.7, 3.5, 4.0],
            "avg_lead_time": [12, 8, 11, 6, 18],
            "on_time_delivery": [0.92, 0.85, 0.95, 0.78, 0.88],
            "quality_score": [4.5, 3.9, 4.8, 3.7, 4.1],
            "location": ["Mumbai, Maharashtra", "Bangalore, Karnataka", "Ludhiana, Punjab", "Hyderabad, Telangana", "Ahmedabad, Gujarat"]
        }
        pd.DataFrame(supplier_data).to_csv("suppliers.csv", index=False)