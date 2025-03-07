import sys
import os
import streamlit as st

# Set project root to one level above this script's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import the function to be tested
from functions.embedded_SSRS import embed_ssrs_report  # Adjust this import based on your actual module

# Set the page configuration at the start


def run_test():
    """
    Test `embed_ssrs_report` function.
    """
    st.header("Testing embed_ssrs_report")
    
    try:
        # Provide dummy parameters for testing
        reportRDLname = "Intake"  # Replace with an actual report name for testing
        minDate = "2023-01-01"
        maxDate = "2023-12-31"

        # Call the function to embed the SSRS report
        embed_ssrs_report(reportRDLname, minDate, maxDate)

        st.success("embed_ssrs_report: Function executed without errors.")
        
    except Exception as e:
        st.error(f"embed_ssrs_report: Error encountered - {e}")

