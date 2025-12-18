# frontend/pages/1_💰_Sell_Product.py

import streamlit as st
import requests
import os
from streamlit_audiorecorder import audiorecorder

# --- Configuration & Session State Check ---
# Ensure the user is authenticated before showing the page
if not st.session_state.get("authenticated", False):
    st.error("Please log in first to access this page.")
    st.stop()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
st.set_page_config(page_title="Sell Product", page_icon="💰", layout="wide")

# --- UI Components ---
st.title("💰 List a Product for Sale")
st.sidebar.success(f"Logged in as Farmer #{st.session_state.user_id}")

# --- Voice Command Section ---
st.header("Option 1: List with Your Voice")
st.info("Record a command like: 'পঞ্চাশ কেজি আলু বিক্রি করতে চাই প্রতি কেজি পঁচিশ টাকা'")

audio_bytes = audiorecorder("Click to Record", "Recording...")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    if st.button("Process Voice Command"):
        files = {'audio_file': ('audio.wav', audio_bytes, 'audio/wav')}
        # The form data contains the seller_id from the session state
        form_data = {'seller_id': st.session_state.user_id}
        
        with st.spinner("🤖 Analyzing your voice command..."):
            try:
                response = requests.post(f"{BACKEND_URL}/api/v1/market/voice-command", files=files, data=form_data)
                
                if response.status_code == 200:
                    st.success("✅ Product listed successfully via voice!")
                    st.json(response.json()['details'])
                else:
                    st.error(f"Could not process command. Server says: {response.json().get('detail')}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: Could not reach the backend. Details: {e}")

# --- Manual Form Section ---
st.divider()
st.header("Option 2: List Manually (with a Form)")

with st.form("sell_product_form", border=False):
    product_name = st.text_input("Product Name (e.g., Potato, Rice)")
    quantity_kg = st.number_input("Quantity (in Kilograms)", min_value=0.1, step=0.5)
    price_per_kg = st.number_input("Price per KG (in BDT)", min_value=1.0, step=1.0)
    
    submitted = st.form_submit_button("List Product Manually")

    if submitted:
        # Construct a text command to be processed by the same NLP logic
        # This makes the backend simpler as it only needs one logic path
        text_command = f"{quantity_kg} কেজি {product_name} বিক্রি করব, কেজি {price_per_kg} টাকা"
        
        # This part simulates a voice command using text for the NLP service
        # A more direct approach would be a dedicated manual creation endpoint
        # But for the MVP, this reuses the powerful NLP logic
        
        st.info(f"Simulating voice command with text: '{text_command}'")
        # In a real app, you would have a dedicated endpoint for manual creation for efficiency
        # For now, this demonstrates the concept. 
