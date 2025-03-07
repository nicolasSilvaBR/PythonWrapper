import sys
import os
import streamlit as st

# Set project root to one level above this script's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import the function to be tested
from functions.config import set_page_config

def run_test():
    """
    Test `set_page_config` function.
    """
    st.header("Testing set_page_config")
    try:
        # Check if the configuration was applied correctly
        if "selected-project" in st.session_state:
            st.success(f"set_page_config: Page configuration set successfully for project '{st.session_state['selected-project']}'")
        else:
            st.error("set_page_config: 'selected-project' not found in session state.")
        
    except Exception as e:
        st.error(f"set_page_config: Error encountered - {e}")
