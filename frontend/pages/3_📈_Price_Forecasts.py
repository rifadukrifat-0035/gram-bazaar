# frontend/pages/3_📈_Price_Forecasts.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# --- Configuration & Session State Check ---
if not st.session_state.get("authenticated", False):
    st.error("Please log in first to access this page.")
    st.stop()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
st.set_page_config(page_title="Price Forecasts", page_icon="📈", layout="wide")

# --- UI Components ---
st.title("📈 AI-Powered Price Forecasts")
st.sidebar.success(f"Logged in as Farmer #{st.session_state.user_id}")
st.info("Select a crop to see the AI-generated price forecast for the next 7 days.")

product_options = ("potato", "rice", "onion")
selected_product = st.selectbox("Select a Product", product_options)

if st.button(f"Generate Forecast for {selected_product.capitalize()}"):
    # Simulate a voice command for forecast
    text_command = f"{selected_product} দামের পূর্বাভাস দেখাও"
    
    # This requires a hypothetical audio file or a backend that can accept text
    # For this MVP, we will directly call a forecast endpoint if it exists
    # Let's assume we add a dedicated endpoint for simplicity
    
    with st.spinner(f"🤖 Generating forecast for {selected_product}..."):
        try:
            # We'll use a direct forecast endpoint for cleaner design
            # You would need to add this endpoint to your backend products.py
            # GET /api/v1/market/forecast/{crop_name}
            
            # For now, we use the voice endpoint as designed before
            # This is less ideal but works with the existing code
            class MockAudio:
                def read(self): return b'mock_audio_data'
            
            files = {'audio_file': ('mock.wav', MockAudio().read(), 'audio/wav')}
            # We need to hack the NLP service to return our desired text.
            # A better way is to create a dedicated forecast endpoint.
            # Let's assume the user said the forecast text.
            # The current backend handles this if NLP returns the right intent.
            
            # Let's write the code assuming the NLP works as intended from voice
            # This is for UI demonstration
            st.warning("Demonstration Mode: Using mock data. A full implementation would process a real audio command.")

            base_price = {"potato": 25, "rice": 50, "onion": 40}.get(selected_product, 30)
            forecast = st.session_state.get('price_prediction_service').generate_mock_forecast(base_price)
            advice = st.session_state.get('price_prediction_service').get_ai_advice(forecast)

            st.success("Forecast Generated!")

            st.subheader("AI Advice:")
            st.warning(f"**{advice}**")
            
            forecast_df = pd.DataFrame(forecast)
            fig = px.line(
                forecast_df, x='date', y='price', title=f'7-Day Price Forecast for {selected_product.capitalize()}',
                labels={'date': 'Date', 'price': 'Predicted Price (BDT)'}, markers=True
            )
            fig.update_traces(line=dict(color='#1E88E5', width=3))
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Could not generate forecast. Error: {e}")
