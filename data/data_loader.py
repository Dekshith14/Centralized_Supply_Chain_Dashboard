import streamlit as st
import pandas as pd
from config.settings import DATA_FILES, CACHE_TTL


# Load data with caching
@st.cache_data(ttl=300)

def load_data():

    # Load all necessary data files with error handling
    data_files = {
        "inventory": "inventory.csv",
        "orders": "orders.csv",
        "shipments": "shipments.csv",
        "costs": "costs.csv",
        "suppliers": "suppliers.csv"
    }
    
    data = {}
    for key, filename in data_files.items():
        try:
            df = pd.read_csv(filename)
            # Convert date columns if they exist
            date_columns = [col for col in df.columns if 'date' in col.lower()]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
            data[key] = df
        
        except FileNotFoundError:
            st.warning(f"Data file {filename} not found! Some features may be limited.")
            data[key] = pd.DataFrame()
    
    return data