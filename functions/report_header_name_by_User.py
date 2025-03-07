import streamlit as st
import pandas as pd
from functions.secrets_config import get_secrets_config

db_config = get_secrets_config()
infeed_database_name = db_config["database"]
enecoms_database_name = db_config["enecoms_database"]
TerminalName = ''
PinCode  =''

# Function to fetch and process the SQL query
def get_report_headers_and_reports_names_by_user(engine):
    sql_query = f"""
        exec [Report].[SSRS_WebMenuItemsByUser] '{PinCode}','{TerminalName}'  

    """
    # Read the SQL query into a DataFrame
    df = pd.read_sql_query(sql_query, engine)
    # Ensure the DataFrame is not empty
    if df.empty:
        st.error("No data found. Please check your database or query.")
    else:
        headers_name = df[['HeaderId', 'ReportDisplayName']].drop_duplicates()
        reports_names = df[['ReportDisplayName', 'HeaderId', 'ReportDisplayName', 'ReportName']].drop_duplicates()

    return headers_name,reports_names