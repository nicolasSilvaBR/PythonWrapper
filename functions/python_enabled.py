import streamlit as st
import pandas as pd
from functions.secrets_config import get_secrets_config

db_config = get_secrets_config()
infeed_database_name = db_config["database"]

# Function to fetch and process the SQL query
def IsPythonDemoEnabled(engine):
    sql_query = f"""  
        SELECT TOP 1 [ConfigSetting] 
        FROM {infeed_database_name}.[Report].[Config] 
        WHERE ConfigName = 'isPythonEnabled'      
    """
    try:
        # Read the SQL query into a DataFrame
        df = pd.read_sql_query(sql_query, engine)
        
        # Ensure the DataFrame is not empty
        if not df.empty:
            # Return only the value of ConfigSetting without DataFrame structure
            return df.iloc[0, 0]  # Access the first value directly
    except Exception:
        return '0'
