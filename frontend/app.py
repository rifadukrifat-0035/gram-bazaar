# frontend/app.py
import streamlit as st
import requests
import os

# Use environment variable for backend URL, default to Docker's service name
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="Gram-Bazaar Login", page_icon="🌾", layout="centered")

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'phone_number' not in st.session_state:
    st.session_state.phone_number = ""
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

def login_page():
    st.title("Welcome to Gram-Bazaar 🌾")
    st.header("Login or Register")

    phone = st.text_input("Enter your phone number (e.g., +88017...)", key="phone_input")
    
    if st.button("Send OTP"):
        if phone:
            st.session_state.phone_number = phone
            try:
                with st.spinner("Sending OTP..."):
                    response = requests.post(f"{BACKEND_URL}/api/v1/auth/send-otp", json={"phone_number": phone})
                    if response.status_code == 202:
                        st.success("OTP sent! Please check the terminal for the simulated OTP.")
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: Could not connect to the backend. Is it running? Details: {e}")
        else:
            st.warning("Please enter a phone number.")

    otp = st.text_input("Enter 6-digit OTP", max_chars=6, key="otp_input")
    if st.button("Login"):
        try:
            with st.spinner("Verifying OTP..."):
                response = requests.post(f"{BACKEND_URL}/api/v1/auth/verify-otp", json={"phone_number": st.session_state.phone_number, "otp": otp})
                if response.status_code == 200:
                    st.session_state.authenticated = True
                    st.session_state.user_id = int(str(st.session_state.phone_number)[-4:]) # Simple user ID for MVP
                    st.rerun()
                else:
                    st.error(f"Invalid OTP: {response.json().get('detail')}")
        except requests.exceptions.RequestException:
             st.error("Verification failed. Please try again.")

def main_app_page():
    st.sidebar.success(f"Logged in as Farmer #{st.session_state.user_id}")
    st.title("Welcome to Gram-Bazaar!")
    st.write("Please select a page from the sidebar to get started.")

# Main logic to show login or app
if st.session_state.authenticated:
    main_app_page()
else:
    login_page()

