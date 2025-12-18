# frontend/pages/2_🛒_Browse_Market.py

import streamlit as st
import pandas as pd
import requests
import os

# --- Configuration & Session State Check ---
if not st.session_state.get("authenticated", False):
    st.error("Please log in first to access this page.")
    st.stop()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
st.set_page_config(page_title="Browse Market", page_icon="🛒", layout="wide")

# --- UI Components ---
st.title("🛒 Browse the Live Market")
st.sidebar.success(f"Logged in as Farmer #{st.session_state.user_id}")

@st.cache_data(ttl=30) # Cache data for 30 seconds to reduce API calls
def fetch_products():
    """Fetches product data from the backend API and caches it."""
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/market/")
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")
        return None

if st.button("🔄 Refresh Listings"):
    st.cache_data.clear() # Manually clear cache
    st.rerun()

products = fetch_products()

if products:
    st.success(f"Found {len(products)} products listed in the market.")
    # Display products in a grid-like fashion
    cols = st.columns(2) # Create 2 columns for a better layout
    for i, product in enumerate(products):
        col = cols[i % 2]
        with col:
            with st.container(border=True):
                st.subheader(product["name"].capitalize())
                st.markdown(f"**Seller ID:** `{product['seller_id']}`")
                st.markdown(f"**Available:** `{product['quantity_kg']}` kg")
                st.metric(label="Price per kg", value=f"BDT {product['price_per_kg']:.2f}")
else:
    st.warning("No products found in the market, or could not fetch data. Please try refreshing.")

