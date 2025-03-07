import sys
import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Set project root to one level above this script's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import the function to be tested
from functions.report_header_name import get_report_headers_and_reports_names
from functions.secrets_config import get_secrets_config

# Retrieve database configuration
db_config = get_secrets_config()
database_name = db_config["database"]  # Use appropriate database name

# Create a SQLAlchemy engine for testing
engine = create_engine(f"mssql+pyodbc://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server")

def run_test():
    """
    Test `get_report_headers_and_reports_names` function.
    """
    st.header("Testing get_report_headers_and_reports_names")
    
    try:
        # Provide a sample project name for testing
        project_name = 'Infeed700'  # or 'Enecoms'

        # Call the function to get report headers and names
        headers_name, reports_names = get_report_headers_and_reports_names(project_name, engine)

        # Check if the outputs are as expected
        if headers_name is not None and not headers_name.empty:
            st.success("get_report_headers_and_reports_names: Headers retrieved successfully.")
            st.write("Headers:", headers_name)
        else:
            st.error("get_report_headers_and_reports_names: No headers found.")

        if reports_names is not None and not reports_names.empty:
            st.success("get_report_headers_and_reports_names: Reports names retrieved successfully.")
            st.write("Reports Names:", reports_names)
        else:
            st.error("get_report_headers_and_reports_names: No report names found.")

    except Exception as e:
        st.error(f"get_report_headers_and_reports_names: Error encountered - {e}")


