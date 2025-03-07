import sys
import os
import streamlit as st
from sqlalchemy import text

# Set project root to one level above this script's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import the function to be tested
from functions.database_connection import mydb

def run_test():
    """
    Test `mydb` function.
    """
    st.header("Testing mydb")
    try:
        engine = mydb()
        if engine:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).fetchone()
                st.success("mydb: Database connection successful.")
                st.write("Test query result:", result)
        else:
            st.error("mydb: Failed to create database engine.")
    except Exception as e:
        st.error(f"mydb: Error encountered - {e}")
