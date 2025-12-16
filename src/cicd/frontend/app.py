import streamlit as st
import requests
from loguru import logger
import os

# --- Configuration de Loguru ---

# Add a sink to make logs writes on stderr/stdout (Docker ready)
logger.add(
    "file_{time}.log", 
    rotation="10 MB", 
    compression="zip", 
    enqueue=True, 
    level="INFO"
)
logger.info("Steamlit app started")

# --- API setting ---

# Utiliser le nom du service Docker pour atteindre le backend
# Par défaut, le port 8000 de FastAPI est exposé.
API_BASE_URL = os.environ.get("API_BASE_URL", "http://backend:8000")
SQUARE_ENDPOINT = f"{API_BASE_URL}/square"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"

logger.info(f"API configured : {API_BASE_URL}")

# --- Fonctions Logiques ---

def check_backend_health():
    """Health check"""
    try:
        logger.info(f"Try to connect to {HEALTH_ENDPOINT}...")
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        response.raise_for_status()
        logger.info(f"Health check successful : {response.json()}")
        st.success(f"Backend is connected : {response.json().get('status', 'OK')}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Health check failed. Error: {e}")
        st.error(f"Backend connection failed on ({HEALTH_ENDPOINT}). Check docker container.")
        return False

def call_square_api(number_to_square: int):
    """API Call"""
    
    # 1. JSON Requeste
    payload = {"number": number_to_square}
    logger.info(f"API call with : {payload}")

    try:
        # 2. Send the POST request
        response = requests.post(SQUARE_ENDPOINT, json=payload, timeout=10)
        
        # 3. Check HTTP status
        if response.status_code == 200:
            result = response.json().get("square")
            logger.success(f"API responds with : {result}")
            return result
        
        # 4. 422 error handling (Validation Pydantic)
        elif response.status_code == 422:
            error_detail = response.json().get("detail", "Unknown validation error")
            error_msg = f"Pydantic check failed : {error_detail[0].get('msg', 'Incorrect format')}"
            logger.warning(f"422 status received from API : {error_msg}")
            st.error(f"Wrong entry : {error_msg}")
            return None
            
        # 5. Other HTTP errors handling
        else:
            logger.error(f"Unattended HTTP error - Status: {response.status_code}, Response: {response.text}")
            st.error(f"Backend uncaught error (Status {response.status_code}).")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed. Error: {e}")
        st.error(f"Connection failed : Unable to connect to API {SQUARE_ENDPOINT}.")
        return None

# --- Streamlit IHM ---

st.set_page_config(page_title="Square API", layout="centered")

st.title("🔢 Square computing")

# Backend healthcheck
if check_backend_health():
    st.markdown("---")

    # Input field
    number_input = st.number_input(
        "Enter an integer :",
        min_value=-999999999,
        max_value=999999999,
        value=0,
        step=1,
        format="%d" # Streamlit handle number as float, so, ensure interger is displayed
    )
    
    # Cast to integer
    number_to_square = int(number_input) 

    if st.button("Compute square"):
        logger.info(f"Trigger computation with : {number_to_square}")
        
        # API Call
        with st.spinner("Wait for backend response..."):
            result = call_square_api(number_to_square)

        # Display result
        if result is not None:
            st.balloons()
            st.success(f"Square from **{number_to_square}** is : **{result}**")