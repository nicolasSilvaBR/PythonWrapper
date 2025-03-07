import sys
import os
import streamlit as st

# Set project root to one level above this script's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import the function to be tested
from functions.secrets_config import get_secrets_config

def run_test():
    """
    Test `get_secrets_config` function.
    """
    st.header("Testing get_secrets_config")
    try:
        db_config = get_secrets_config()
        if db_config:
            st.success("get_secrets_config: Loaded configuration successfully.")
            st.write("Configuration:", db_config)
        else:
            st.error("get_secrets_config: Failed to load configuration.")
    except Exception as e:
        st.error(f"get_secrets_config: Error encountered - {e}")
